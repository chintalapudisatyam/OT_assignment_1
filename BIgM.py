import numpy as np


def big_m_simplex(c, A, b, constraint_types, M=1000000):
    """
    Big-M Simplex Method for maximization problems.

    c               : objective function coefficients
    A               : constraint coefficient matrix
    b               : RHS values
    constraint_types: '<=', '>=', or '='
    M               : Big-M penalty
    """

    c = np.array(c, dtype=float)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    m, n = A.shape
    original_n = n
    columns = [A[:, j].copy() for j in range(n)]
    variable_names = [f"x{j + 1}" for j in range(n)]
    basis = []
    for i, sign in enumerate(constraint_types):

        if sign == "<=":
            # Add slack variable
            col = np.zeros(m)
            col[i] = 1

            columns.append(col)
            variable_names.append(f"s{i + 1}")
            basis.append(len(columns) - 1)

        elif sign == ">=":
            # Add surplus variable
            col = np.zeros(m)
            col[i] = -1

            columns.append(col)
            variable_names.append(f"s{i + 1}")
            
            # Add artificial variable
            col = np.zeros(m)
            col[i] = 1

            columns.append(col)
            variable_names.append(f"a{i + 1}")
            basis.append(len(columns) - 1)

        elif sign == "=":
            # Add artificial variable
            col = np.zeros(m)
            col[i] = 1

            columns.append(col)
            variable_names.append(f"a{i + 1}")
            basis.append(len(columns) - 1)

    A_std = np.column_stack(columns)
    total_vars = A_std.shape[1]
    c_std = np.zeros(total_vars)

    for j in range(original_n):
        c_std[j] = c[j]
    for j, name in enumerate(variable_names):
        if name.startswith("a"):
            c_std[j] = -M

    tableau = np.zeros((m + 1, total_vars + 1))
    tableau[:m, :total_vars] = A_std
    tableau[:m, -1] = b
    tableau[-1, :total_vars] = -c_std    
    for i in range(m):
        basic_var = basis[i]

        coefficient = c_std[basic_var]

        tableau[-1, :] += coefficient * tableau[i, :]

    iteration = 0

    while True:

        iteration += 1

        print("\n" + "=" * 70)
        print("Iteration:", iteration)
        print("=" * 70)

        print("Basis:", [variable_names[i] for i in basis])

        print("\nTableau:")

        header = variable_names + ["RHS"]
        print(" | ".join(f"{x:>10}" for x in header))

        for row in tableau:
            print(" | ".join(f"{x:10.2f}" for x in row))

        #  entering variable
        objective_row = tableau[-1, :-1]

        entering = np.argmin(objective_row)

        # If all coefficients are >= 0, optimal solution reached
        if objective_row[entering] >= -1e-9:
            break


        ratios = []

        for i in range(m):

            if tableau[i, entering] > 1e-9:
                ratios.append(tableau[i, -1] / tableau[i, entering])
            else:
                ratios.append(np.inf)

        leaving = np.argmin(ratios)

        if ratios[leaving] == np.inf:
            raise ValueError("The problem is unbounded.")

        print("Entering variable:", variable_names[entering])
        print("Leaving variable:", variable_names[basis[leaving]])


        pivot = tableau[leaving, entering]

        tableau[leaving, :] /= pivot

        for i in range(m + 1):

            if i != leaving:

                factor = tableau[i, entering]

                tableau[i, :] -= factor * tableau[leaving, :]

        basis[leaving] = entering


    solution = np.zeros(total_vars)

    for i, basic_var in enumerate(basis):
        solution[basic_var] = tableau[i, -1]

    for j, name in enumerate(variable_names):

        if name.startswith("a") and solution[j] > 1e-6:
            raise ValueError("The problem is infeasible.")

    optimal_value = np.dot(c_std, solution)

    return variable_names, solution, optimal_value



# Objective:
# Max Z = 3x1 + 5x2

c = [3, 5]

# Constraints:
#
# x1 + x2 <= 4
# 2x1 + x2 >= 6
# x1 + 2x2 <= 6

A = [
    [1, 1],
    [2, 1],
    [1, 2]
]

b = [4, 6, 6]

constraint_types = [
    "<=",
    ">=",
    "<="
]

variables, solution, optimal_value = big_m_simplex(
    c,
    A,
    b,
    constraint_types
)
print("\n" + "=" * 70)
print("OPTIMAL SOLUTION")
print("=" * 70)

for name, value in zip(variables, solution):
    print(f"{name} = {value:.4f}")

print(f"\nOptimal objective value Z = {optimal_value:.4f}")
