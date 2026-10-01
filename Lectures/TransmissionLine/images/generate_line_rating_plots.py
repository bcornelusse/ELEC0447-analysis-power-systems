import os
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'

import numpy as np
import matplotlib.pyplot as plt

# Theme colors matching Trigon Beamer theme
C_TEAL = '#00707F'       # tPrim
C_ORANGE = '#C85A17'     # tOrange / Accent
C_RED = '#D12239'        # myRed
C_GREEN = '#289B38'      # tSec / Green
C_DARK = '#2C3E50'       # Dark text/slate
C_GRAY = '#7F8C8D'

# Conductor parameters (ACSR Drake: 28.1 mm outer diameter, 75-80 C rating)
D = 0.0281               # Outer diameter [m]
T_max = 80.0             # Maximum operating temperature [deg C]
alpha_s = 0.8            # Solar absorptivity
epsilon = 0.8            # Emissivity
sigma_SB = 5.670374e-8   # Stefan-Boltzmann constant [W/(m^2 K^4)]
R_80 = 8.9e-5            # AC resistance at 80 deg C [Ohm/m]

def calc_ampacity(Ta, vw, S=1000.0, phi_deg=90.0):
    """Calculates steady-state ampacity according to IEEE Std 738."""
    T_film = 0.5 * (T_max + Ta)
    T_film_K = T_film + 273.15
    mu = (1.458e-6 * T_film_K**1.5) / (T_film_K + 110.4)
    rho = 1.293 * 273.15 / T_film_K
    k_air = 2.424e-2 + 7.477e-5 * T_film
    nu = mu / rho
    Re = max(0.0, vw) * D / nu

    # Wind direction factor
    phi_rad = np.radians(phi_deg)
    k_angle = 1.194 - np.cos(phi_rad) + 0.194 * np.cos(2 * phi_rad) + 0.368 * np.sin(2 * phi_rad)
    k_angle = max(0.38, min(1.0, k_angle))

    # Radiative cooling
    qr = np.pi * D * epsilon * sigma_SB * ((T_max + 273.15)**4 - (Ta + 273.15)**4)

    # Solar gain
    qs = alpha_s * S * D

    # Convective cooling
    qc1 = (1.01 + 1.35 * (Re**0.52)) * k_air * k_angle * (T_max - Ta)
    qc2 = (0.754 * (Re**0.60)) * k_air * k_angle * (T_max - Ta)
    qcn = 3.645 * (rho**0.5) * (D**0.75) * ((T_max - Ta)**1.25)
    qc = max(qc1, qc2, qcn)

    q_net = qc + qr - qs
    return np.sqrt(max(0.0, q_net) / R_80)

