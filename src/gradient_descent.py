# gradient_descent.py
import numpy as np
from src.math_core import compute_jacobian, compute_loss, gradient_norm

DIVERGENCE_THRESHOLD = 1e15


def gradient_descent_loop(a0_init, alpha, x, y,
                           max_iterations=10000, tolerance=1e-6):
    """
    Multi-variable Gradient Descent.
    a[k+1] = a[k] - alpha * J(a[k])

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

        a_new = a - alpha * J

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