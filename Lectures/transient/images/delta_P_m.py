import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']
plt.rcParams['font.sans-serif'] = ['Helvetica']

delta = np.linspace(0, np.pi, 500)
Pmax = 10.0
Pe = Pmax * np.sin(delta)
Pm = 7.0

delta_eq1 = np.arcsin(Pm / Pmax)
delta_eq2 = np.pi - delta_eq1

fig, ax = plt.subplots(figsize=(5.5, 4.2))
ax.plot(delta, Pe, 'k-', linewidth=2, label=r'$P_e(\delta) = 10 \sin\delta$')
ax.axhline(Pm, color='red', linestyle='--', linewidth=1.8, label=r'$P_m = 7\ \mathrm{pu}$')
ax.plot([delta_eq1, delta_eq2], [Pm, Pm], 'ro', markersize=8, zorder=5)

ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_xticklabels([r'$0$', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$'])
ax.set_xlim(0, np.pi)
ax.set_ylim(0, 10.5)
ax.set_xlabel(r'$\delta_{eq}$ [rad]', fontsize=12)
ax.set_ylabel(r'$P_e,\ P_m$ [pu]', fontsize=12)
ax.grid(True, alpha=0.4)
ax.legend(loc='upper right', frameon=True)

plt.tight_layout()
plt.savefig("Lectures/transient/images/delta_P_m.pdf")
plt.close(fig)
