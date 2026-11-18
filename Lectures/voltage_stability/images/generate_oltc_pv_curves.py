import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

out_dir = Path('Lectures/voltage_stability/images')
out_dir.mkdir(parents=True, exist_ok=True)


def nose_curve(x_max: float, n: int = 500):
    """Return (x_full, y_full) for a normalized P-V nose curve with peak x_max."""
    y_upper = np.linspace(1.0 / np.sqrt(2.0), 1.0, n)
    y_lower = np.linspace(0.0, 1.0 / np.sqrt(2.0), n)
    # y = sqrt(0.5 +/- sqrt(0.25 - (0.5 * x / x_max)^2))  =>  x / (2 * x_max) = y * sqrt(1 - y^2)
    x_upper = 2.0 * x_max * y_upper * np.sqrt(np.maximum(1.0 - y_upper**2, 0.0))
    x_lower = 2.0 * x_max * y_lower * np.sqrt(np.maximum(1.0 - y_lower**2, 0.0))
    return np.concatenate([x_upper[::-1], x_lower[::-1]]), np.concatenate([y_upper[::-1], y_lower[::-1]])


def intersect_z_load(k: float, x_max: float):
    """Intersection of load x = k * y^2 with upper branch of nose curve."""
    # From x = 2*x_max*y*sqrt(1-y^2) and x = k*y^2:
    # k^2 * y^2 = 4 * x_max^2 * (1 - y^2) => y^2 = 4*x_max^2 / (k^2 + 4*x_max^2)
    y = 2.0 * x_max / np.sqrt(k**2 + 4.0 * x_max**2)
    x = k * y**2
    return x, y


def plot_oltc_scenario(stable: bool, filename: str):
    fig, ax = plt.subplots(figsize=(5.8, 4.3), dpi=300)

    x_pre, y_pre = nose_curve(0.50)
    x_post, y_post = nose_curve(1.0 / 3.0)

    ax.plot(x_pre, y_pre, color='#1b4f72', linewidth=2.2, label='Pre-disturbance $P$-$V$ curve')
    ax.plot(x_post, y_post, color='#2874a6', linewidth=2.0, linestyle='--', label=r'Post-disturbance ($X_L \nearrow$)')

    # Arrow showing nose curve shift
    ax.annotate('', xy=(0.35, 0.707), xytext=(0.485, 0.707),
                arrowprops=dict(arrowstyle='->', color='#1b4f72', lw=1.8))
    ax.text(0.418, 0.735, r'$X_L \nearrow$', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1b4f72')

    y_grid = np.linspace(0.0, 1.02, 300)

    if stable:
        k_vals = [0.30, 0.34, 0.38]  # r decreases => k = G*X_L/r^2 increases
        stage_labels = ['0: Initial', '1: Post-trip', '2: Tap 1', '3: Restored']
        colors = ['#111111', '#d35400', '#27ae60', '#1e8449']
        styles = ['-', '-.', ':', '--']

        # Plot load curves
        for i, k in enumerate(k_vals):
            lbl = r'Load $P_R = G(V_R/r)^2$' if i == 0 else None
            ax.plot(k * y_grid**2, y_grid, color='#333333', linestyle=styles[i], linewidth=1.6, label=lbl)

        # Operating points: 0 on pre-disturbance, 1..3 on post-disturbance
        pts = [intersect_z_load(k_vals[0], 0.50)] + [intersect_z_load(k, 1.0 / 3.0) for k in k_vals]
        offsets = [(-0.075, 0.025), (-0.075, -0.055), (0.018, 0.02), (0.022, -0.03)]
        for idx, ((px, py), (dx, dy)) in enumerate(zip(pts, offsets)):
            ax.plot(px, py, 'o', color=colors[idx], markersize=6.5, zorder=6)
            ax.text(px + dx, py + dy, f'({idx})', fontsize=8.5, fontweight='bold', color=colors[idx])

        # Stage progression arrows
        for idx in range(len(pts) - 1):
            ax.annotate('', xy=pts[idx + 1], xytext=pts[idx],
                        arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.3, shrinkA=4, shrinkB=4))

        ax.set_title('Stable Case: OLTC Restores $P_R$ after Tap Changes', fontsize=10.5, fontweight='bold')
        ax.text(0.32, 0.24, 'Stages:\n(0) Pre-disturbance\n(1) Line trip ($V_R \\searrow$)\n(2)-(3) $r \\searrow$ restores $P_R$',
                fontsize=8.2, bbox=dict(boxstyle='round,pad=0.3', facecolor='#eafaf1', edgecolor='#27ae60', alpha=0.92))
    else:
        k_vals = [0.38, 0.48, 0.60, 0.76, 0.96]
        for i, k in enumerate(k_vals):
            lbl = r'Load $P_R = G(V_R/r)^2$' if i == 0 else None
            ls = '-' if i == 0 else '--'
            alpha = 1.0 if i == 0 else 0.75
            ax.plot(k * y_grid**2, y_grid, color='#333333', linestyle=ls, linewidth=1.4, alpha=alpha, label=lbl)

        pts = [intersect_z_load(k_vals[0], 0.50)] + [intersect_z_load(k, 1.0 / 3.0) for k in k_vals[:4]]
        pt_colors = ['#111111', '#d35400', '#c0392b', '#922b21', '#7b241c']
        offsets = [(-0.075, 0.025), (-0.065, 0.025), (0.015, 0.015), (0.015, -0.025), (0.015, -0.045)]
        for idx, ((px, py), (dx, dy)) in enumerate(zip(pts, offsets)):
            ax.plot(px, py, 'o', color=pt_colors[idx], markersize=6.0, zorder=6)
            ax.text(px + dx, py + dy, f'({idx})', fontsize=8.2, fontweight='bold', color=pt_colors[idx])

        for idx in range(len(pts) - 1):
            ax.annotate('', xy=pts[idx + 1], xytext=pts[idx],
                        arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.2, shrinkA=3, shrinkB=3))

        # Collapse arrow past last point
        ax.annotate('', xy=(0.12, 0.25), xytext=pts[-1],
                    arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.8, linestyle='--'))

        ax.set_title('Unstable Case: OLTC Tap Changes Drive Voltage Collapse', fontsize=10.5, fontweight='bold')
        ax.text(0.32, 0.24, 'Stages:\n(0) Pre-disturbance\n(1) Line trip ($V_R \\searrow$)\n(2)-(4) $r \\searrow$ crosses nose\n      $\\Rightarrow$ Voltage collapse',
                fontsize=8.2, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdedec', edgecolor='#c0392b', alpha=0.92))

    ax.set_xlim(0.0, 0.58)
    ax.set_ylim(0.0, 1.06)
    ax.set_xlabel(r'Normalized Active Power $x = P_R X_L / V_S^2$', fontsize=10)
    ax.set_ylabel(r'Normalized Voltage $y = V_R / V_S$', fontsize=10)
    ax.legend(loc='lower right', fontsize=8.0, frameon=True)
    ax.grid(True, linestyle='--', alpha=0.4)
    fig.tight_layout()

    out_path = out_dir / filename
    fig.savefig(out_path, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Successfully generated {out_path}')


if __name__ == '__main__':
    plot_oltc_scenario(stable=True, filename='PVcurvestable.pdf')
    plot_oltc_scenario(stable=False, filename='PVcurveunstable.pdf')
