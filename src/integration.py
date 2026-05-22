import numpy as np
from src.data_loader import load_and_clean_data, normalization
from src.gradient_descent import gradient_descent_loop
from src.newton import newton_loop
from src.math_core import denormalize_params

A0_INIT    = [0.0, 0.0]
ALPHA      = 0.1
MAX_ITER_GD = 10000
MAX_ITER_N  = 1000
TOLERANCE  = 1e-6


def verify_convergence(file_path='data/AmesHousing.csv'):
    """
    Runs both GD and Newton on the same data and asserts
    they reach the same final (a0, a1) within tolerance.
    """
    x, y = load_and_clean_data(file_path)
    x_n, y_n, x_mean, x_std, y_mean, y_std = normalization(x, y)
    stats = (x_mean, x_std, y_mean, y_std)

    a_gd, _, iters_gd, status_gd = gradient_descent_loop(
        A0_INIT, ALPHA, x_n, y_n, MAX_ITER_GD, TOLERANCE)

    a_nt, _, iters_nt, status_nt = newton_loop(
        A0_INIT, ALPHA, x_n, y_n, MAX_ITER_N, TOLERANCE)

    a_gd_orig = denormalize_params(a_gd, *stats)
    a_nt_orig = denormalize_params(a_nt, *stats)

    diff = np.abs(a_gd_orig - a_nt_orig)
    match = np.all(diff < 1.0)   # $1 tolerance on original price scale

    print("\n" + "=" * 55)
    print("  VERIFICATION — GD vs Newton Final Parameters")
    print("=" * 55)
    print(f"  {'':20} {'a0':>12}  {'a1':>12}")
    print(f"  {'GD':20} {a_gd_orig[0]:>12.4f}  {a_gd_orig[1]:>12.4f}  ({status_gd}, {iters_gd} iters)")
    print(f"  {'Newton':20} {a_nt_orig[0]:>12.4f}  {a_nt_orig[1]:>12.4f}  ({status_nt}, {iters_nt} iters)")
    print(f"  {'Difference':20} {diff[0]:>12.6f}  {diff[1]:>12.6f}")
    print()

    if match:
        print("  ✅ PASSED — both algorithms converge to the same (a0, a1)")
    else:
        print("  ❌ FAILED — parameters differ beyond tolerance")
        print(f"     diff = {diff}")

    return match, a_gd_orig, a_nt_orig