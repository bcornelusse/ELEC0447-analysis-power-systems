import os
import numpy as np
import matplotlib.pyplot as plt

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'

# Exact skin depths in mm matching lecture table and physical values
# Cu: 50 Hz -> 9.4 mm, 60 Hz -> 8.6 mm, 400 Hz -> 3.3 mm
# Al: 50 Hz -> 12.0 mm, 60 Hz -> 10.9 mm, 400 Hz -> 4.2 mm
curves = [
    {'mat': 'Aluminum', 'freq': '50 Hz', 'delta': 12.0, 'color': '#00707F', 'ls': '-', 'lw': 2.2},
    {'mat': 'Aluminum', 'freq': '60 Hz', 'delta': 10.9, 'color': '#00707F', 'ls': '--', 'lw': 1.8},
    {'mat': 'Aluminum', 'freq': '400 Hz', 'delta': 4.2, 'color': '#00707F', 'ls': ':', 'lw': 1.6},
    {'mat': 'Copper', 'freq': '50 Hz', 'delta': 9.4, 'color': '#C85A17', 'ls': '-', 'lw': 2.2},
    {'mat': 'Copper', 'freq': '60 Hz', 'delta': 8.6, 'color': '#C85A17', 'ls': '--', 'lw': 1.8},
    {'mat': 'Copper', 'freq': '400 Hz', 'delta': 3.3, 'color': '#C85A17', 'ls': ':', 'lw': 1.6},
]

d = np.linspace(0, 30, 500)

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(4.3, 3.2), dpi=300)

for c in curves:
    J_ratio = np.exp(-d / c['delta'])
    label = f"{c['mat']} ({c['freq']}, $\\delta={c['delta']:.1f}\\,$mm)"
    ax.plot(d, J_ratio, linestyle=c['ls'], color=c['color'], linewidth=c['lw'], label=label)

# 1/e threshold line
one_over_e = 1.0 / np.e
ax.axhline(one_over_e, color='#444444', linestyle='-.', linewidth=1.2, alpha=0.85, label='$1/e \\approx 0.368$ (Skin depth $\\delta$)')

# Markers for 50 Hz skin depths
ax.plot([9.4], [one_over_e], 'o', color='#C85A17', markersize=6.0, zorder=5)
ax.plot([12.0], [one_over_e], 'o', color='#00707F', markersize=6.0, zorder=5)

# Annotations pointing to the markers
ax.annotate('Cu 50 Hz\n(9.4 mm)', xy=(9.4, one_over_e), xytext=(5.6, 0.16),
            fontsize=8.0, ha='center', color='#C85A17', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#C85A17', lw=1.0))
ax.annotate('Al 50 Hz\n(12.0 mm)', xy=(12.0, one_over_e), xytext=(15.5, 0.50),
            fontsize=8.0, ha='center', color='#00707F', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#00707F', lw=1.0))

ax.set_xlabel('Distance from surface $d$ [mm]', fontsize=9.5, fontweight='bold')
ax.set_ylabel('Current density ratio $J(d) / J_0$', fontsize=9.5, fontweight='bold')
ax.set_xlim(0, 30)
ax.set_ylim(0, 1.05)
ax.tick_params(labelsize=8.5)

ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper right', fontsize=7.2, frameon=True, framealpha=0.95, edgecolor='#cccccc',
          handlelength=1.4, labelspacing=0.25, borderaxespad=0.4)

plt.tight_layout(pad=0.5)

output_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(output_dir, 'skin_effect.pdf')
png_path = os.path.join(output_dir, 'skin_effect.png')

plt.savefig(pdf_path, bbox_inches='tight')
plt.savefig(png_path, bbox_inches='tight', dpi=300)
print(f"Saved: {pdf_path}")
print(f"Saved: {png_path}")
