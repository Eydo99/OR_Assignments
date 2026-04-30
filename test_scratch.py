import sys
from utils.enums.obj_fn_type import ObjectiveFunctionType
from utils.enums.constraint_type import ConstraintType
from utils.enums.restriction_type import RestrictionType
from core.lp_problem import LPProblem
from core.constraint import Constraint
from core.tableau_matrix import TableauMatrix
from core.simplex_solver import SimplexSolver
import numpy as np

# Test A: Pure <=
c1 = Constraint([1, 1], ConstraintType.smaller_equal, 4)
c2 = Constraint([1, 2], ConstraintType.smaller_equal, 8)
prob = LPProblem(ObjectiveFunctionType.max, np.array([2, 3]), [c1, c2], [RestrictionType.non_negative, RestrictionType.non_negative])
tm = TableauMatrix(prob)
tm.build_tableau_matrix()
solver = SimplexSolver(tm, prob)
res = solver.solve()
print("Test A Result:", res)

# Test B: >= constraints
c1 = Constraint([1, 1], ConstraintType.greater_equal, 4)
c2 = Constraint([1, 2], ConstraintType.equal, 8)
prob = LPProblem(ObjectiveFunctionType.max, np.array([2, 3]), [c1, c2], [RestrictionType.non_negative, RestrictionType.non_negative])
tm = TableauMatrix(prob)
tm.build_tableau_matrix()
solver = SimplexSolver(tm, prob)
res = solver.solve()
print("Test B Result:", res)

# Test C: Free variable
# max x1 + 2x2
# x1 - x2 <= 2
# x1 + x2 <= 4
# x1 is free, x2 >= 0
c1 = Constraint([1, -1], ConstraintType.smaller_equal, 2)
c2 = Constraint([1, 1], ConstraintType.smaller_equal, 4)
prob = LPProblem(ObjectiveFunctionType.max, np.array([1, 2]), [c1, c2], [RestrictionType.free, RestrictionType.non_negative])
tm = TableauMatrix(prob)
tm.build_tableau_matrix()
solver = SimplexSolver(tm, prob)
res = solver.solve()
print("Test C Result:", res)
