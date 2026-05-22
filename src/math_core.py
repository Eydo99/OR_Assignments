# math_core.py
import numpy as np


def compute_loss(a, x, y):
    """L = 0.5 * sum((y - (a0 + a1*x))^2)"""
    n=len(y)
    a0, a1 = a[0], a[1]
    residuals = y - (a0 + a1 * x)
    return 0.5 * np.sum(residuals ** 2)/n


def compute_jacobian(a, x, y):
    """
    Gradient of L w.r.t. [a0, a1].
    dL/da0 = -sum(y - (a0 + a1*x))
    dL/da1 = -sum(x * (y - (a0 + a1*x)))
    Returns shape (2,)
    """
    a0, a1 = a[0], a[1]
    residuals = y - (a0 + a1 * x)
    n = len(x)
    dL_da0 = -np.sum(residuals) / n
    dL_da1 = -np.sum(x * residuals) / n
    return np.array([dL_da0, dL_da1])


def compute_hessian(x):
    """
    Hessian of L w.r.t. [a0, a1].
    H = [[n,      sum(x)  ],
         [sum(x), sum(x^2)]]
    Constant because loss is quadratic in a0, a1.
    Returns shape (2, 2)
    """
    n = len(x)
    H = np.array([
        [1.0,      np.mean(x)],
        [np.mean(x),  np.mean(x ** 2)]
    ], dtype=float)
    return H


def gradient_norm(a, x, y):
    """‖J‖ — used as secondary convergence indicator."""
    return np.linalg.norm(compute_jacobian(a, x, y))


def denormalize_params(a, x_mean, x_std, y_mean, y_std):
    """
    Convert normalized (a0_n, a1_n) back to original scale.
    f_norm = a0_n + a1_n * x_norm
    x_norm = (x - x_mean) / x_std
    y_norm = (y - y_mean) / y_std

    => y = y_std * f_norm + y_mean
         = y_std*(a0_n + a1_n*(x-x_mean)/x_std) + y_mean
         = (y_std*a0_n - y_std*a1_n*x_mean/x_std + y_mean)
           + (y_std*a1_n/x_std)*x

    So:
        a1_orig = a1_n * y_std / x_std
        a0_orig = a0_n * y_std + y_mean - a1_orig * x_mean
    """
    a0_n, a1_n = a[0], a[1]
    a1_orig = a1_n * y_std / x_std
    a0_orig = a0_n * y_std + y_mean - a1_orig * x_mean
    return np.array([a0_orig, a1_orig])