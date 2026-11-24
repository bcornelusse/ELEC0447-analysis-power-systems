import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
import math

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']
plt.rcParams['font.sans-serif'] = ['Helvetica']


def solve_transcendental(a, b, c, initial_guess, tolerance=1e-6, max_iterations=100):
    x = initial_guess
    for _ in range(max_iterations):
        f_x = a * x + b * math.cos(x) - c
        f_prime_x = a - b * math.sin(x)
        if abs(f_prime_x) < 1e-9:
            return None
        x_next = x - f_x / f_prime_x
        if abs(x_next - x) < tolerance:
            return x_next
        x = x_next
    return None


# Same parameters as EAC.py
Pm = 0.8
Pmax1 = 1.6
Pmax2 = 0.5
Pmax3 = 1.3
H = 5.0
omega_syn = 2 * np.pi * 50.0
coeff = omega_syn / (2 * H)

delta0 = np.arcsin(Pm / Pmax1)
delta_1 = np.arcsin(Pm / Pmax3)
delta_max = np.pi - delta_1

numerator = -Pm * (delta_max - delta0) - (Pmax3 * np.cos(delta_max)) + (Pmax2 * np.cos(delta0))
denominator = Pmax2 - Pmax3
delta_c_crit = np.arccos(numerator / denominator)

lam = 0.6
delta_cl = lam * delta0 + (1 - lam) * delta_c_crit

c_m = np.cos(delta_cl) * (Pmax3 - Pmax2) + Pm * delta0 + Pmax2 * np.cos(delta0)
delta_m = solve_transcendental(Pm, Pmax3, c_m, initial_guess=0.5 * (delta_cl + delta_max))

c_2 = Pm * delta_m + Pmax3 * math.cos(delta_m)
delta_2 = solve_transcendental(Pm, Pmax3, c_2, initial_guess=0.1)

# Integrate swing equation with RK4
dt = 0.001
t_end = 4.0
n_steps = int(t_end / dt) + 1
t = np.linspace(0, t_end, n_steps)
delta = np.zeros(n_steps)
omega = np.zeros(n_steps)  # d(delta)/dt
accel = np.zeros(n_steps)  # Pm - Pe

delta[0] = delta0
omega[0] = 0.0
cleared = False

for i in range(n_steps - 1):
    if not cleared and delta[i] >= delta_cl:
        cleared = True
    Pmax_curr = Pmax3 if cleared else Pmax2
    accel[i] = Pm - Pmax_curr * np.sin(delta[i])

    def deriv(d, w):
        return w, coeff * (Pm - Pmax_curr * np.sin(d))

    k1_d, k1_w = deriv(delta[i], omega[i])
    k2_d, k2_w = deriv(delta[i] + 0.5 * dt * k1_d, omega[i] + 0.5 * dt * k1_w)
    k3_d, k3_w = deriv(delta[i] + 0.5 * dt * k2_d, omega[i] + 0.5 * dt * k2_w)
    k4_d, k4_w = deriv(delta[i] + dt * k3_d, omega[i] + dt * k3_w)

    delta[i + 1] = delta[i] + (dt / 6.0) * (k1_d + 2 * k2_d + 2 * k3_d + k4_d)
    omega[i + 1] = omega[i] + (dt / 6.0) * (k1_w + 2 * k2_w + 2 * k3_w + k4_w)

accel[-1] = Pm - Pmax3 * np.sin(delta[-1])

# Color curve segments: blue when accelerating (Pm > Pe), red when decelerating (Pe > Pm)
points = np.array([t, delta]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
colors = ['tab:blue' if a >= 0 else 'tab:red' for a in accel[:-1]]

fig, ax = plt.subplots(figsize=(6 * 2.5 / 2.54, 3.6 * 2.5 / 2.54))
lc = LineCollection(segments, colors=colors, linewidths=2.0)
ax.add_collection(lc)

# Reference lines for delta_m, delta_1, delta_2
ax.axhline(delta_m, color='red', linestyle=':', linewidth=1.2)
ax.axhline(delta_1, color='black', linestyle='--', linewidth=1.0, alpha=0.6)
ax.axhline(delta_2, color='blue', linestyle=':', linewidth=1.2)

ax.text(t_end * 1.015, delta_m, r'$\delta_m$', va='center', ha='left', color='red', fontsize=11)
ax.text(t_end * 1.015, delta_1, r'$\delta_1$', va='center', ha='left', color='black', fontsize=11)
ax.text(t_end * 1.015, delta_2, r'$\delta_2$', va='center', ha='left', color='blue', fontsize=11)

legend_handles = [
    Line2D([0], [0], color='tab:blue', lw=2, label=r'Acceleration ($P_m > P_e$)'),
    Line2D([0], [0], color='tab:red', lw=2, label=r'Deceleration ($P_e > P_m$)'),
]
ax.legend(handles=legend_handles, loc='upper right', fontsize=8, frameon=True)

ax.set_xlim(0, t_end)
ax.set_ylim(delta_2 - 0.15, delta_m + 0.35)
ax.set_xlabel(r'$t$ [s]')
ax.set_ylabel(r'$\delta$ [rad]')
ax.grid(True, alpha=0.35)

plt.tight_layout()
plt.subplots_adjust(right=0.92)
plt.savefig("Lectures/transient/images/RotorOscillation.pdf")
plt.close(fig)