# ==============================================================================
# Plot 1: Ampacity vs Wind Speed (Summer & Winter)
# ==============================================================================
def generate_ampacity_vs_wind():
    vw = np.linspace(0.0, 10.0, 300)
    
    # Summer: Ta = 35 C, S = 1000 W/m2
    I_summer = np.array([calc_ampacity(35.0, v, S=1000.0) for v in vw])
    # Winter: Ta = 5 C, S = 400 W/m2
    I_winter = np.array([calc_ampacity(5.0, v, S=400.0) for v in vw])

    I_stat_summer = calc_ampacity(35.0, 0.5, S=1000.0) # ~817 A
    I_breeze_summer = calc_ampacity(35.0, 2.0, S=1000.0) # ~1172 A

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(5.5, 3.15), dpi=300)

    ax.plot(vw, I_winter, color=C_TEAL, lw=2.4, label='Winter ($T_a = 5^\\circ$C, $S=400\\,$W/m$^2$)')
    ax.plot(vw, I_summer, color=C_ORANGE, lw=2.4, label='Summer ($T_a = 35^\\circ$C, $S=1000\\,$W/m$^2$)')

    # Static line rating baseline
    ax.axhline(I_stat_summer, color=C_RED, ls='--', lw=1.6, label=f'Static Rating (SLR): {I_stat_summer:.0f} A')
    ax.plot([0.5], [I_stat_summer], 'o', color=C_RED, markersize=5.5, zorder=5)

    # Point at 2 m/s breeze
    ax.plot([2.0], [I_breeze_summer], 's', color=C_ORANGE, markersize=6.0, zorder=5)

    # Annotation for 2 m/s breeze
    gain_pct = (I_breeze_summer / I_stat_summer - 1.0) * 100
    ax.annotate(f'Light breeze (2 m/s):\n{I_breeze_summer:.0f} A (+{gain_pct:.0f}%)',
                xy=(2.0, I_breeze_summer), xytext=(3.5, 950),
                fontsize=8.0, fontweight='bold', color=C_ORANGE,
                arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=1.2),
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=C_ORANGE, alpha=0.9))

    ax.set_xlabel('Wind speed perpendicular to line $v_w$ [m/s]', fontsize=8.5, fontweight='bold')
    ax.set_ylabel('Line Ampacity $I_{\\text{max}}$ [A]', fontsize=8.5, fontweight='bold')
    ax.set_xlim(0, 10)
    ax.set_ylim(600, 2200)
    ax.tick_params(labelsize=8.0)
    ax.grid(True, ls='--', alpha=0.55)

    ax.legend(loc='upper left', fontsize=7.5, frameon=True, framealpha=0.92, edgecolor='#dddddd')
    plt.tight_layout(pad=0.5)

    out_pdf = 'Lectures/TransmissionLine/images/ampacity_vs_wind.pdf'
    out_png = 'Lectures/TransmissionLine/images/ampacity_vs_wind.png'
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.savefig(out_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated: {out_pdf} and {out_png}")

# ==============================================================================
# Plot 2: 24-Hour Time Series (SLR vs DLR vs Line Loading)
# ==============================================================================
def generate_dlr_vs_slr_24h():
    hours = np.linspace(0, 24, 288) # 5-min intervals
    
    # Summer heatwave profile: min 20 C at 05:00, peak 38 C at 13:30
    T_a = 28.0 - 8.0 * np.cos(2 * np.pi * (hours - 5) / 24) + 3.0 * np.exp(-((hours - 13.0)/1.8)**2)
    
    # Solar radiation [W/m2]: 0 at night, peak 1000 W/m2 at 13:00
    solar = np.maximum(0.0, 1000.0 * np.sin(np.pi * np.clip(hours - 6, 0, 14) / 14))

    # Wind speed [m/s]:
    # Midday calm lull around 12:45 (v_w down to 0.1 m/s), strong afternoon/evening wind generation (5-6 m/s)
    np.random.seed(42)
    v_w = 2.8 - 2.7 * np.exp(-((hours - 12.6)/1.4)**2) + 2.8 * np.exp(-((hours - 17.0)/3.2)**2)
    noise = np.random.normal(0, 0.12, len(hours))
    noise_smooth = np.convolve(noise, np.ones(5)/5, mode='same')
    v_w = np.clip(v_w + noise_smooth, 0.08, 7.5)

    # Calculate DLR over 24h
    I_dlr = np.array([calc_ampacity(t, w, S=s) for t, w, s in zip(T_a, v_w, solar)])
    
    # Static rating: conservative benchmark
    I_slr = 820.0 * np.ones_like(hours)

    # Actual load current [A] (wind generation injection ramping up in afternoon)
    I_load = 550.0 + 380.0 * np.sin(np.pi * np.clip(hours - 10, 0, 12) / 12)**2 + 80 * np.sin(2*np.pi*hours/24)

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(5.5, 3.15), dpi=300)

    # Shaded headroom area (DLR above SLR)
    ax.fill_between(hours, I_slr, I_dlr, where=(I_dlr >= I_slr),
                    color=C_GREEN, alpha=0.20, label='Unlocked Headroom (+10--80%)')

    # Shaded risk area if DLR < SLR
    ax.fill_between(hours, I_dlr, I_slr, where=(I_dlr < I_slr),
                    color=C_RED, alpha=0.35, label='SLR Overestimates Capacity!')

    # Lines
    ax.plot(hours, I_dlr, color=C_TEAL, lw=2.2, label='Dynamic Line Rating ($I_{\\mathrm{DLR}}$)')
    ax.plot(hours, I_slr, color=C_RED, ls='--', lw=1.8, label='Static Line Rating ($I_{\\mathrm{SLR}}$)')
    ax.plot(hours, I_load, color=C_DARK, ls='-', lw=1.8, label='Actual Line Loading $I(t)$')

    # Annotations:
    # 1. Midday lull where DLR < SLR
    idx_min = np.argmin(I_dlr)
    ax.annotate('Extreme calm & heat:\n$I_{\\mathrm{DLR}} < I_{\\mathrm{SLR}}$ (Safety risk avoided!)',
                xy=(hours[idx_min], I_dlr[idx_min]), xytext=(hours[idx_min]-7.2, I_dlr[idx_min]-180),
                fontsize=7.2, fontweight='bold', color=C_RED,
                arrowprops=dict(arrowstyle='->', color=C_RED, lw=1.0),
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=C_RED, alpha=0.92))

    # 2. Peak wind injection where I_load > I_slr but safe under DLR
    idx_peak = np.argmax(I_load)
    ax.plot([hours[idx_peak]], [I_load[idx_peak]], 'o', color=C_DARK, markersize=5)
    ax.annotate(f'Wind injection peak:\n$I(t) > I_{{\\mathrm{{SLR}}}}$ (Safe under DLR!)',
                xy=(hours[idx_peak], I_load[idx_peak]), xytext=(hours[idx_peak]-5.2, I_load[idx_peak]+250),
                fontsize=7.2, fontweight='bold', color=C_DARK,
                arrowprops=dict(arrowstyle='->', color=C_DARK, lw=1.0),
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#888888', alpha=0.92))

    ax.set_xlabel('Time of day [Hours]', fontsize=8.5, fontweight='bold')
    ax.set_ylabel('Line Current [A]', fontsize=8.5, fontweight='bold')
    ax.set_xlim(0, 24)
    ax.set_xticks(np.arange(0, 25, 4))
    ax.set_xticklabels(['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'])
    ax.set_ylim(400, 1850)
    ax.tick_params(labelsize=8.0)
    ax.grid(True, ls='--', alpha=0.55)

    ax.legend(loc='upper right', fontsize=7.0, frameon=True, framealpha=0.92, edgecolor='#dddddd')
    plt.tight_layout(pad=0.5)

    out_pdf = 'Lectures/TransmissionLine/images/dlr_vs_slr_24h.pdf'
    out_png = 'Lectures/TransmissionLine/images/dlr_vs_slr_24h.png'
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.savefig(out_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated: {out_pdf} and {out_png}")

if __name__ == '__main__':
    generate_ampacity_vs_wind()
    generate_dlr_vs_slr_24h()
