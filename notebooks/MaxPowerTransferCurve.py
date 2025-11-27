import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

# Parameters
V_source = 1  # Voltage source in volts
R = 0.5  # Source resistance in ohms

# Load resistance range
R_L = np.linspace(0.0, 10, 400)

# Calculate voltage across load
V_L = V_source * R_L / (R + R_L)

# Calculate power transferred to load
P_L = V_L**2 / R_L

# Create figure
plt.figure(figsize=(7, 4.5))

# Plot voltage across load
ax1 = plt.gca()
color1 = 'tab:blue'
ax1.set_xlabel(r'$R_L$ (Ω)', fontsize=12)
ax1.set_ylabel(r'$V$ (V)', color=color1, fontsize=12)
ax1.plot(R_L, V_L, color=color1, linewidth=2, label=r'Voltage $V$')
ax1.tick_params(axis='y', labelcolor=color1)

# Create second y-axis for power
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel(r'$P$ (W)', color=color2, fontsize=12)
ax2.plot(R_L, P_L, color=color2, linewidth=2, linestyle='--', label=r'Power $P$')
ax2.tick_params(axis='y', labelcolor=color2)

# Find maximum power transfer point (when R_L = R)
R_L_max = R
V_L_max = V_source * R_L_max / (R + R_L_max)
P_L_max = V_L_max**2 / R_L_max
ax1.plot(R_L_max, V_L_max, 'bo', markersize=8)
ax2.plot(R_L_max, P_L_max, 'r*', markersize=15)
ax1.axvline(x=R_L_max, color='gray', linestyle=':', alpha=0.5)

# Annotations
ax1.text(R_L_max, V_L_max + 0.05, 
         rf'$R_L = R = {R}$ Ω', 
         fontsize=10, ha='center')
ax2.text(R_L_max + 0.3, P_L_max, 
         rf'$P^{{max}} = {P_L_max:.3f}$ W', 
         fontsize=10, color=color2)

plt.title(r'Maximum Power Transfer: $E = ' + f'{V_source}$ V, $R = {R}$ Ω', 
          fontsize=13)
plt.grid(True, alpha=0.3)
plt.tight_layout()


# Save figure
out_dir = Path('Lectures') / 'voltage_stability' / 'images'
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / 'max_power_transfer_curve.pdf'
plt.savefig(out_file, format='pdf', bbox_inches='tight', dpi=300)
print(f'Saved plot to: {out_file}')

# Plot V_L vs P_L
plt.figure(figsize=(6, 3.6))
plt.plot(P_L, V_L, color='purple', linewidth=2)
plt.xlabel(r'$P$ (W)', fontsize=12)
plt.ylabel(r'$V$ (V)', fontsize=12)
plt.title(r'Voltage vs Power Transfered: $E = ' + f'{V_source}$ V, $R = {R}$ Ω', fontsize=13)
plt.grid(True, alpha=0.3)
plt.tight_layout()

out_file_vp = out_dir / 'DC_voltage_vs_power.pdf'
plt.savefig(out_file_vp, format='pdf', bbox_inches='tight', dpi=300)
print(f'Saved plot to: {out_file_vp}')

# Controller simulation: dR_L/dt = R_L * I**2 - P0  where I = V_source / (R + R_L)
P0 = 0.4  # target power in watts (adjust as needed)

t_max = 50.0
dt = 0.01
n_steps = int(np.ceil(t_max / dt))

# initial controlled load resistance
R_L0 = 5


eps = 1e-9  # small floor to avoid divide-by-zero
t = np.linspace(0.0, n_steps * dt, n_steps + 1)
R_hist = np.zeros_like(t)
P_hist = np.zeros_like(t)
V_hist = np.zeros_like(t)


R_hist[0] = R_L0

def dRdt(RL):
    RL_eff = max(RL, eps)
    I = V_source / (R + RL_eff)
    return RL_eff * I**2 - P0

# 4th-order Runge-Kutta for scalar ODE
for k in range(n_steps):
    y = R_hist[k]
    k1 = dRdt(y)
    k2 = dRdt(y + 0.5 * dt * k1)
    k3 = dRdt(y + 0.5 * dt * k2)
    k4 = dRdt(y + dt * k3)
    y_next = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    y_next = max(y_next, eps)
    R_hist[k + 1] = y_next

# compute power history consistently as P = R_L * I**2
for k in range(len(t)):
    RL = max(R_hist[k], eps)
    I = V_source / (R + RL)
    P_hist[k] = RL * I**2
    V_hist[k] = RL * I

# Plot R_L and P over time
fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(8, 7))

# First subplot: R_L and P over time
color1 = 'tab:blue'
ax1.plot(t, R_hist, color=color1, linewidth=2, label=r'$R_L(t)$')
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel(r'$R_L$ (Ω)', color=color1, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.plot(t, P_hist, color=color2, linewidth=2, linestyle='--', label=r'$P(t)$')
ax2.axhline(P0, color='gray', linestyle=':', label=r'$P_0$')
ax2.set_ylabel('Power (W)', color=color2, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color2)

# Second subplot: V_L over time
color3 = 'tab:green'
ax3.plot(t, V_hist, color=color3, linewidth=2, label=r'$V_L(t)$')
ax3.set_xlabel('Time (s)', fontsize=12)
ax3.set_ylabel(r'$V_L$ (V)', color=color3, fontsize=12)
ax3.tick_params(axis='y', labelcolor=color3)
ax3.grid(True, alpha=0.3)
ax1.grid(True, alpha=0.3)

plt.title(f'Controller response: target P0 = {P0} W, initial R_L = {R_L0} Ω', fontsize=13)
fig.tight_layout()

out_file_ctrl = out_dir / 'controller_response.pdf'
plt.savefig(out_file_ctrl, format='pdf', bbox_inches='tight', dpi=300)
print(f'Saved controller response plot to: {out_file_ctrl}')