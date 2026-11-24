import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']
plt.rcParams['font.sans-serif'] = ['Helvetica']

# Same system parameters as EAC.py & interactive_synchronism_loss.html
Pm = 0.8
Pmax1 = 1.6
Pmax2 = 0.5
Pmax3 = 1.3
H = 5.0
omega_syn = 2 * np.pi * 50.0
coeff = omega_syn / (2 * H)

delta0 = np.arcsin(Pm / Pmax1)
delta1 = np.arcsin(Pm / Pmax3)
delta_max = np.pi - delta1

t_fault = 0.25
dt = 0.001
t_end = 2.0
n_steps = int(t_end / dt) + 1
t = np.linspace(0, t_end, n_steps)


def simulate(tcl):
    delta = np.zeros(n_steps)
    omega = np.zeros(n_steps)
    delta[0] = delta0
    omega[0] = 0.0
    for i in range(n_steps - 1):
        tc = t[i]
        Pmax = Pmax1 if tc < t_fault else (Pmax2 if tc < t_fault + tcl else Pmax3)

        def deriv(d, w):
            return w, coeff * (Pm - Pmax * np.sin(d))

        k1d, k1w = deriv(delta[i], omega[i])
        k2d, k2w = deriv(delta[i] + 0.5 * dt * k1d, omega[i] + 0.5 * dt * k1w)
        k3d, k3w = deriv(delta[i] + 0.5 * dt * k2d, omega[i] + 0.5 * dt * k2w)
        k4d, k4w = deriv(delta[i] + dt * k3d, omega[i] + dt * k3w)

        delta[i + 1] = delta[i] + (dt / 6.0) * (k1d + 2 * k2d + 2 * k3d + k4d)
        omega[i + 1] = omega[i] + (dt / 6.0) * (k1w + 2 * k2w + 2 * k3w + k4w)
    return np.rad2deg(delta), omega


d_stable, w_stable = simulate(0.16)
d_lost, w_lost = simulate(0.40)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.8, 4.4), sharex=True)

ax1.axvspan(t_fault, t_fault + 0.40, color='orange', alpha=0.14, label=r'Fault window ($t_{cl}=0.40$ s)')
ax1.plot(t, d_stable, color='#00843B', lw=2.0, label=r'Stable ($t_{cl} = 0.16\ \mathrm{s} < \mathrm{CCT}$)')
ax1.plot(t, d_lost, color='#d93025', lw=2.0, label=r'Loss of synchronism ($t_{cl} = 0.40\ \mathrm{s} > \mathrm{CCT}$)')
ax1.axhline(np.rad2deg(delta_max), color='#d93025', ls=':', lw=1.2)
ax1.text(0.03, np.rad2deg(delta_max) + 12, r'$\delta_{\max} = %.1f^\circ$' % np.rad2deg(delta_max),
         color='#d93025', fontsize=9)
ax1.axhline(360, color='gray', ls='--', lw=0.9, alpha=0.6)
ax1.text(0.03, 372, r'$360^\circ$ (1 pole slip)', color='gray', fontsize=8)
ax1.set_ylabel(r'$\delta$ [deg]')
ax1.set_ylim(0, max(620, np.max(d_lost) * 1.08))
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left', fontsize=8, frameon=True)

ax2.axvspan(t_fault, t_fault + 0.40, color='orange', alpha=0.14)
ax2.plot(t, w_stable, color='#00843B', lw=2.0)
ax2.plot(t, w_lost, color='#d93025', lw=2.0)
ax2.axhline(0, color='black', lw=0.8, alpha=0.5)
ax2.set_xlabel(r'$t$ [s]')
ax2.set_ylabel(r'$\Delta\omega$ [rad/s]')
ax2.set_xlim(0, t_end)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Lectures/transient/images/LossOfSynchronism.pdf")
plt.close(fig)
