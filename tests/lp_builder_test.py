import numpy as np
from lp.lp_builder import LPBuilder
from utils.enums.role import Role

# Assignment example payoff matrix
payoff_matrix = np.array([
    [-1,  1,  1,  1],
    [ 2, -1,  2,  2],
    [ 1,  1, -3,  1],
    [ 2,  2,  2, -1]
])

# Test hider LP
print("=== HIDER LP ===")
builder = LPBuilder(payoff_matrix, Role.hider)
lp_dict = builder.build_lp_problem()
print("obj_fn_type:", lp_dict['obj_fn_type'])
print("obj_fn_values:", lp_dict['obj_fn_values'])
print("restrictions:", lp_dict['restrictions'])
print("constraints:")
for c in lp_dict['constraints']:
    print(f"  {c['lhs']} {c['constraint_type']} {c['rhs']}")