import numpy as np
from utils.enums.obj_fn_type import ObjectiveFunctionType
from utils.enums.constraint_type import ConstraintType
from utils.enums.restriction_type import RestrictionType
from core.lp_problem import LPProblem
from core.constraint import Constraint
from core.tableau_matrix import TableauMatrix
from core.simplex_solver import SimplexSolver

PASS = 0
FAIL = 0

def run_test(name, lp_problem, expected_status, expected_obj=None, expected_vars=None, tol=1e-4):
    global PASS, FAIL
    try:
        tm = TableauMatrix(lp_problem)
        tm.build_tableau_matrix()
        solver = SimplexSolver(tm, lp_problem)
        result = solver.solve()

        if solver.result != expected_status:
            print(f"  ❌ FAIL [{name}] — status: got '{solver.result}', expected '{expected_status}'")
            FAIL += 1
            return

        if expected_obj is not None and result is not None:
            got_obj = result["optimal_value"]
            if abs(got_obj - expected_obj) > tol:
                print(f"  ❌ FAIL [{name}] — objective: got {got_obj:.6f}, expected {expected_obj:.6f}")
                FAIL += 1
                return

        if expected_vars is not None and result is not None:
            got_vars = result["variables"]
            for i, (g, e) in enumerate(zip(got_vars, expected_vars)):
                if e is not None and abs(g - e) > tol:
                    print(f"  ❌ FAIL [{name}] — x{i+1}: got {g:.6f}, expected {e:.6f}")
                    FAIL += 1
                    return

        print(f"  ✅ PASS [{name}]" + (f" — Z* = {result['optimal_value']:.4f}, vars = {[round(v,4) for v in result['variables']]}" if result else f" — status: {solver.result}"))
        PASS += 1

    except Exception as ex:
        import traceback
        print(f"  💥 ERROR [{name}] — {ex}")
        traceback.print_exc()
        FAIL += 1


# ════════════════════════════════════════════════════════
print("\n══════════ GROUP 1: STANDARD SIMPLEX (≤ only) ══════════")
# ════════════════════════════════════════════════════════

# 1A — Classic textbook max
run_test("1A: Classic 2-var max",
    LPProblem(ObjectiveFunctionType.max, np.array([5.0, 4.0]),
        [Constraint([6,4], ConstraintType.smaller_equal, 24),
         Constraint([1,2], ConstraintType.smaller_equal, 6)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=21.0, expected_vars=[3.0, 1.5])

# 1B — 3 variables
run_test("1B: 3-variable max",
    LPProblem(ObjectiveFunctionType.max, np.array([2.0, 3.0, 1.0]),
        [Constraint([1,1,1], ConstraintType.smaller_equal, 40),
         Constraint([2,1,0], ConstraintType.smaller_equal, 60),
         Constraint([0,1,1], ConstraintType.smaller_equal, 30)],
        [RestrictionType.non_negative]*3),
    "optimal", expected_obj=90.0)

# 1C — Minimization with ≤
run_test("1C: 2-var minimize",
    LPProblem(ObjectiveFunctionType.min, np.array([2.0, 3.0]),
        [Constraint([1,0], ConstraintType.smaller_equal, 4),
         Constraint([0,1], ConstraintType.smaller_equal, 6),
         Constraint([1,1], ConstraintType.smaller_equal, 8)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=0.0, expected_vars=[0.0, 0.0])

# 1D — Unbounded problem
run_test("1D: Unbounded (no upper bound on x1)",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([-1,1], ConstraintType.smaller_equal, 1)],
        [RestrictionType.non_negative]*2),
    "unbounded")

# 1E — Single variable
run_test("1E: Single variable",
    LPProblem(ObjectiveFunctionType.max, np.array([7.0]),
        [Constraint([1], ConstraintType.smaller_equal, 5)],
        [RestrictionType.non_negative]),
    "optimal", expected_obj=35.0, expected_vars=[5.0])

# 1F — Degenerate optimal (multiple constraints active at same point)
run_test("1F: Degenerate BFS",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,0], ConstraintType.smaller_equal, 4),
         Constraint([0,1], ConstraintType.smaller_equal, 4),
         Constraint([1,1], ConstraintType.smaller_equal, 4)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=4.0)

