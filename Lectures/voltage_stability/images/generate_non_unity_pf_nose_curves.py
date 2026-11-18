import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Normalized 2-bus lossless AC power flow:
#   y = V_R / V_S,  x = P_R * X_L / V_S^2,  Q_R = P_R * tan(phi)
#   y^4 + (2 * x * tan(phi) - 1) * y^2 + x^2 * (1 + tan^2(phi)) = 0
#   x_max(phi) = cos(phi) / (2 * (1 + sin(phi)))

tan_phis = [-0.41, -0.20, 0.00, 0.20, 0.41, 0.67, 1.00, 1.50, 2.41, 5.03]

fig, ax = plt.subplots(figsize=(6.2, 4.4), dpi=300)
cmap = plt.get_cmap('viridis')

for idx, tphi in enumerate(tan_phis):
    phi = np.arctan(tphi)
    x_max = np.cos(phi) / (2.0 * (1.0 + np.sin(phi)))
    x = np.linspace(0.0, x_max * (1.0 - 1e-7), 600)

    b = 2.0 * x * tphi - 1.0
    c = x**2 * (1.0 + tphi**2)
    disc = np.maximum(b**2 - 4.0 * c, 0.0)

    y_upper = np.sqrt(np.maximum(0.5 * (-b + np.sqrt(disc)), 0.0))
    y_lower = np.sqrt(np.maximum(0.5 * (-b - np.sqrt(disc)), 0.0))

    # Concatenate upper (0 -> x_max) and lower (x_max -> 0) into one continuous nose curve
    x_full = np.concatenate([x, x[::-1]])
    y_full = np.concatenate([y_upper, y_lower[::-1]])

    is_unity = np.isclose(tphi, 0.0)
    color = '#c0392b' if is_unity else cmap(0.15 + 0.72 * idx / (len(tan_phis) - 1))
    lw = 2.4 if is_unity else 1.6
    ax.plot(x_full, y_full, color=color, linewidth=lw, zorder=4 if is_unity else 3)

    # Place label near the nose tip or upper-right of each curve
    y_nose = np.sqrt(0.5 * (1.0 - 2.0 * x_max * tphi))
    if tphi == -0.41:
        ax.text(x_max - 0.06, 1.04, r'$\tan\phi = -0.41$', fontsize=8.5, color=color, fontweight='bold')
    elif tphi == -0.20:
        ax.text(x_max - 0.04, 0.93, r'$-0.20$', fontsize=8.5, color=color, fontweight='bold')
    elif is_unity:
        ax.text(x_max + 0.012, y_nose, r'$0.00$ ($\cos\phi=1$)', fontsize=8.5, color=color, fontweight='bold', va='center')
    elif tphi <= 1.00:
        ax.text(x_max + 0.01, y_nose - 0.01, f'{tphi:.2f}', fontsize=8, color=color, va='center')
    else:
        ax.text(x_max + 0.01, y_nose - 0.015, f'{tphi:.2f}', fontsize=8, color=color, va='center')

ax.axhline(1.0, color='gray', linestyle=':', linewidth=0.9, alpha=0.6)
ax.set_xlim(0.0, 0.85)
ax.set_ylim(0.0, 1.18)
ax.set_xlabel(r'Normalized Active Power $P_R X_L / V_S^2$', fontsize=10.5)
ax.set_ylabel(r'Normalized Receiving-End Voltage $V_R / V_S$', fontsize=10.5)
ax.set_title(r'$P$-$V$ Nose Curves for Different Power Factors ($\tan\phi = Q_R / P_R$)', fontsize=11)
ax.grid(True, linestyle='--', alpha=0.4)

# Annotations for leading vs lagging
ax.text(0.56, 0.22, r'Leading PF ($\tan\phi < 0$)' + '\nLoad supplies $Q$', fontsize=8.5,
        color='#1b4f72', zorder=6,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#1b4f72', alpha=0.95))
ax.text(0.03, 0.14, r'Lagging PF ($\tan\phi > 0$)' + '\nLoad consumes $Q$', fontsize=8.5,
        color='#444444', zorder=6,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#888888', alpha=0.95))

fig.tight_layout()
out_path = Path('Lectures/voltage_stability/images/TrueNoseCurve.pdf')
fig.savefig(out_path, format='pdf', bbox_inches='tight')
plt.close(fig)
print(f'Successfully generated {out_path}')
