# Stability Analysis: Gradient Descent vs Newton's Method

## Overview

This document analyzes the stability behavior of Gradient Descent (GD) and Newton's
Method when initialized far from the optimum, as required by Assignment 3 (Section 3 —
Stability Analysis). Both algorithms were tested from three distant starting points:
`[10.0, 10.0]`, `[-10.0, -10.0]`, and `[5.0, -5.0]`.

---

## 1. Why Newton's Method Can Be Vulnerable to Divergence

### 1.1 The Update Rule

Newton's damped update is:

```
X = a - α * H⁻¹ * J
```

Where:
- `J` is the Jacobian (gradient vector, shape 2×1)
- `H` is the Hessian (matrix of second derivatives, shape 2×2)
- `α` is the damping factor (learning rate)

The key insight is that the step size is **scaled by the inverse Hessian**. This means
Newton automatically adjusts its step based on the local curvature of the loss surface.
Near the optimum, this is extremely powerful — it produces large, confident steps in
flat directions and small, careful steps in curved ones.

### 1.2 The Problem Far from the Optimum

When the initial guess is far from the optimum, two problems arise:

**Problem 1 — Quadratic approximation breaks down.**
Newton's method is derived from a second-order Taylor expansion of the loss function:

```
L(a + Δa) ≈ L(a) + J·Δa + (1/2)·Δa^T·H·Δa
```

This approximation is only accurate in a small neighborhood around the current point.
Far from the optimum, the true loss surface may curve differently than the local
quadratic model predicts, causing the computed step to overshoot the minimum.

**Problem 2 — H⁻¹ amplifies large gradients.**
If the Jacobian `J` is large (as it will be far from the optimum), multiplying by `H⁻¹`
can produce a very large step `H⁻¹·J`, pushing the parameters even further away.
Without damping (`α = 1.0`), this can cause immediate divergence. With damping
(`α < 1.0`), the risk is reduced but not eliminated.

**Problem 3 — Ill-conditioning of the Hessian.**
In some problem geometries, the Hessian far from the optimum may be nearly singular
(determinant close to zero), making its inverse numerically unstable and producing
erratic, very large steps.

---

## 2. Why Gradient Descent Is More Stable

### 2.1 The Update Rule

GD uses only first-order information:

```
a[k+1] = a[k] - α * J
```

The step size is directly proportional to the gradient magnitude, scaled by `α`.
There is no matrix inversion, no curvature scaling, and no quadratic approximation.

### 2.2 Conservative Steps by Design

Because GD multiplies the raw gradient by a fixed small scalar `α`, its steps are
inherently bounded. Even from a far starting point where `‖J‖` is large, the
update `α * J` grows only linearly with the gradient. As long as `α` is chosen
small enough (i.e., `α < 2 / λ_max`, where `λ_max` is the largest eigenvalue of `H`),
GD is **globally convergent** for convex loss functions.

This means GD degrades gracefully: it may take many more iterations from a distant
starting point, but it will reliably converge without special handling.

---

## 3. Experimental Results

All three far starting points were tested with `α = 0.1` and `max_iter = 10000` for GD
and `max_iter = 1000` for Newton.

| Starting Point   | GD Status   | GD Iters | Newton Status | Newton Iters |
|------------------|-------------|----------|---------------|--------------|
| [10.0,  10.0]    | converged   | 136      | converged     | 136          |
| [-10.0, -10.0]   | converged   | 136      | converged     | 136          |
| [5.0,  -5.0]     | converged   | 130      | converged     | 130          |

### 3.1 Observation

In this specific experiment, both algorithms converged from all three starting points
and required the same number of iterations. This outcome is explained by the nature of
the loss function.

### 3.2 Why Both Converged Equally Here

The loss function for linear regression is a **strictly convex quadratic**:

```
L(a0, a1) = (1/2n) * Σ(y - (a0 + a1*x))²
```

For a quadratic loss, the Hessian `H` is **constant** — it does not depend on the
current parameter values `(a0, a1)`. This means:

- The quadratic approximation used by Newton is **exact everywhere**, not just locally.
- `H⁻¹·J` always points directly toward the global optimum.
- The step direction computed by Newton is always correct, regardless of starting point.

Because `H` is constant, the damped Newton step `a - α·H⁻¹·J` is mathematically
equivalent to a preconditioned gradient descent step. With `α = 0.1`, both methods
effectively take the same trajectory scaled by the same factor, which is why the
iteration counts are identical.

### 3.3 When Newton Would Actually Diverge

Newton's vulnerability becomes real in the following scenarios, which do not apply to
this assignment's quadratic loss but are important to understand:

| Scenario | Effect on Newton |
|----------|-----------------|
| Non-quadratic loss (e.g., logistic regression, neural networks) | Hessian changes with position; quadratic approximation fails far from optimum |
| Saddle points or negative curvature regions | H is indefinite; H⁻¹·J points uphill instead of downhill |
| Near-singular Hessian | H⁻¹ is numerically unstable; steps become arbitrarily large |
| Full Newton step (α = 1.0) on non-convex loss | No damping to prevent overshoot |

---

## 4. Conclusion

| Property | Gradient Descent | Newton's Method |
|----------|-----------------|-----------------|
| Information used | First-order (gradient only) | Second-order (gradient + curvature) |
| Step size control | Fixed scalar α | Curvature-scaled via H⁻¹ |
| Global stability (convex) | ✅ Guaranteed for small α | ✅ Guaranteed for quadratic loss |
| Global stability (non-convex) | More robust | Can diverge |
| Convergence speed (quadratic) | Slower | Same as GD (H is constant) |
| Convergence speed (general) | Slower | Faster (fewer iterations) |
| Risk from far starting point | Low | Higher on non-quadratic losses |

**Summary:** Newton's method is theoretically more vulnerable to divergence from far
starting points because it relies on a local quadratic approximation that may be
inaccurate far from the optimum, and because the inverse Hessian can amplify large
gradients into overshooting steps. However, for the strictly convex quadratic loss used
in this assignment, the Hessian is constant and exact everywhere, so both algorithms
converge equally from any starting point. The stability risk of Newton's method is
most relevant in non-quadratic, non-convex optimization problems encountered in more
advanced machine learning settings.

---