# 1G — Zero objective coefficients
run_test("1G: Zero objective coefficients",
    LPProblem(ObjectiveFunctionType.max, np.array([0.0, 0.0]),
        [Constraint([1,1], ConstraintType.smaller_equal, 10)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=0.0)

# 1H — Large coefficients
run_test("1H: Large coefficients",
    LPProblem(ObjectiveFunctionType.max, np.array([1000.0, 2000.0]),
        [Constraint([1,2], ConstraintType.smaller_equal, 100),
         Constraint([3,2], ConstraintType.smaller_equal, 150)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=100000.0)


# ════════════════════════════════════════════════════════
print("\n══════════ GROUP 2: TWO-PHASE METHOD (≥ and =) ══════════")
# ════════════════════════════════════════════════════════

# 2A — Single equality constraint
run_test("2A: Single equality",
    LPProblem(ObjectiveFunctionType.max, np.array([2.0, 3.0]),
        [Constraint([1,1], ConstraintType.equal, 4),
         Constraint([1,0], ConstraintType.smaller_equal, 3)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=12.0, expected_vars=[0.0, 4.0])

# 2B — Single >= constraint
run_test("2B: Single >= constraint",
    LPProblem(ObjectiveFunctionType.max, np.array([2.0, 3.0]),
        [Constraint([1,1], ConstraintType.greater_equal, 2),
         Constraint([1,2], ConstraintType.smaller_equal, 8)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=12.0)

# 2C — Infeasible (contradictory constraints)
run_test("2C: Infeasible problem",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.greater_equal, 10),
         Constraint([1,1], ConstraintType.smaller_equal, 5)],
        [RestrictionType.non_negative]*2),
    "infeasible")

# 2D — All equality constraints
run_test("2D: All equality constraints",
    LPProblem(ObjectiveFunctionType.max, np.array([3.0, 5.0]),
        [Constraint([1,0], ConstraintType.equal, 4),
         Constraint([0,2], ConstraintType.equal, 12),
         Constraint([3,2], ConstraintType.equal, 18)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=42.0, expected_vars=[4.0, 6.0])

# 2E — Mix of all three constraint types
run_test("2E: Mixed <=, >=, = constraints",
    LPProblem(ObjectiveFunctionType.min, np.array([2.0, 3.0, 1.0]),
        [Constraint([1,1,1], ConstraintType.equal, 10),
         Constraint([2,1,0], ConstraintType.greater_equal, 8),
         Constraint([0,1,1], ConstraintType.smaller_equal, 7)],
        [RestrictionType.non_negative]*3),
    "optimal")

# 2F — Infeasible with equality
run_test("2F: Infeasible equality",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.equal, 5),
         Constraint([1,1], ConstraintType.equal, 7)],
        [RestrictionType.non_negative]*2),
    "infeasible")

# 2G — >= with minimization
run_test("2G: Minimize with >= (diet-style problem)",
    LPProblem(ObjectiveFunctionType.min, np.array([0.6, 0.35]),
        [Constraint([3,1], ConstraintType.greater_equal, 6),
         Constraint([1,1], ConstraintType.greater_equal, 4),
         Constraint([0,1], ConstraintType.greater_equal, 1.5)],
        [RestrictionType.non_negative]*2),
    "optimal")

# 2H — Unbounded inside Two-Phase
run_test("2H: Unbounded after Phase 1 succeeds",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.greater_equal, 2)],
        [RestrictionType.non_negative]*2),
    "unbounded")


# ════════════════════════════════════════════════════════
print("\n══════════ GROUP 3: FREE (UNRESTRICTED) VARIABLES ══════════")
# ════════════════════════════════════════════════════════

# 3A — One free variable, optimal is positive
run_test("3A: One free variable (positive optimal)",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 2.0]),
        [Constraint([1,1], ConstraintType.smaller_equal, 4),
         Constraint([1,-1], ConstraintType.smaller_equal, 2)],
        [RestrictionType.free, RestrictionType.non_negative]),
    "optimal", expected_obj=8.0)

# 3B — Free variable takes negative value
run_test("3B: Free variable goes negative",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 3.0]),
        [Constraint([-1,1], ConstraintType.smaller_equal, 2),
         Constraint([1,1], ConstraintType.smaller_equal, 4)],
        [RestrictionType.free, RestrictionType.non_negative]),
    "optimal")

# 3C — Both variables free
run_test("3C: Both variables free",
    LPProblem(ObjectiveFunctionType.max, np.array([2.0, 1.0]),
        [Constraint([1,1], ConstraintType.smaller_equal, 6),
         Constraint([2,1], ConstraintType.smaller_equal, 10)],
        [RestrictionType.free, RestrictionType.free]),
    "optimal")

# 3D — Free variable with >= constraint
run_test("3D: Free variable + >= constraint",
    LPProblem(ObjectiveFunctionType.min, np.array([1.0, 2.0]),
        [Constraint([1,1], ConstraintType.greater_equal, 3),
         Constraint([1,-1], ConstraintType.smaller_equal, 1)],
        [RestrictionType.free, RestrictionType.non_negative]),
    "optimal")

# 3E — 3 variables, middle one is free
run_test("3E: 3 vars, middle one free",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 2.0, 1.0]),
        [Constraint([1,1,0], ConstraintType.smaller_equal, 5),
         Constraint([0,1,1], ConstraintType.smaller_equal, 5),
         Constraint([1,0,1], ConstraintType.smaller_equal, 5)],
        [RestrictionType.non_negative, RestrictionType.free, RestrictionType.non_negative]),
    "optimal")


# ════════════════════════════════════════════════════════
print("\n══════════ GROUP 4: DEGENERACY EDGE CASES ══════════")
# ════════════════════════════════════════════════════════

