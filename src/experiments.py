# experiments.py
import time
import numpy as np
from src.data_loader import load_and_clean_data, normalization
from src.gradient_descent import gradient_descent_loop
from src.newton import newton_loop
from src.math_core import compute_loss, denormalize_params

# ── shared settings ────────────────────────────────────────────────────────────
A0_INIT      = [0.0, 0.0]
TOLERANCE    = 1e-6
MAX_ITER_GD  = 10000
MAX_ITER_N   = 1000

ALPHA_TOO_SMALL = 0.001
ALPHA_GOOD      = 0.1
ALPHA_TOO_LARGE = 1.5

# starting points far from optimum — for Newton stability analysis
FAR_STARTS = [
    [10.0,  10.0],
    [-10.0, -10.0],
    [5.0,  -5.0],
]


def _sep(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def _print_iter_log(history, max_rows=10):
    """Print iteration table (loss + grad_norm), capped at max_rows."""
    losses = history['loss']
    gnorms = history['grad_norm']
    total  = len(losses)
    step   = max(1, total // max_rows)
    print(f"  {'Iter':>6}  {'Loss':>18}  {'‖∇L‖':>14}")
    print(f"  {'-'*6}  {'-'*18}  {'-'*14}")
    for i in range(0, total, step):
        print(f"  {i:>6}  {losses[i]:>18.6f}  {gnorms[i]:>14.6f}")
    if (total - 1) % step != 0:
        print(f"  {total-1:>6}  {losses[-1]:>18.6f}  {gnorms[-1]:>14.6f}")


def load_data(file_path='data/AmesHousing.csv'):
    x, y = load_and_clean_data(file_path)
    x_n, y_n, x_mean, x_std, y_mean, y_std = normalization(x, y)
    stats = (x_mean, x_std, y_mean, y_std)
    return x_n, y_n, stats, len(x)


def _predict_samples(a_orig, x_raw, y_raw, n=5):
    """Print predicted vs actual for n sample houses (original scale)."""
    print(f"\n  {'Sample':>6}  {'GrLivArea':>10}  {'Actual $':>12}  {'Predicted $':>12}")
    print(f"  {'-'*6}  {'-'*10}  {'-'*12}  {'-'*12}")
    indices = np.linspace(0, len(x_raw) - 1, n, dtype=int)
    for i in indices:
        pred = a_orig[0] + a_orig[1] * x_raw[i]
        print(f"  {i:>6}  {x_raw[i]:>10.0f}  {y_raw[i]:>12.0f}  {pred:>12.0f}")


# ── Experiment 1: GD vs Newton convergence + timing ───────────────────────────
def experiment_convergence(x, y, stats, x_raw, y_raw, alpha=ALPHA_GOOD):
    _sep(f"EXPERIMENT 1 — GD vs Newton Convergence  (α={alpha})")

    # --- Gradient Descent ---
    t0 = time.time()
    a_gd, hist_gd, iters_gd, status_gd = gradient_descent_loop(
        A0_INIT, alpha, x, y, MAX_ITER_GD, TOLERANCE)
    t_gd = time.time() - t0

    # --- Newton ---
    t0 = time.time()
    a_nt, hist_nt, iters_nt, status_nt = newton_loop(
        A0_INIT, alpha, x, y, MAX_ITER_N, TOLERANCE)
    t_nt = time.time() - t0

    # denormalize
    a_gd_orig = denormalize_params(a_gd, *stats)
    a_nt_orig = denormalize_params(a_nt, *stats)

    print(f"\n  {'Algorithm':<20} {'Status':<12} {'Iters':>7} "
          f"{'Time(s)':>10} {'Final Loss':>14}  a0_orig        a1_orig")
    print(f"  {'-'*20} {'-'*12} {'-'*7} {'-'*10} {'-'*14}  {'-'*13}  {'-'*13}")

    for label, a_o, hist, iters, status, t in [
        ("Gradient Descent",  a_gd_orig, hist_gd, iters_gd, status_gd, t_gd),
        ("Newton's Method",   a_nt_orig, hist_nt, iters_nt, status_nt, t_nt),
    ]:
        print(f"  {label:<20} {status:<12} {iters:>7} "
              f"{t:>10.4f} {hist['loss'][-1]:>14.6f}  "
              f"{a_o[0]:>13.4f}  {a_o[1]:>13.4f}")

    print("\n  — GD iteration log —")
    _print_iter_log(hist_gd)
    print("\n  — Newton iteration log —")
    _print_iter_log(hist_nt)

    print("\n  — Predicted vs Actual (GD model, original scale) —")
    _predict_samples(a_gd_orig, x_raw, y_raw)

    speedup = iters_gd / iters_nt if iters_nt > 0 else float('inf')
    print(f"\n  Newton speed-up: {speedup:.1f}x fewer iterations")
    print(f"  GD wall-clock / Newton wall-clock: "
          f"{t_gd/t_nt:.1f}x" if t_nt > 0 else "  N/A")

    return {
        'gd': {'a': a_gd, 'a_orig': a_gd_orig, 'history': hist_gd,
               'iters': iters_gd, 'time': t_gd, 'status': status_gd},
        'nt': {'a': a_nt, 'a_orig': a_nt_orig, 'history': hist_nt,
               'iters': iters_nt, 'time': t_nt, 'status': status_nt},
    }


# ── Experiment 2: α sensitivity on GD ────────────────────────────────────────
def experiment_alpha_sensitivity(x, y, stats):
    _sep("EXPERIMENT 2 — α Sensitivity on Gradient Descent")

    configs = [
        ("too small",  ALPHA_TOO_SMALL),
        ("good",       ALPHA_GOOD),
        ("too large",  ALPHA_TOO_LARGE),
    ]

    print(f"\n  {'α':<8} {'Label':<12} {'Status':<12} "
          f"{'Iters':>7} {'Final Loss':>16}  Behavior")
    print(f"  {'-'*8} {'-'*12} {'-'*12} {'-'*7} {'-'*16}  {'-'*30}")

    results = {}
    for label, alpha in configs:
        try:
            t0 = time.time()
            a, hist, iters, status = gradient_descent_loop(
                A0_INIT, alpha, x, y, MAX_ITER_GD, TOLERANCE)
            elapsed = time.time() - t0
            final_loss = hist['loss'][-1]

            if status == 'diverged':
                behavior = "DIVERGED — α too large, overshooting"
            elif status == 'max_iter':
                behavior = "Hit max_iter — α too small, very slow"
            else:
                behavior = "Converged normally"

            print(f"  {alpha:<8} {label:<12} {status:<12} "
                  f"{iters:>7} {final_loss:>16.4f}  {behavior}")

            results[label] = {
                'alpha': alpha, 'a': a, 'history': hist,
                'iters': iters, 'status': status, 'time': elapsed
            }
        except Exception as e:
            print(f"  {alpha:<8} {label:<12} ERROR: {e}")
            results[label] = {'alpha': alpha, 'error': str(e)}

    # iteration log for the good alpha only
    if 'good' in results and 'history' in results['good']:
        print("\n  — Iteration log for α=good —")
        _print_iter_log(results['good']['history'])

    return results


# ── Experiment 3: Newton curvature advantage ──────────────────────────────────
def experiment_newton_curvature(x, y, alpha=ALPHA_GOOD):
    _sep(f"EXPERIMENT 3 — Newton Faster via Curvature  (α={alpha})")

    _, hist_gd, iters_gd, _ = gradient_descent_loop(
        A0_INIT, alpha, x, y, MAX_ITER_GD, TOLERANCE)
    _, hist_nt, iters_nt, _ = newton_loop(
        A0_INIT, alpha, x, y, MAX_ITER_N, TOLERANCE)

    speedup = iters_gd / iters_nt if iters_nt > 0 else float('inf')

    print(f"\n  GD  iterations : {iters_gd}")
    print(f"  Newton iters   : {iters_nt}")
    print(f"  Speed-up       : {speedup:.1f}x")
    print(f"\n  Why: Newton uses the Hessian (curvature) to scale each step,")
    print(f"  landing near the optimum in very few iterations even for this")
    print(f"  quadratic loss, while GD takes many small fixed-scale steps.")

    return {'gd_iters': iters_gd, 'nt_iters': iters_nt, 'speedup': speedup}


# ── Experiment 4: Newton stability — far starting points ─────────────────────
def experiment_newton_stability(x, y, stats):
    _sep("EXPERIMENT 4 — Newton Stability Analysis (Far Starting Points)")

    print(f"\n  {'Start (a0,a1)':<20} {'GD Status':<12} {'GD Iters':>9} "
          f"{'NT Status':<12} {'NT Iters':>9}")
    print(f"  {'-'*20} {'-'*12} {'-'*9} {'-'*12} {'-'*9}")

    results = []
    for start in FAR_STARTS:
        _, _, iters_gd, status_gd = gradient_descent_loop(
            start, ALPHA_GOOD, x, y, MAX_ITER_GD, TOLERANCE)
        _, _, iters_nt, status_nt = newton_loop(
            start, ALPHA_GOOD, x, y, MAX_ITER_N, TOLERANCE)

        label = f"[{start[0]}, {start[1]}]"
        print(f"  {label:<20} {status_gd:<12} {iters_gd:>9} "
              f"{status_nt:<12} {iters_nt:>9}")
        results.append({
            'start': start,
            'gd': {'iters': iters_gd, 'status': status_gd},
            'nt': {'iters': iters_nt, 'status': status_nt},
        })

    print(f"\n  Stability note:")
    print(f"  Newton's damped update (alpha * H^-1 * J) scales steps by")
    print(f"  curvature. Far from the optimum, the quadratic approximation")
    print(f"  may be poor, causing large steps and potential divergence.")
    print(f"  GD takes conservative fixed-scale steps so it degrades")
    print(f"  gracefully — slower but safer from any starting point.")

    return results


# ── runner ────────────────────────────────────────────────────────────────────
def run_all(file_path='data/AmesHousing.csv'):
    x, y, stats, n = load_data(file_path)
    x_raw, y_raw   = load_and_clean_data(file_path)   # original scale for display
    print(f"\nData loaded & normalized  |  n={n} samples")

    r1 = experiment_convergence(x, y, stats, x_raw, y_raw)
    r2 = experiment_alpha_sensitivity(x, y, stats)
    r3 = experiment_newton_curvature(x, y)
    r4 = experiment_newton_stability(x, y, stats)

    _sep("SUMMARY")
    print(f"  GD  iters (α=good)  : {r1['gd']['iters']}")
    print(f"  NT  iters (α=good)  : {r1['nt']['iters']}")
    print(f"  GD  time  (s)       : {r1['gd']['time']:.4f}")
    print(f"  NT  time  (s)       : {r1['nt']['time']:.4f}")
    print(f"  GD  a0 (orig scale) : {r1['gd']['a_orig'][0]:.2f}")
    print(f"  GD  a1 (orig scale) : {r1['gd']['a_orig'][1]:.2f}")
    print(f"  NT  a0 (orig scale) : {r1['nt']['a_orig'][0]:.2f}")
    print(f"  NT  a1 (orig scale) : {r1['nt']['a_orig'][1]:.2f}")
    print()

    return {'convergence': r1, 'alpha_sensitivity': r2,
            'curvature': r3, 'stability': r4}


if __name__ == '__main__':
    run_all()