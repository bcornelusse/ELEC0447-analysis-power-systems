import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Parameters
V_source = 1.0  # Voltage source [V]
R = 0.5         # Source resistance [Ohm]
P_max = V_source**2 / (4 * R)
V_crit = V_source / 2.0

out_dir = Path('Lectures') / 'voltage_stability' / 'images'
out_dir.mkdir(parents=True, exist_ok=True)


def plot_max_power_transfer():
    """Plot load voltage V and power P as a function of load resistance R_L."""
    R_L = np.linspace(0.0, 10.0, 500)
    V_L = V_source * R_L / (R + R_L)
    P_L = np.where(R_L > 0, V_L**2 / R_L, 0.0)

    fig, ax1 = plt.subplots(figsize=(7.0, 4.3))

    color1 = '#1b4f72'
    color2 = '#c0392b'

    l1 = ax1.plot(R_L, V_L, color=color1, linewidth=2.2, label=r'Voltage $V$ [V]')
    ax1.set_xlabel(r'$R_L$ ($\Omega$)', fontsize=11)
    ax1.set_ylabel(r'$V$ (V)', color=color1, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xlim(-0.2, 10.2)
    ax1.set_ylim(-0.04, 1.08)

    ax2 = ax1.twinx()
    l2 = ax2.plot(R_L, P_L, color=color2, linewidth=2.2, linestyle='--', label=r'Power $P$ [W]')
    ax2.set_ylabel(r'$P$ (W)', color=color2, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(-0.02, 0.58)

    # Maximum power transfer point (R_L = R)
    R_L_max = R
    V_L_max = V_source * R_L_max / (R + R_L_max)
    P_L_max = V_L_max**2 / R_L_max

    ax1.plot(R_L_max, V_L_max, 'o', color=color1, markersize=7.5, zorder=5)
    ax2.plot(R_L_max, P_L_max, '*', color=color2, markersize=13, zorder=5)
    ax1.axvline(x=R_L_max, color='gray', linestyle=':', alpha=0.6, linewidth=1.2)

    ax1.annotate(
        rf'$R_L = R = {R}\ \Omega$' + f'\n($V = {V_L_max:.2f}$ V)',
        xy=(R_L_max, V_L_max),
        xytext=(1.7, 0.34),
        arrowprops=dict(arrowstyle='->', color=color1, lw=1.1),
        fontsize=9.5,
        color=color1,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=color1, alpha=0.9),
    )
    ax2.annotate(
        rf'$P^{{\max}} = {P_L_max:.3f}$ W',
        xy=(R_L_max, P_L_max),
        xytext=(1.7, 0.515),
        arrowprops=dict(arrowstyle='->', color=color2, lw=1.1),
        fontsize=9.5,
        fontweight='bold',
        color=color2,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=color2, alpha=0.9),
    )

    lines = l1 + l2
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, fontsize=9.5)

    ax1.set_title(rf'Maximum Power Transfer: $E = {V_source:.0f}$ V, $R = {R}\ \Omega$', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.35)
    fig.tight_layout()

    out_file = out_dir / 'max_power_transfer_curve.pdf'
    fig.savefig(out_file, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Saved plot to: {out_file}')


def plot_dc_voltage_vs_power():
    """Plot the full DC nose curve V vs P parameterized by load voltage."""
    V_upper = np.linspace(V_crit, V_source, 400)
    P_upper = (V_upper * V_source - V_upper**2) / R

    V_lower = np.linspace(0.0, V_crit, 400)
    P_lower = (V_lower * V_source - V_lower**2) / R

    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(P_upper, V_upper, color='#1b4f72', linewidth=2.3, label=r'Upper / Stable branch ($R_L > R$)')
    ax.plot(P_lower, V_lower, color='#7f8c8d', linewidth=2.0, linestyle='--', label=r'Lower / Unstable branch ($R_L < R$)')

    ax.plot(P_max, V_crit, 's', color='#c0392b', markersize=7, zorder=5)
    ax.vlines(P_max, 0, V_crit, colors='#c0392b', linestyles=':', alpha=0.6, linewidth=1.2)
    ax.hlines(V_crit, 0, P_max, colors='#c0392b', linestyles=':', alpha=0.6, linewidth=1.2)

    ax.annotate(
        rf'Nose Point ($P^{{\max}} = {P_max:.2f}$ W, $V = {V_crit:.2f}$ V)',
        xy=(P_max, V_crit),
        xytext=(0.16, 0.53),
        arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.1),
        fontsize=9,
        fontweight='bold',
        color='#c0392b',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#c0392b', alpha=0.9),
    )

    ax.set_xlim(-0.01, 0.56)
    ax.set_ylim(-0.02, 1.06)
    ax.set_xlabel(r'Power Transferred $P$ (W)', fontsize=11)
    ax.set_ylabel(r'Load Voltage $V$ (V)', fontsize=11)
    ax.set_title(rf'DC Voltage vs. Power Transferred: $E = {V_source:.0f}$ V, $R = {R}\ \Omega$', fontsize=12)
    ax.legend(loc='lower left', frameon=True, fontsize=8.8)
    ax.grid(True, linestyle='--', alpha=0.35)
    fig.tight_layout()

    out_file = out_dir / 'DC_voltage_vs_power.pdf'
    fig.savefig(out_file, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Saved plot to: {out_file}')


def simulate_and_plot_controller(P0: float, filename: str):
    """Simulate dR_L/dt = R_L * I^2 - P0 and plot R_L(t), P(t), and V_L(t)."""
    t_max = 50.0
    dt = 0.01
    n_steps = int(np.ceil(t_max / dt))
    R_L0 = 5.0
    eps = 1e-9

    t = np.linspace(0.0, n_steps * dt, n_steps + 1)
    R_hist = np.zeros_like(t)
    R_hist[0] = R_L0

    def dRdt(RL):
        RL_eff = max(RL, eps)
        I = V_source / (R + RL_eff)
        return RL_eff * I**2 - P0

    for k in range(n_steps):
        y = R_hist[k]
        k1 = dRdt(y)
        k2 = dRdt(y + 0.5 * dt * k1)
        k3 = dRdt(y + 0.5 * dt * k2)
        k4 = dRdt(y + dt * k3)
        R_hist[k + 1] = max(y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4), eps)

    RL_eff = np.maximum(R_hist, eps)
    I_hist = V_source / (R + RL_eff)
    P_hist = RL_eff * I_hist**2
    V_hist = RL_eff * I_hist

    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(7.6, 6.2), sharex=True)

    color1 = '#1b4f72'
    color2 = '#c0392b'
    color3 = '#1e8449'

    l1 = ax1.plot(t, R_hist, color=color1, linewidth=2.1, label=r'$R_L(t)$ ($\Omega$)')
    ax1.set_ylabel(r'$R_L$ ($\Omega$)', color=color1, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.35)

    ax2 = ax1.twinx()
    l2 = ax2.plot(t, P_hist, color=color2, linewidth=2.1, linestyle='--', label=r'$P(t)$ (W)')
    l3 = ax2.axhline(P0, color='#555555', linestyle=':', linewidth=1.5, label=rf'Target $P_0 = {P0:.1f}$ W')
    ax2.set_ylabel(r'Power (W)', color=color2, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(-0.03, max(0.65, P0 + 0.08))

    lines = l1 + l2 + [l3]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True, fontsize=9)
    ax1.set_title(rf'Controller Response: Target $P_0 = {P0:.1f}$ W, Initial $R_L(0) = {R_L0:.0f}\ \Omega$', fontsize=12)

    ax3.plot(t, V_hist, color=color3, linewidth=2.1, label=r'$V_L(t)$')
    ax3.axhline(V_crit, color='#c0392b', linestyle=':', linewidth=1.4, label=rf'$V_{{\mathrm{{crit}}}} = {V_crit:.1f}$ V')
    ax3.set_xlabel('Time (s)', fontsize=11)
    ax3.set_ylabel(r'$V_L$ (V)', color=color3, fontsize=11)
    ax3.tick_params(axis='y', labelcolor=color3)
    ax3.set_ylim(-0.04, 1.04)
    ax3.legend(loc='upper right', frameon=True, fontsize=9)
    ax3.grid(True, linestyle='--', alpha=0.35)

    fig.tight_layout()
    out_file = out_dir / filename
    fig.savefig(out_file, format='pdf', bbox_inches='tight')
    plt.close(fig)
    print(f'Saved plot to: {out_file}')


if __name__ == '__main__':
    plot_max_power_transfer()
    plot_dc_voltage_vs_power()
    for target_p, fname in [(0.4, 'controller_response_400mW.pdf'), (0.6, 'controller_response_600mW.pdf')]:
        simulate_and_plot_controller(target_p, fname)
