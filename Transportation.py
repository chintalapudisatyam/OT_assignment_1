def vogel_approximation_method(cost, supply, demand):

    m = len(supply)
    n = len(demand)

    # Copy supply and demand so original values are not changed
    supply = supply[:]
    demand = demand[:]
    allocation = [[0 for j in range(n)] for i in range(m)]
    active_rows = [True] * m
    active_cols = [True] * n

    while True:
        if sum(supply) == 0 and sum(demand) == 0:
            break
        row_penalties = []

        for i in range(m):

            if not active_rows[i]:
                row_penalties.append((-1, i))
                continue

            values = []

            for j in range(n):
                if active_cols[j] and demand[j] > 0:
                    values.append(cost[i][j])

            if len(values) >= 2:
                values.sort()
                penalty = values[1] - values[0]

            elif len(values) == 1:
                penalty = values[0]

            else:
                penalty = -1

            row_penalties.append((penalty, i))

        col_penalties = []

        for j in range(n):

            if not active_cols[j]:
                col_penalties.append((-1, j))
                continue

            values = []

            for i in range(m):
                if active_rows[i] and supply[i] > 0:
                    values.append(cost[i][j])

            if len(values) >= 2:
                values.sort()
                penalty = values[1] - values[0]

            elif len(values) == 1:
                penalty = values[0]

            else:
                penalty = -1

            col_penalties.append((penalty, j))


        best_row = max(row_penalties)
        best_col = max(col_penalties)


        if best_row[0] >= best_col[0]:

            i = best_row[1]

            available = [
                j for j in range(n)
                if active_cols[j] and demand[j] > 0
            ]

            j = min(available, key=lambda x: cost[i][x])

        else:

            j = best_col[1]

   
            available = [
                i for i in range(m)
                if active_rows[i] and supply[i] > 0
            ]

            i = min(available, key=lambda x: cost[x][j])


        quantity = min(supply[i], demand[j])

        allocation[i][j] = quantity

        supply[i] -= quantity
        demand[j] -= quantity



        if supply[i] == 0:
            active_rows[i] = False

        if demand[j] == 0:
            active_cols[j] = False

    return allocation

def print_allocation(allocation, cost):

    print("\nAllocation Table:")
    print("-" * 65)

    total_cost = 0

    for i in range(len(allocation)):

        row_total = 0

        for j in range(len(allocation[0])):

            quantity = allocation[i][j]

            if quantity > 0:
                print(
                    f"Warehouse {i + 1} -> Market {j + 1}: "
                    f"{quantity} units "
                    f"(Cost = {quantity} × {cost[i][j]})"
                )

                row_total += quantity * cost[i][j]

        total_cost += row_total

    print("-" * 65)
    print("Total Transportation Cost =", total_cost)

    return total_cost

def calculate_potentials(cost, allocation):

    m = len(cost)
    n = len(cost[0])

    u = [None] * m
    v = [None] * n

    u[0] = 0

    changed = True

    while changed:

        changed = False

        for i in range(m):

            for j in range(n):

                if allocation[i][j] > 0:

                    if u[i] is not None and v[j] is None:

                        v[j] = cost[i][j] - u[i]
                        changed = True

                    elif v[j] is not None and u[i] is None:

                        u[i] = cost[i][j] - v[j]
                        changed = True

    return u, v
def find_cycle(allocation, entering):

    m = len(allocation)
    n = len(allocation[0])

    basic = set()

    for i in range(m):
        for j in range(n):

            if allocation[i][j] > 0:
                basic.add((i, j))

    entering_i, entering_j = entering


    graph = {}

    for i, j in basic:

        row_node = ("r", i)
        col_node = ("c", j)

        if row_node not in graph:
            graph[row_node] = []

        if col_node not in graph:
            graph[col_node] = []

        graph[row_node].append(col_node)
        graph[col_node].append(row_node)

    start = ("r", entering_i)
    target = ("c", entering_j)


    def dfs(node, visited, path):

        if node == target:
            return path

        visited.add(node)

        for next_node in graph.get(node, []):

            if next_node not in visited:

                if node[0] == "r":
                    cell = (node[1], next_node[1])
                else:
                    cell = (next_node[1], node[1])

                result = dfs(
                    next_node,
                    visited,
                    path + [cell]
                )

                if result is not None:
                    return result

        return None

    path = dfs(start, set(), [])

    if path is None:
        return None

    cycle = [entering] + path

    return cycle

