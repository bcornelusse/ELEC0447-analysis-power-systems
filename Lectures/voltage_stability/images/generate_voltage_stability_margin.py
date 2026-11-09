import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Parameters for AC radial line with unity power factor (cos phi = 1)
Vs = 1.0                # Source voltage [pu]
X = 0.5                 # Line reactance [pu]
Pmax = Vs**2 / (2 * X)  # Maximum transmissible power: Pmax = 1.0 pu
Vcrit = Vs / np.sqrt(2) # Critical voltage: Vcrit = 0.7071 pu

# Generate curve using angle delta: 0 to pi/2
delta = np.linspace(0, np.pi / 2, 800)
P = (Vs**2 / (2 * X)) * np.sin(2 * delta)
V = Vs * np.cos(delta)

# Upper (stable) and lower (unstable) branches
upper = delta <= np.pi / 4
lower = delta >= np.pi / 4

# Operating point at P0 = 0.65 pu
P0 = 0.65
delta0 = 0.5 * np.arcsin(P0 / Pmax)
V0 = Vs * np.cos(delta0)
delta_P = Pmax - P0

fig, ax = plt.subplots(figsize=(5.6, 3.8), dpi=300)

# Plot curves
ax.plot(P[upper], V[upper], color='#1b4f72', linewidth=2.5, label='Upper / Stable branch ($dV/dP < 0$)')
ax.plot(P[lower], V[lower], color='#7f8c8d', linewidth=2.0, linestyle='--', label='Lower / Unstable branch ($dV/dP > 0$)')

# Points
ax.plot(P0, V0, 'o', color='#1b4f72', markersize=6.5, zorder=5)
ax.plot(Pmax, Vcrit, 's', color='#c0392b', markersize=6.5, zorder=5)

# Drop lines
ax.vlines(P0, 0, V0, colors='#1b4f72', linestyles=':', alpha=0.55, linewidth=1.1)
ax.hlines(V0, 0, P0, colors='#1b4f72', linestyles=':', alpha=0.55, linewidth=1.1)

ax.vlines(Pmax, 0, Vcrit, colors='#c0392b', linestyles=':', alpha=0.55, linewidth=1.1)
ax.hlines(Vcrit, 0, Pmax, colors='#c0392b', linestyles=':', alpha=0.55, linewidth=1.1)

# Shaded margin region
ax.axvspan(P0, Pmax, ymin=0, ymax=1.0, color='#27ae60', alpha=0.08)

# Margin double arrow
arrow_y = 0.35
ax.annotate('', xy=(Pmax, arrow_y), xytext=(P0, arrow_y),
            arrowprops=dict(arrowstyle='<->', color='#27ae60', lw=2.0))
ax.text((P0 + Pmax) / 2, arrow_y + 0.04, r'Margin $\Delta P = P_{\max} - P_0$',
        ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#196f3d',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#eafaf1', edgecolor='#27ae60', alpha=0.9))

# Point labels
ax.annotate(r'Operating Point $(P_0, V_0)$' + f'\n($P_0={P0:.2f}$, $V_0={V0:.2f}$ pu)',
            xy=(P0, V0), xytext=(P0 - 0.30, V0 + 0.04),
            arrowprops=dict(arrowstyle='->', color='#1b4f72', lw=1.1),
            fontsize=8.5, fontweight='bold', color='#1b4f72',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#1b4f72', alpha=0.85))

ax.annotate(r'Nose Point $(P_{\max}, V_{\mathrm{crit}})$' + f'\n($P_{{\max}}={Pmax:.2f}$, $V_{{\mathrm{{crit}}}}={Vcrit:.2f}$ pu)',
            xy=(Pmax, Vcrit), xytext=(Pmax - 0.38, Vcrit - 0.18),
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.1),
            fontsize=8.5, fontweight='bold', color='#c0392b',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#c0392b', alpha=0.85))

# Axis limits & labels
ax.set_xlim(-0.02, 1.15)
ax.set_ylim(0.0, 1.10)
ax.set_xlabel(r'Transferred Active Power $P$ [pu]', fontsize=10)
ax.set_ylabel(r'Receiving-End Voltage $V$ [pu]', fontsize=10)
ax.set_title(r'$P$-$V$ Nose Curve & Voltage Stability Margin ($\cos\phi = 1$)', fontsize=11, pad=8)

# Custom ticks
ax.set_xticks([0.0, 0.2, 0.4, P0, 0.8, Pmax])
ax.set_xticklabels(['0.0', '0.2', '0.4', r'$P_0$', '0.8', r'$P_{\max}$'], fontsize=9)
ax.set_yticks([0.0, 0.2, 0.4, 0.6, Vcrit, 0.8, V0, 1.0])
ax.set_yticklabels(['0.0', '0.2', '0.4', '0.6', r'$V_{\mathrm{crit}}$', '0.8', r'$V_0$', '1.0'], fontsize=9)

ax.legend(loc='lower left', frameon=True, fontsize=8.5)
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
out_dir = Path('Lectures/voltage_stability/images')
out_dir.mkdir(parents=True, exist_ok=True)
pdf_path = out_dir / 'voltage_stability_margin.pdf'
png_path = out_dir / 'voltage_stability_margin.png'
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f'Successfully updated {pdf_path} and {png_path}')
