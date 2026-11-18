import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

out_dir = Path('Lectures/voltage_stability/images')
out_dir.mkdir(parents=True, exist_ok=True)


def torque(s: np.ndarray, V: float, R1: float = 0.02, R2: float = 0.04, Xeq: float = 0.22) -> np.ndarray:
    """Steady-state induction motor electromechanical torque-slip characteristic."""
    s_safe = np.maximum(s, 1e-4)
    return (V**2 * (R2 / s_safe)) / ((R1 + R2 / s_safe) ** 2 + Xeq**2)


s = np.linspace(0.001, 1.0, 1000)
# Plot against (1 - s) so slip increases right-to-left (S_0^- < S_1 < S_2), matching standard motor-stalling convention
x_axis = 1.0 - s

V_levels = [
    (1.00, r'$C_0^-$ (nominal $V$)', '#1b4f72', 2.2, '-'),
    (0.86, r'$C_0^+$ (voltage drop)', '#2874a6', 1.8, '-'),
    (0.82, r'$C_1$ (further drop)', '#d35400', 1.7, '--'),
    (0.76, r'$C_2$ (stalling)', '#c0392b', 2.0, '-'),
]

fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=300)

T_L = 1.38
T0_plus = 1.10

for V, label, color, lw, ls in V_levels:
    T = torque(s, V)
    ax.plot(x_axis, T, color=color, linewidth=lw, linestyle=ls, label=label)

# Mechanical torque T_L and reduced T_0^+
ax.axhline(T_L, color='#111111', linewidth=1.6, label=r'Mechanical torque $T_L$')
ax.axhline(T0_plus, color='#555555', linewidth=1.2, linestyle='--', label=r'$T_0^+$')

# Find intersections on stable (right) side for C_0^-, C_0^+, C_1
markers = []
for V, name, color in [(1.00, r'$S_0^-$', '#1b4f72'), (0.86, r'$S_1$', '#2874a6'), (0.82, r'$S_2$', '#d35400')]:
    T = torque(s, V)
    # Rightmost root (smallest slip s)
    idx_peak = np.argmax(T)
    s_right = s[: idx_peak + 1]
    T_right = T[: idx_peak + 1]
    idx_cross = np.argmin(np.abs(T_right - T_L))
    sx = 1.0 - s_right[idx_cross]
    ax.plot(sx, T_L, 'o', color=color, markersize=6, zorder=5)
    ax.vlines(sx, 0.0, T_L, colors=color, linestyles=':', linewidth=1.2)
    markers.append((sx, name, color))

ax.set_xlim(0.0, 1.02)
ax.set_ylim(0.0, 2.35)
ax.set_xticks([m[0] for m in markers])
ax.set_xticklabels([m[1] for m in markers], fontsize=9.5, fontweight='bold')
ax.set_yticks([T0_plus, T_L])
ax.set_yticklabels([r'$T_0^+$', r'$T_L$'], fontsize=9.5, fontweight='bold')

ax.set_xlabel(r'Rotor speed $\omega_r / \omega_s = 1 - s$  ($\longleftarrow$ slip $s$ increases)', fontsize=10)
ax.set_ylabel('Torque', fontsize=10)
ax.set_title('Induction Motor Torque–Slip Curves & Voltage Stalling', fontsize=11)
ax.legend(loc='upper left', fontsize=8.3, frameon=True)
ax.grid(True, linestyle='--', alpha=0.35)
fig.tight_layout()

out_path = out_dir / 'Motorstalling.pdf'
fig.savefig(out_path, format='pdf', bbox_inches='tight')
plt.close(fig)
print(f'Successfully generated {out_path}')