def modi_method(cost, allocation):

    m = len(cost)
    n = len(cost[0])

    iteration = 0

    while True:

        iteration += 1

        print("\n")
        print("=" * 70)
        print("MODI ITERATION", iteration)
        print("=" * 70)


        u, v = calculate_potentials(cost, allocation)

        print("\nU values:", u)
        print("V values:", v)


        best_delta = 0
        entering_cell = None

        print("\nOpportunity Costs:")

        for i in range(m):

            for j in range(n):

            
                if allocation[i][j] == 0:

                    delta = cost[i][j] - u[i] - v[j]

                    print(
                        f"Cell ({i + 1},{j + 1}) : "
                        f"Delta = {delta}"
                    )



                    if delta < best_delta:

                        best_delta = delta
                        entering_cell = (i, j)


        if entering_cell is None:

            print("\nAll opportunity costs are >= 0.")

            print("Therefore, the solution is OPTIMAL.")

            break

        print(
            "\nEntering cell:",
            f"({entering_cell[0] + 1},"
            f"{entering_cell[1] + 1})"
        )

        print("Most negative Delta =", best_delta)



        cycle = find_cycle(allocation, entering_cell)

        if cycle is None:
            print("Could not find a valid loop.")
            break

        print("\nClosed loop:")

        for i, j in cycle:

            print(
                f"({i + 1},{j + 1})",
                end=" -> "
            )

        print()


        print("\nLoop signs:")

        for k, (i, j) in enumerate(cycle):

            if k % 2 == 0:
                print(
                    f"+ ({i + 1},{j + 1})"
                )
            else:
                print(
                    f"- ({i + 1},{j + 1})"
                )


        minus_cells = cycle[1::2]

        theta = min(
            allocation[i][j]
            for i, j in minus_cells
        )

        print("\nTheta =", theta)



        for k, (i, j) in enumerate(cycle):

            if k % 2 == 0:
                allocation[i][j] += theta

            else:
                allocation[i][j] -= theta

        print("\nNew allocation:")

        for row in allocation:
            print(row)

    return allocation



# Transportation costs

cost = [

    [19, 30, 50, 10],

    [70, 30, 40, 60],

    [40, 8, 70, 20]

]




supply = [7, 9, 18]


# Demand of markets

demand = [5, 8, 7, 14]


# ------------------------------------------------------------
# STEP 1: VAM
# ------------------------------------------------------------

print("=" * 70)
print("TRANSPORTATION PROBLEM")
print("=" * 70)

print("\nUsing Vogel's Approximation Method (VAM)...")

allocation = vogel_approximation_method(
    cost,
    supply,
    demand
)

print("\nInitial Basic Feasible Solution obtained using VAM:")

initial_cost = print_allocation(
    allocation,
    cost
)


# ------------------------------------------------------------
# STEP 2: MODI
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("APPLYING MODI METHOD")
print("=" * 70)

allocation = modi_method(
    cost,
    allocation
)


# ------------------------------------------------------------
# FINAL ANSWER
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("FINAL OPTIMAL SOLUTION")
print("=" * 70)

final_cost = print_allocation(
    allocation,
    cost
)

print("\nInitial VAM Cost =", initial_cost)

print("Optimal MODI Cost =", final_cost)

print("\nOptimal Shipment Plan:")

for i in range(len(allocation)):

    for j in range(len(allocation[0])):

        if allocation[i][j] > 0:

            print(
                f"Warehouse {i + 1} -> "
                f"Market {j + 1} = "
                f"{allocation[i][j]} units"
            )

print("\nProgram completed successfully.")
