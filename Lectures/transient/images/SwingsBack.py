import numpy as np
import matplotlib.pyplot as plt
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

delta0 = np.arcsin(Pm / Pmax1)
delta_1 = np.arcsin(Pm / Pmax3)  # post-fault equilibrium
delta_max = np.pi - delta_1

numerator = -Pm * (delta_max - delta0) - (Pmax3 * np.cos(delta_max)) + (Pmax2 * np.cos(delta0))
denominator = Pmax2 - Pmax3
delta_c_crit = np.arccos(numerator / denominator)

lam = 0.6
delta_cl = lam * delta0 + (1 - lam) * delta_c_crit

# Compute delta_m (delta_stop)
c_m = np.cos(delta_cl) * (Pmax3 - Pmax2) + Pm * delta0 + Pmax2 * np.cos(delta0)
delta_m = solve_transcendental(Pm, Pmax3, c_m, initial_guess=0.5 * (delta_cl + delta_max))

# Compute delta_2: int_{delta_2}^{delta_m} (Pm - Pmax3*sin(theta)) dtheta = 0
# => Pm * delta_2 + Pmax3 * cos(delta_2) = Pm * delta_m + Pmax3 * cos(delta_m)
c_2 = Pm * delta_m + Pmax3 * math.cos(delta_m)
delta_2 = solve_transcendental(Pm, Pmax3, c_2, initial_guess=0.1)

delta_min_plot = min(-0.15, delta_2 - 0.15)
delta = np.linspace(delta_min_plot, np.pi, 600)

Pe1 = Pmax1 * np.sin(delta)
Pe3 = Pmax3 * np.sin(delta)
Pm_line = np.full_like(delta, Pm)

fig = plt.figure(figsize=(6 * 2.5 / 2.54, 4 * 2.5 / 2.54))

plt.plot(delta, Pe1, 'k-', label='Pre-fault')
plt.plot(delta, Pe3, 'r--', label='Post-fault')
plt.plot(delta, Pm_line, 'k--', label=r'$P_m$')

# Area C: Deceleration (Pe3 > Pm) between delta_1 and delta_m
d_C = np.linspace(delta_1, delta_m, 400)
plt.fill_between(d_C, Pm, Pmax3 * np.sin(d_C), color='red', alpha=0.3, label='Area C (deceleration)')

# Area D: Acceleration (Pm > Pe3) between delta_2 and delta_1
d_D = np.linspace(delta_2, delta_1, 400)
plt.fill_between(d_D, Pm, Pmax3 * np.sin(d_D), color='blue', alpha=0.3, label='Area D (acceleration)')

# Arrows showing backward swing along post-fault curve
for d_arr in [0.5 * (delta_1 + delta_m), 0.5 * (delta_2 + delta_1)]:
    dd = -0.06
    plt.annotate(
        '',
        xy=(d_arr + dd, Pmax3 * np.sin(d_arr + dd)),
        xytext=(d_arr, Pmax3 * np.sin(d_arr)),
        arrowprops=dict(arrowstyle='->', color='red', lw=1.8),
    )

plt.xticks([0, np.pi / 2, np.pi], [r'$0$', r'$\pi/2$', r'$\pi$'])

y_min = min(-0.2, Pmax3 * np.sin(delta_2) - 0.15)
plt.vlines([delta_2, delta_1, delta_m], y_min, 1.8, linestyles=':', color='gray')
plt.text(delta_2, y_min - 0.12, r'$\delta_2$', ha='center', color='blue')
plt.text(delta_1, y_min - 0.12, r'$\delta_1$', ha='center', color='black')
plt.text(delta_m, y_min - 0.12, r'$\delta_m$', ha='center', color='red')

plt.xlabel(r'$\delta$ [rad]')
plt.ylabel(r'$P_e$ [pu]')
plt.legend(loc='upper right', fontsize=8)
plt.ylim(y_min, 1.8)
plt.xlim(delta_min_plot, np.pi)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig("Lectures/transient/images/SwingsBack.pdf")
plt.close(fig)
