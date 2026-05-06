from world.place import Place
from utils.enums.place_type import PlaceType
from lp.payoff_matrix_generator import PayoffMatrix
import numpy as np

# Manually create world matching assignment example
# Place 1: neutral, Place 2: easy, Place 3: hard, Place 4: easy
world = [[
    Place(win_value=1, lose_value=-1, place_type=PlaceType.neutral),
    Place(win_value=2, lose_value=-1, place_type=PlaceType.easy),
    Place(win_value=1, lose_value=-3, place_type=PlaceType.hard),
    Place(win_value=2, lose_value=-1, place_type=PlaceType.easy),
]]

pm = PayoffMatrix(world)
matrix = pm.generate_payoff_matrix()
print(matrix)