# 4A — Classic degeneracy (ratio test tie)
run_test("4A: Degenerate ratio test tie",
    LPProblem(ObjectiveFunctionType.max, np.array([3.0, 2.0]),
        [Constraint([1,1], ConstraintType.smaller_equal, 4),
         Constraint([1,0], ConstraintType.smaller_equal, 4),
         Constraint([0,1], ConstraintType.smaller_equal, 4)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=12.0)

# 4B — Degenerate Phase 1 (artificial stuck at zero)
run_test("4B: Degenerate Phase 1",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.greater_equal, 2),
         Constraint([1,0], ConstraintType.smaller_equal, 2),
         Constraint([0,1], ConstraintType.smaller_equal, 2)],
        [RestrictionType.non_negative]*2),
    "optimal")

# 4C — Redundant constraint
run_test("4C: Redundant constraint",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.smaller_equal, 10),
         Constraint([1,1], ConstraintType.smaller_equal, 10),
         Constraint([1,0], ConstraintType.smaller_equal, 6)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=10.0)


# ════════════════════════════════════════════════════════
print("\n══════════ GROUP 5: HARD COMBINED CASES ══════════")
# ════════════════════════════════════════════════════════

# 5A — 4 variables, mixed constraints, one free
run_test("5A: 4 vars, mixed constraints, one free",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 2.0, 3.0, 1.0]),
        [Constraint([1,1,1,1], ConstraintType.smaller_equal, 40),
         Constraint([2,1,1,0], ConstraintType.greater_equal, 10),
         Constraint([0,1,2,1], ConstraintType.equal, 20)],
        [RestrictionType.non_negative, RestrictionType.free,
         RestrictionType.non_negative, RestrictionType.non_negative]),
    "optimal")

# 5B — Classic transportation-style problem
run_test("5B: 3 vars, 3 constraints, minimize",
    LPProblem(ObjectiveFunctionType.min, np.array([1.0, 2.0, 3.0]),
        [Constraint([1,1,0], ConstraintType.greater_equal, 3),
         Constraint([0,1,1], ConstraintType.greater_equal, 4),
         Constraint([1,0,1], ConstraintType.smaller_equal, 5)],
        [RestrictionType.non_negative]*3),
    "optimal")

# 5C — All >= minimize (classic Phase 1 stress test)
run_test("5C: All >= minimize (Phase 1 stress)",
    LPProblem(ObjectiveFunctionType.min, np.array([5.0, 4.0, 3.0]),
        [Constraint([6,4,2], ConstraintType.greater_equal, 240),
         Constraint([3,2,5], ConstraintType.greater_equal, 270),
         Constraint([5,6,5], ConstraintType.greater_equal, 420),
         Constraint([8,2,4], ConstraintType.greater_equal, 350)],
        [RestrictionType.non_negative]*3),
    "optimal")

# 5D — Free variable + equality + >= combined
run_test("5D: Free var + equality + >= ",
    LPProblem(ObjectiveFunctionType.min, np.array([2.0, 1.0, 3.0]),
        [Constraint([1,1,1], ConstraintType.equal, 6),
         Constraint([2,1,0], ConstraintType.greater_equal, 4),
         Constraint([0,1,2], ConstraintType.smaller_equal, 8)],
        [RestrictionType.free, RestrictionType.non_negative, RestrictionType.non_negative]),
    "optimal")

# 5E — Fractional optimal solution
run_test("5E: Fractional optimal solution",
    LPProblem(ObjectiveFunctionType.max, np.array([3.0, 5.0]),
        [Constraint([1,0], ConstraintType.smaller_equal, 4),
         Constraint([0,2], ConstraintType.smaller_equal, 12),
         Constraint([3,2], ConstraintType.smaller_equal, 18)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=36.0, expected_vars=[2.0, 6.0])

# 5F — Negative RHS handled via >= (multiply both sides by -1 is done by user)
run_test("5F: Problem with zero RHS constraint",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.smaller_equal, 5),
         Constraint([1,-1], ConstraintType.smaller_equal, 0)],
        [RestrictionType.non_negative]*2),
    "optimal", expected_obj=5.0)

# 5G — 5 variable problem
run_test("5G: 5-variable problem",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0, 1.0, 1.0, 1.0]),
        [Constraint([1,0,0,0,1], ConstraintType.smaller_equal, 5),
         Constraint([0,1,0,1,0], ConstraintType.smaller_equal, 5),
         Constraint([0,0,1,0,0], ConstraintType.smaller_equal, 5),
         Constraint([1,1,1,1,1], ConstraintType.smaller_equal, 10)],
        [RestrictionType.non_negative]*5),
    "optimal", expected_obj=10.0)

# 5H — Infeasible with >= and = mixed
run_test("5H: Infeasible mixed >= and =",
    LPProblem(ObjectiveFunctionType.max, np.array([1.0, 1.0]),
        [Constraint([1,1], ConstraintType.equal, 5),
         Constraint([1,0], ConstraintType.greater_equal, 6)],
        [RestrictionType.non_negative]*2),
    "infeasible")


# ════════════════════════════════════════════════════════
print("\n══════════════════════════════════════════════════════")
print(f"  RESULTS: {PASS} passed, {FAIL} failed out of {PASS+FAIL} tests")
print("══════════════════════════════════════════════════════\n")