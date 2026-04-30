import sys
from utils.enums.obj_fn_type import ObjectiveFunctionType
from utils.enums.constraint_type import ConstraintType
from utils.enums.restriction_type import RestrictionType
from core.lp_problem import LPProblem
from core.constraint import Constraint
from core.tableau_matrix import TableauMatrix
from core.simplex_solver import SimplexSolver
import numpy as np

# Test D
c1 = Constraint([-1, 1], ConstraintType.smaller_equal, 2)
c2 = Constraint([1, 1], ConstraintType.smaller_equal, 4)
prob = LPProblem(ObjectiveFunctionType.max, np.array([1, 2]), [c1, c2], [RestrictionType.free, RestrictionType.non_negative])
tm = TableauMatrix(prob)
tm.build_tableau_matrix()
solver = SimplexSolver(tm, prob)
res = solver.solve()
print("Test D Result:", res)
