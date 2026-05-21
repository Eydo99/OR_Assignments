# newton.py
import numpy as np
from src.math_core import compute_jacobian, compute_hessian, compute_loss, gradient_norm

DIVERGENCE_THRESHOLD = 1e15


def inverse(H):
    """
    Analytical 2x2 matrix inverse.
    H = [[a, b], [c, d]]
    H_inv = (1/det) * [[d, -b], [-c, a]]
    """
    a, b = H[0, 0], H[0, 1]
    c, d = H[1, 0], H[1, 1]

    det = a * d - b * c
    if abs(det) < 1e-12:
        raise ValueError("Hessian is singular — cannot invert.")

    H_inv = (1.0 / det) * np.array([
        [ d, -b],
        [-c,  a]
    ], dtype=float)
    return H_inv


def newton_step(a, alpha, x, y):
    """Single damped Newton update: a_new = a - alpha * H^{-1} @ J"""
    J     = compute_jacobian(a, x, y)
    H     = compute_hessian(x)
    H_inv = inverse(H)
    return a - alpha * (H_inv @ J)


def newton_loop(a0_init, alpha, x, y,
                max_iterations=1000, tolerance=1e-6):
    """
    Damped Newton's Method.
    X = a - alpha * H^{-1} * J

    Stopping criteria:
      - weight change  ‖a_new - a‖ < tolerance
      - gradient norm  ‖J‖         < tolerance
      - divergence     loss > DIVERGENCE_THRESHOLD

    Returns:
        a_final   : final parameters (2,)
        history   : dict — loss, a0, a1, grad_norm per iteration
        iterations: steps taken
        status    : 'converged' | 'max_iter' | 'diverged'
    """
    a = np.array(a0_init, dtype=float)

    history = {'loss': [], 'a0': [], 'a1': [], 'grad_norm': []}

    status = 'max_iter'

    for i in range(max_iterations):
        loss  = compute_loss(a, x, y)
        J     = compute_jacobian(a, x, y)
        gnorm = np.linalg.norm(J)

        history['loss'].append(loss)
        history['a0'].append(a[0])
        history['a1'].append(a[1])
        history['grad_norm'].append(gnorm)

        # divergence guard
        if loss > DIVERGENCE_THRESHOLD or np.isnan(loss) or np.isinf(loss):
            status = 'diverged'
            break

        a_new = newton_step(a, alpha, x, y)

        weight_change = np.linalg.norm(a_new - a)

        if weight_change < tolerance or gnorm < tolerance:
            a = a_new
            history['loss'].append(compute_loss(a, x, y))
            history['a0'].append(a[0])
            history['a1'].append(a[1])
            history['grad_norm'].append(gradient_norm(a, x, y))
            status = 'converged'
            return a, history, i + 1, status

        a = a_new

    return a, history, len(history['loss']), status