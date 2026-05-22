# visualize.py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ── color palette (matches the dark theme from the lab board) ─────────────────
GD_COLOR     = '#7C6FCD'   # purple  — Person 1 / GD
NT_COLOR     = '#2E8B6E'   # teal    — Person 2 / Newton
SMALL_COLOR  = '#E07B39'   # orange  — α too small
GOOD_COLOR   = '#7C6FCD'   # purple  — α good
LARGE_COLOR  = '#C0392B'   # red     — α too large
BG           = '#1A1A2E'
PANEL        = '#16213E'
TEXT         = '#E0E0E0'
GRID         = '#2A2A4A'

plt.rcParams.update({
    'figure.facecolor':  BG,
    'axes.facecolor':    PANEL,
    'axes.edgecolor':    GRID,
    'axes.labelcolor':   TEXT,
    'axes.titlecolor':   TEXT,
    'xtick.color':       TEXT,
    'ytick.color':       TEXT,
    'grid.color':        GRID,
    'grid.linestyle':    '--',
    'grid.alpha':        0.5,
    'text.color':        TEXT,
    'legend.facecolor':  PANEL,
    'legend.edgecolor':  GRID,
    'font.family':       'monospace',
})


# ── helper ────────────────────────────────────────────────────────────────────
def _trim(history, max_pts=500):
    """Downsample history to at most max_pts points for clean plots."""
    losses    = np.array(history['loss'])
    a0s       = np.array(history['a0'])
    a1s       = np.array(history['a1'])
    gnorms    = np.array(history['grad_norm'])
    n         = len(losses)
    if n <= max_pts:
        idx = np.arange(n)
    else:
        idx = np.unique(np.linspace(0, n - 1, max_pts, dtype=int))
    return idx, losses[idx], a0s[idx], a1s[idx], gnorms[idx]


