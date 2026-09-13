# OT_assignment_1


This repository contains Python programs for solving two optimization problems using Operations Research methods.

## 1. Big-M Simplex Method

A Linear Programming Problem is solved using the Big-M Simplex Method.

**Objective:**

Maximize  
`Z = 3x1 + 5x2`

**Constraints:**

- `x1 + x2 <= 4`
- `2x1 + x2 >= 6`
- `x1 + 2x2 <= 6`
- `x1, x2 >= 0`

The program converts the LPP into standard form using slack, surplus, and artificial variables and applies the Big-M Simplex method to obtain the optimal solution.

**Result:**

- `x1 = 2`
- `x2 = 2`
- `Maximum Z = 16`

**File:** `BigM.py`

**Requirement:** Python 3 and NumPy

---

## 2. Transportation Problem

A balanced transportation problem with 3 warehouses and 4 markets is solved using:

- Vogel's Approximation Method (VAM)
- MODI (Modified Distribution) Method

VAM is used to obtain the Initial Basic Feasible Solution, and MODI is used to test and improve the solution until the optimum is reached.

**Supply:** `7, 9, 18`

**Demand:** `5, 8, 7, 14`

The total supply and total demand are both `34`, so the problem is balanced.

**Initial VAM Cost:** `779`

**Optimal Shipment Plan:**

|              | Market 1 | Market 2 | Market 3 | Market 4 |
|--------------|----------|----------|----------|----------|
| Warehouse 1  | 5        | 0        | 0        | 2        |
| Warehouse 2  | 0        | 2        | 7        | 0        |
| Warehouse 3  | 0        | 6        | 0        | 12       |

**Minimum Transportation Cost:** `743`

**File:** `Transportation.py`

**Requirement:** Python 3

---

## Repository Structure

```text
.
├── BigM.py
├── Transportation.py
└── README.md
