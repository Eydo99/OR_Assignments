import sys
import os
sys.path.append(r"d:\simplex")
from core.parser import Parser
from core.tableau_matrix import TableauMatrix
from core.simplex_solver import SimplexSolver

data = {
    "obj_fn_type": "min",
    "obj_fn_values": [4, 1],
    "constraints": [
        {"LHS": [3, 1], "type": "=", "RHS": 3},
        {"LHS": [4, 3], "type": ">=", "RHS": 6},
        {"LHS": [1, 2], "type": "<=", "RHS": 4}
    ],
    "restrictions": ["free", ">="]
}

parser = Parser(data)
lp_problem = parser.build_lp_problem()
tm = TableauMatrix(lp_problem)
tm.build_tableau_matrix()

solver = SimplexSolver(tm, lp_problem)
solver.solve()

for i, step in enumerate(solver.steps):
    p_row = step.get("pivot_row")
    p_col = step.get("pivot_col")
    print(f"Step {i}: '{step.get('message')}' - Pivot: {p_row} {type(p_row)}, {p_col} {type(p_col)}")