# ══════════════════════════════════════════════════════════════════════════════
# Plot 1 — Loss curves: GD vs Newton
# ══════════════════════════════════════════════════════════════════════════════
def plot_loss_curves(hist_gd, hist_nt, save_path='results/plot1_loss_curves.png'):
    """
    Loss vs iteration for GD and Newton on the same axes.
    Uses log scale on y-axis to show convergence detail.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Plot 1 — Loss Convergence: GD vs Newton', fontsize=14, y=1.02)

    idx_gd, loss_gd, *_ = _trim(hist_gd)
    idx_nt, loss_nt, *_ = _trim(hist_nt)

    # ── left: linear scale ────────────────────────────────────────────────────
    ax = axes[0]
    ax.plot(idx_gd, loss_gd, color=GD_COLOR, lw=1.8, label=f'GD  ({len(hist_gd["loss"])} iters)')
    ax.plot(idx_nt, loss_nt, color=NT_COLOR,  lw=1.8, label=f'Newton ({len(hist_nt["loss"])} iters)', linestyle='--')
    ax.set_title('Linear Scale')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Loss  L')
    ax.legend()
    ax.grid(True)

    # ── right: log scale ─────────────────────────────────────────────────────
    ax = axes[1]
    ax.semilogy(idx_gd, loss_gd, color=GD_COLOR, lw=1.8, label='GD')
    ax.semilogy(idx_nt, loss_nt, color=NT_COLOR,  lw=1.8, label='Newton', linestyle='--')
    ax.set_title('Log Scale  (shows convergence rate)')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Loss  L  (log)')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'  Saved → {save_path}')


# ══════════════════════════════════════════════════════════════════════════════
# Plot 2 — Weight paths: a0 and a1 vs iteration
# ══════════════════════════════════════════════════════════════════════════════
def plot_weight_paths(hist_gd, hist_nt, save_path='results/plot2_weight_paths.png'):
    """
    Two sub-plots: a0 vs iteration and a1 vs iteration for both algorithms.
    Also includes a 2-D weight-space trajectory (a0 vs a1).
    """
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Plot 2 — Weight Values at Each Step: GD vs Newton', fontsize=14)
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

    idx_gd, _, a0_gd, a1_gd, _ = _trim(hist_gd)
    idx_nt, _, a0_nt, a1_nt, _ = _trim(hist_nt)

    # ── a0 vs iteration ───────────────────────────────────────────────────────
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(idx_gd, a0_gd, color=GD_COLOR, lw=1.8, label='GD')
    ax.plot(idx_nt, a0_nt, color=NT_COLOR,  lw=1.8, label='Newton', linestyle='--')
    ax.axhline(a0_gd[-1], color=GD_COLOR, lw=0.6, alpha=0.4, linestyle=':')
    ax.set_title('a₀  (intercept)  vs Iteration')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('a₀')
    ax.legend()
    ax.grid(True)

    # ── a1 vs iteration ───────────────────────────────────────────────────────
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(idx_gd, a1_gd, color=GD_COLOR, lw=1.8, label='GD')
    ax.plot(idx_nt, a1_nt, color=NT_COLOR,  lw=1.8, label='Newton', linestyle='--')
    ax.axhline(a1_gd[-1], color=GD_COLOR, lw=0.6, alpha=0.4, linestyle=':')
    ax.set_title('a₁  (slope)  vs Iteration')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('a₁')
    ax.legend()
    ax.grid(True)

    # ── 2-D weight-space trajectory ───────────────────────────────────────────
    ax = fig.add_subplot(gs[1, :])

    # scatter with color-mapped iteration index
    sc_gd = ax.scatter(a0_gd, a1_gd,
                       c=idx_gd, cmap='Purples', s=6, alpha=0.7,
                       label='GD path', zorder=3)
    sc_nt = ax.scatter(a0_nt, a1_nt,
                       c=idx_nt, cmap='Greens',  s=18, alpha=0.9,
                       marker='D', label='Newton path', zorder=4)

    # mark start / end
    ax.plot(a0_gd[0],  a1_gd[0],  'o', color='white',   ms=8, zorder=5)
    ax.plot(a0_gd[-1], a1_gd[-1], '*', color=GD_COLOR,  ms=14, zorder=5, label='GD  end')
    ax.plot(a0_nt[-1], a1_nt[-1], '*', color=NT_COLOR,   ms=14, zorder=5, label='Newton end')

    plt.colorbar(sc_gd, ax=ax, label='GD iteration', pad=0.01)
    ax.set_title('Weight-Space Trajectory  (a₀ vs a₁)')
    ax.set_xlabel('a₀  (intercept, normalised)')
    ax.set_ylabel('a₁  (slope, normalised)')
    ax.legend(loc='upper left')
    ax.grid(True)

    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'  Saved → {save_path}')


# ══════════════════════════════════════════════════════════════════════════════
# Plot 3 — α sensitivity on GD
# ══════════════════════════════════════════════════════════════════════════════
def plot_alpha_sensitivity(results_alpha, save_path='results/plot3_alpha_sensitivity.png'):
    """
    Loss vs iteration for three α values: too small / good / too large.
    results_alpha is the dict returned by experiment_alpha_sensitivity().
    """
    configs = [
        ('too small',  SMALL_COLOR, '-'),
        ('good',       GOOD_COLOR,  '-'),
        ('too large',  LARGE_COLOR, '-'),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Plot 3 — α Sensitivity on Gradient Descent', fontsize=14)

    for label, color, ls in configs:
        r = results_alpha.get(label)
        if r is None or 'history' not in r:
            continue
        hist   = r['history']
        alpha  = r['alpha']
        status = r['status']
        losses = np.array(hist['loss'])
        n      = len(losses)
        idx    = np.unique(np.linspace(0, n - 1, min(500, n), dtype=int))

        leg = f'α={alpha}  [{label}]  {status}'

        # linear
        axes[0].plot(idx, losses[idx], color=color, lw=1.8, linestyle=ls, label=leg)
        # log (clip negatives / zeros for log)
        safe = np.clip(losses[idx], 1e-12, None)
        axes[1].semilogy(idx, safe, color=color, lw=1.8, linestyle=ls, label=leg)

    for ax, title in zip(axes, ['Linear Scale', 'Log Scale']):
        ax.set_title(title)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Loss  L')
        ax.legend(fontsize=8)
        ax.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'  Saved → {save_path}')


# ══════════════════════════════════════════════════════════════════════════════
# Plot 4 — Stability: GD vs Newton from far starting points
# ══════════════════════════════════════════════════════════════════════════════
def plot_stability(stability_results, save_path='results/plot4_stability.png'):
    """
    For each far starting point, plots the loss curve of GD and Newton
    side-by-side so it is visually clear when Newton diverges.
    stability_results is the list returned by experiment_newton_stability().
    """
    n_starts = len(stability_results)
    fig, axes = plt.subplots(n_starts, 2, figsize=(14, 4 * n_starts))
    fig.suptitle('Plot 4 — Stability Analysis: GD vs Newton from Far Starting Points',
                 fontsize=13, y=1.01)

    if n_starts == 1:
        axes = [axes]   # keep indexing consistent

    for row, res in enumerate(stability_results):
        start  = res['start']
        title  = f'Start = {start}'

        for col, (key, color, label) in enumerate([
            ('gd', GD_COLOR, 'GD'),
            ('nt', NT_COLOR, 'Newton'),
        ]):
            ax     = axes[row][col]
            hist   = res[key].get('history')
            status = res[key]['status']
            iters  = res[key]['iters']

            if hist is None or len(hist.get('loss', [])) == 0:
                ax.text(0.5, 0.5, f'{label}\nNo history', ha='center',
                        va='center', transform=ax.transAxes, color=TEXT)
            else:
                losses = np.array(hist['loss'])
                n      = len(losses)
                idx    = np.unique(np.linspace(0, n - 1, min(300, n), dtype=int))
                safe   = np.clip(losses[idx], 1e-12, None)
                ax.semilogy(idx, safe, color=color, lw=1.8)
                ax.set_title(f'{title}  |  {label}  ({status}, {iters} iters)')

            ax.set_xlabel('Iteration')
            ax.set_ylabel('Loss (log)')
            ax.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'  Saved → {save_path}')


# ══════════════════════════════════════════════════════════════════════════════
# Plot 5 — Gradient norm convergence
# ══════════════════════════════════════════════════════════════════════════════
def plot_gradient_norms(hist_gd, hist_nt, save_path='results/plot5_gradient_norms.png'):
    """‖∇L‖ vs iteration — shows how quickly the gradient vanishes."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle('Plot 5 — Gradient Norm ‖∇L‖ vs Iteration', fontsize=14)

    idx_gd, _, _, _, gn_gd = _trim(hist_gd)
    idx_nt, _, _, _, gn_nt = _trim(hist_nt)

    ax.semilogy(idx_gd, np.clip(gn_gd, 1e-12, None),
                color=GD_COLOR, lw=1.8, label=f'GD  ({len(hist_gd["loss"])} iters)')
    ax.semilogy(idx_nt, np.clip(gn_nt, 1e-12, None),
                color=NT_COLOR,  lw=1.8, label=f'Newton ({len(hist_nt["loss"])} iters)',
                linestyle='--')

    ax.set_xlabel('Iteration')
    ax.set_ylabel('‖∇L‖  (log scale)')
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'  Saved → {save_path}')


# ══════════════════════════════════════════════════════════════════════════════
# Master runner — call this from experiments.py
# ══════════════════════════════════════════════════════════════════════════════
def generate_all_plots(results):
    """
    results is the dict returned by experiments.run_all():
        {
          'convergence':       r1,   # keys: gd, nt  (each has 'history')
          'alpha_sensitivity': r2,   # keys: 'too small', 'good', 'too large'
          'curvature':         r3,
          'stability':         r4,   # list of dicts with 'gd'/'nt' histories
        }
    """
    import os
    os.makedirs('results', exist_ok=True)

    print('\n  Generating plots...')

    r1 = results['convergence']
    plot_loss_curves(r1['gd']['history'], r1['nt']['history'])
    plot_weight_paths(r1['gd']['history'], r1['nt']['history'])
    plot_alpha_sensitivity(results['alpha_sensitivity'])
    plot_stability(results['stability'])
    plot_gradient_norms(r1['gd']['history'], r1['nt']['history'])

    print('  All plots saved to results/')
