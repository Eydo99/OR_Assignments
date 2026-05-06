import numpy as np
from lp.lp_builder import LPBuilder
from lp.payoff_matrix_generator import PayoffMatrix
from simplex.parser import Parser
from simplex.tableau_matrix import TableauMatrix
from simplex.simplex_solver import SimplexSolver
from utils.enums.role import Role
from world.place import Place
from utils.enums.place_type import PlaceType

# Manually create world matching assignment example
world = [[
    Place(win_value=1, lose_value=-1, place_type=PlaceType.neutral),
    Place(win_value=2, lose_value=-1, place_type=PlaceType.easy),
    Place(win_value=1, lose_value=-3, place_type=PlaceType.hard),
    Place(win_value=2, lose_value=-1, place_type=PlaceType.easy),
]]

# Build payoff matrix
pm = PayoffMatrix(world)
matrix = pm.generate_payoff_matrix()
print("Payoff Matrix:\n", matrix)

# Build LP
builder = LPBuilder(matrix, Role.hider)
lp_dict = builder.build_lp_problem()

# Parse
parser = Parser(lp_dict)
lp_problem = parser.build_lp_problem()

# Build tableau
tableau = TableauMatrix(lp_problem)
tableau.build_tableau_matrix()

# Solve
solver = SimplexSolver(tableau, lp_problem)
result = solver.solve()
print("\nResult:", result)
