import numpy as np
from src.math_core import compute_jacobian, compute_hessian


def inverse(H):
    # eyad part
    pass


def newton_step(a, alpha, x, y):
    #hany part
    J = compute_jacobian(a, x, y)
    H = compute_hessian(x)

    #eyad part
    H_inv = inverse(H)

    a_new = a - alpha * (H_inv @ J)

    return a_new


def newton_loop(a0, alpha, x, y, max_iterations, tolerance):
    a_current = np.array(a0, dtype=float)
    iterations = 0

    while iterations < max_iterations:
        a_old = a_current.copy()

        a_current = newton_step(a_old, alpha, x, y)

        weight_change = np.linalg.norm(a_current - a_old)

        if weight_change < tolerance:
            break

        iterations += 1

    return a_current, iterations