#!/usr/bin/env python3
"""
Script to generate and execute the Jupyter Notebook:
notebooks/PST_controlling_parallel_flows.ipynb

Demonstrates the physical principle of controlling parallel path and loop flows
using a Phase-Shifting Transformer (PST / Quadrature Booster) in pandapower.
"""

import os
import sys
import io
import base64
import contextlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat as nbf
import numpy as np
import pandas as pd
import pandapower as pp
import logging
logging.getLogger("pandapower").setLevel(logging.ERROR)

def build_pst_notebook():
    nb = nbf.v4.new_notebook()
    env = {}
    exec_count = 1

    def add_markdown(text):
        nb.cells.append(nbf.v4.new_markdown_cell(text.strip()))

    def add_code(code_str):
        nonlocal exec_count
        code_str = code_str.strip()
        f_out = io.StringIO()
        plt.close("all")
        
        with contextlib.redirect_stdout(f_out):
            # Custom display function to capture DataFrame or HTML prints
            def custom_display(obj):
                if isinstance(obj, pd.DataFrame):
                    print(obj.to_string())
                elif hasattr(obj, "to_string"):
                    print(obj.to_string())
                else:
                    print(repr(obj))
            env["display"] = custom_display
            
            exec(code_str, env)
            
        stdout_str = f_out.getvalue()
        outputs = []
        if stdout_str:
            outputs.append(nbf.v4.new_output(output_type="stream", name="stdout", text=stdout_str))
            
        # Capture matplotlib figures
        figs = [plt.figure(n) for n in plt.get_fignums()]
        for fig in figs:
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode("utf-8")
            outputs.append(nbf.v4.new_output(
                output_type="display_data",
                data={"image/png": img_b64, "text/plain": "<Figure size ...>"}
            ))
        plt.close("all")
        
        cell = nbf.v4.new_code_cell(source=code_str, execution_count=exec_count, outputs=outputs)
        nb.cells.append(cell)
        exec_count += 1

    # -------------------------------------------------------------------------
    # 1. Header & Theoretical Framework
    # -------------------------------------------------------------------------
    add_markdown(
r"""# Controlling Parallel Path & Loop Flows with a Phase-Shifting Transformer (PST)
### Course: ELEC0447 - Analysis of Electric Power and Energy Systems
**Instructor**: Prof. Bertrand Cornélusse (University of Liège)

---

## 1. Physical Principle & Theoretical Motivation

In alternating current (AC) power systems, active power flow is dictated strictly by Kirchhoff's laws and the physical impedance of network branches rather than commercial contracts.

For any transmission branch connecting bus $i$ and bus $j$ with reactance $X_{ij}$ (neglecting small resistances in high-voltage grids):
$$P_{ij} \approx \frac{V_i V_j}{X_{ij}} \sin(\theta_i - \theta_j) \approx \frac{\theta_i - \theta_j}{X_{ij}} \quad \text{[p.u.]}$$

### The Parallel Corridor Dilemma (Transit Flows & Bottle-Necks)
Consider two parallel corridors connecting a generation center (**Area A**) to a demand center (**Area B**):
* **Path 1**: Direct, shorter corridor with **low reactance** $X_1$.
* **Path 2**: Longer, alternative corridor with **higher reactance** $X_2 > X_1$.

```
         Area A (Generator)                       Area B (Load)
            [Bus A]                                  [Bus B]
               |                                        |
               +------- Line 1 (X1) ----- [PST (±α)] ---+   Path 1 (Low X1)
               |                                        |
               +--------------- Line 2 (X2) ------------+   Path 2 (High X2)
               |                                        |
```

### 1. Natural Flow Division without PST ($\alpha = 0$):
Under Kirchhoff's Voltage Law around the closed loop:
$$X_1 P_1 = X_2 P_2 \implies \frac{P_1}{P_2} = \frac{X_2}{X_1}$$
Because $P_1 + P_2 = P_{\text{total}}$:
$$P_1 = P_{\text{total}} \frac{X_2}{X_1 + X_2}, \qquad P_2 = P_{\text{total}} \frac{X_1}{X_1 + X_2}$$

> **The Problem**: Because $X_1 < X_2$, Path 1 naturally attracts a disproportionately large share of power. Path 1 often reaches its thermal rating ($I_{\max}$) and becomes congested while Path 2 remains severely underloaded!

### 2. Controlled Flow Division with a PST ($\alpha \ne 0$):
A **Phase-Shifting Transformer (PST)** (or *Quadrature Booster*) injects an in-quadrature voltage component $\Delta \bar{V}_q \perp \bar{V}$, introducing a controllable phase angle boost $\alpha$.

The voltage angle drop across Path 1 becomes $(\theta_A - \theta_B + \alpha)$, giving in **per-unit (pu)**:
$$p_1(\alpha) \approx \frac{\theta_A - \theta_B + \alpha}{x_1} \quad \text{[pu]}$$
Around the parallel loop:
$$\theta_A - \theta_B = x_2 p_2 = x_1 p_1 - \alpha$$
Substituting $p_2 = p_{\text{total}} - p_1$:
$$(x_1 + x_2) p_1 = x_2 p_{\text{total}} + \alpha$$
In **per-unit (pu)** (where $v_A \approx v_B \approx 1.0\text{ pu}$):
$$\mathbf{p_1(\alpha) = p_{\text{total}} \frac{x_2}{x_1 + x_2} + \frac{\alpha}{x_1 + x_2}} \quad \text{[pu]}$$

### In Physical Units ($\Omega$, kV, MW) — Why $V_n^2$ appears:
When working with physical parameters (reactances $X_1, X_2$ in $\Omega$, total power $P_{\text{total}}$ in $\text{MW}$, and nominal line-to-line voltage $V_n$ in $\text{kV}$), three-phase active power is $P = \frac{V_n^2}{X} \Delta \theta$.
Converting from per-unit using base impedance $Z_{\text{base}} = \frac{V_n^2}{S_{\text{base}}}$:
$$P_{\text{circ}} = p_{\text{circ}} \times S_{\text{base}} = \frac{\alpha_{\text{rad}}}{x_1 + x_2} S_{\text{base}} = \frac{\alpha_{\text{rad}}}{(X_1 + X_2)\frac{S_{\text{base}}}{V_n^2}} S_{\text{base}} = \mathbf{\frac{\alpha_{\text{rad}}}{X_1 + X_2} \cdot V_n^2 \quad \text{[MW]}}$$
* **Dimensional check**: $\left[\frac{V_n^2}{X_1 + X_2} \alpha_{\text{rad}}\right] = \frac{\text{kV}^2}{\Omega} \times \text{rad} = \frac{(10^3 \text{ V})^2}{\Omega} = 10^6 \frac{\text{V}^2}{\Omega} = \mathbf{\text{MW}}$. Without $V_n^2$, $\frac{\alpha}{X}$ would have units of Siemens ($\Omega^{-1}$), not Power!

Therefore, in physical units:
$$\mathbf{P_1(\alpha) = P_{\text{total}} \frac{X_2}{X_1 + X_2} + \frac{\alpha_{\text{rad}}}{X_1 + X_2} \cdot V_n^2 \quad \text{[MW]}}$$
$$\mathbf{P_2(\alpha) = P_{\text{total}} \frac{X_1}{X_1 + X_2} - \frac{\alpha_{\text{rad}}}{X_1 + X_2} \cdot V_n^2 \quad \text{[MW]}}$$

### Real-World Relevance:
In continental Europe, massive wind generation in Northern Germany flows toward industrial load centers in Southern Germany and France. Due to transmission bottlenecks inside Germany, power spills into neighboring grids (Belgium and the Netherlands), creating unintended **transit loop flows**. Transmission System Operators (TSOs like Elia) install high-power $380\text{ kV}$ PSTs on border interconnections (e.g. at **Zandvliet**, **Meerhout**, and **Gramme**) to act as **electrical valves** that protect national grids from cascading overloads."""
    )

    # -------------------------------------------------------------------------
    # 2. Imports & Setup
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 2. Environment Setup & Network Definition

We implement the 2-bus parallel corridor system using **pandapower**:
* **System Nominal Voltage**: $V_n = 380\text{ kV}$.
* **Area A (Sending End)**: Slack bus ($V_A = 1.0\text{ pu}$, $\theta_A = 0^\circ$) representing bulk generation.
* **Area B (Receiving End)**: PQ bus with heavy industrial demand ($P_{\text{load}} = 800\text{ MW}$, $Q_{\text{load}} = 50\text{ MVAR}$).
* **Path 1 (Low Reactance Corridor)**:
  - 50 km transmission line ($r = 0.03\,\Omega/\text{km}$, $x = 0.30\,\Omega/\text{km} \implies X_{\text{line1}} = 15.0\,\Omega$).
  - Thermal rating: $I_{\max} = 0.75\text{ kA} \implies S_{\max, 1} \approx 493.6\text{ MVA}$ ($\approx 490\text{ MW}$).
  - In series with a **380/380 kV PST**: $S_n = 1400\text{ MVA}$, $v_k\% = 5.0\% \implies X_{\text{PST}} \approx 5.16\,\Omega$.
  - Total Path 1 reactance: $X_1 = 15.0 + 5.16 = \mathbf{20.16\,\Omega}$.
* **Path 2 (High Reactance Alternative Corridor)**:
  - 100 km transmission line ($r = 0.03\,\Omega/\text{km}$, $x = 0.30\,\Omega/\text{km} \implies X_2 = \mathbf{30.0\,\Omega}$).
  - Thermal rating: $I_{\max} = 1.00\text{ kA} \implies S_{\max, 2} \approx 658.2\text{ MVA}$ ($\approx 650\text{ MW}$).
* **Total Loop Reactance**: $X_{\text{loop}} = X_1 + X_2 = \mathbf{50.16\,\Omega}$."""
    )

    add_code(
r"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandapower as pp
import logging

# Silence pandapower internal logs
logging.getLogger("pandapower").setLevel(logging.ERROR)

print(f"pandapower version: {pp.__version__}")

def create_parallel_pst_network(load_p_mw=800.0, load_q_mvar=50.0, tap_pos=0):
    # Constructs a 380 kV 2-bus parallel corridor system with a PST on Path 1.
    net = pp.create_empty_network(name="Parallel Corridors with PST")
    Vn = 380.0  # kV
    
    # 1. Buses
    b_a = pp.create_bus(net, vn_kv=Vn, name="Area A (Slack Gen)")
    b_b = pp.create_bus(net, vn_kv=Vn, name="Area B (Load)")
    b_mid = pp.create_bus(net, vn_kv=Vn, name="Path 1 Intermediate Bus")
    
    # 2. Generator and Load
    pp.create_ext_grid(net, bus=b_a, vm_pu=1.0, va_degree=0.0, name="Area A Generation")
    pp.create_load(net, bus=b_b, p_mw=load_p_mw, q_mvar=load_q_mvar, name="Area B Demand")
    
    # 3. Path 1: Line 1 (50 km) + Series PST (1400 MVA, 380/380 kV)
    # Line 1: max_i_ka=0.75 kA (approx 494 MVA thermal limit)
    pp.create_line_from_parameters(
        net, from_bus=b_a, to_bus=b_mid, length_km=50.0,
        r_ohm_per_km=0.03, x_ohm_per_km=0.30, c_nf_per_km=0.0,
        max_i_ka=0.75, name="Path 1 - Line 1 (50 km)"
    )
    
    # PST: 380/380 kV, 1400 MVA, vk=5.0%, tap_step=1.5 deg, 35 positions (+-17)
    pp.create_transformer_from_parameters(
        net, hv_bus=b_mid, lv_bus=b_b, sn_mva=1400.0,
        vn_hv_kv=Vn, vn_lv_kv=Vn, vkr_percent=0.1, vk_percent=5.0,
        pfe_kw=0.0, i0_percent=0.0, shift_degree=0.0,
        tap_side="lv", tap_neutral=0, tap_min=-17, tap_max=17,
        tap_step_degree=1.5, tap_pos=tap_pos, tap_phase_shifter=True,
        name="Path 1 - PST (Quadrature Booster)"
    )
    
    # 4. Path 2: Line 2 (100 km)
    # Line 2: max_i_ka=1.00 kA (approx 658 MVA thermal limit)
    pp.create_line_from_parameters(
        net, from_bus=b_a, to_bus=b_b, length_km=100.0,
        r_ohm_per_km=0.03, x_ohm_per_km=0.30, c_nf_per_km=0.0,
        max_i_ka=1.00, name="Path 2 - Line 2 (100 km)"
    )
    
    return net

net_base = create_parallel_pst_network()
print(f"Network successfully initialized:")
print(f" - Buses: {len(net_base.bus)}")
print(f" - Lines: {len(net_base.line)}")
print(f" - Transformers (PST): {len(net_base.trafo)}")"""
    )

    # -------------------------------------------------------------------------
    # 3. Baseline Power Flow (alpha = 0)
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 3. Baseline Power Flow without Phase Shift ($\alpha = 0^\circ$, Neutral Tap)

Let us solve the baseline AC power flow (`runpp`) with the PST in neutral position ($\alpha = 0^\circ$).
We will inspect how power divides naturally between the two lines."""
    )

    add_code(
r"""# Run baseline AC power flow with angle tracking enabled
pp.runpp(net_base, calculate_voltage_angles=True, numba=False)

print("=" * 75)
print(" BASELINE POWER FLOW RESULTS (alpha = 0 deg, Neutral Tap)")
print("=" * 75)

print("\n--- BUS SUMMARY ---")
bus_summary = net_base.res_bus[["vm_pu", "va_degree", "p_mw", "q_mvar"]].copy()
bus_summary.index = net_base.bus["name"]
print(bus_summary.round(3))

print("\n--- LINE LOADINGS & ACTIVE POWER FLOWS ---")
line_summary = net_base.res_line[["p_from_mw", "q_from_mvar", "p_to_mw", "pl_mw", "loading_percent"]].copy()
line_summary.index = net_base.line["name"]
print(line_summary.round(2))

p1_base = net_base.res_line.loc[0, "p_from_mw"]
p2_base = net_base.res_line.loc[1, "p_from_mw"]
load1_base = net_base.res_line.loc[0, "loading_percent"]
load2_base = net_base.res_line.loc[1, "loading_percent"]

print("\n" + "-" * 75)
print(f"Natural Power Division:")
print(f"  Path 1 (Line 1 + PST): P1 = {p1_base:.1f} MW  --> Loading = {load1_base:.1f}%")
print(f"  Path 2 (Line 2):       P2 = {p2_base:.1f} MW  --> Loading = {load2_base:.1f}%")
print("-" * 75)
if load1_base > 95.0:
    print(f"ALERT: Line 1 is operating near/above its thermal limit ({load1_base:.1f}%)!")
    print(f"       Meanwhile, Path 2 has huge spare capacity ({load2_base:.1f}% loading).")"""
    )

    # -------------------------------------------------------------------------
    # 4. Continuous Sweep of Phase Shift Angle alpha
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 4. Continuous Parameter Sweep: Power Flow as a Function of $\alpha$

We now systematically vary the PST phase shift angle $\alpha$ over a wide range:
$$\alpha \in [-20^\circ, +20^\circ]$$

For each angle $\alpha$:
1. We solve the full non-linear AC Newton-Raphson power flow (`runpp`).
2. We extract active power flows $P_1(\alpha)$, $P_2(\alpha)$, line loadings, system losses, and voltage profiles.
3. We compute the theoretical linear DC power flow approximation:
   $$P_1^{\text{DC}}(\alpha) = P_{\text{total}} \frac{X_2}{X_1 + X_2} + \frac{\alpha_{\text{rad}}}{X_1 + X_2} \cdot V_n^2$$
   $$P_2^{\text{DC}}(\alpha) = P_{\text{total}} \frac{X_1}{X_1 + X_2} - \frac{\alpha_{\text{rad}}}{X_1 + X_2} \cdot V_n^2$$"""
    )

    add_code(
r"""# Reactance calculations
Vn = 380.0
X1 = (50.0 * 0.30) + (0.05 * Vn**2 / 1400.0)  # 20.157 Ohm
X2 = 100.0 * 0.30                              # 30.000 Ohm
X_loop = X1 + X2                               # 50.157 Ohm
P_total = 800.0                                # MW

alpha_degrees = np.linspace(-20.0, 20.0, 81)
sweep_records = []

net_sweep = create_parallel_pst_network()

for alpha in alpha_degrees:
    # In pandapower, positive shift_degree advances HV relative to LV.
    # To match the slide definition P1 = (theta_A - theta_B + alpha)/X1 where
    # a positive alpha boosts Path 1 flow and negative alpha relieves Path 1,
    # we apply shift_degree = -alpha:
    net_sweep.trafo.loc[0, "shift_degree"] = -alpha
    net_sweep.trafo.loc[0, "tap_pos"] = 0
    net_sweep.trafo.loc[0, "tap_phase_shifter"] = False
    
    pp.runpp(net_sweep, calculate_voltage_angles=True, numba=False)
    
    p1 = net_sweep.res_line.loc[0, "p_from_mw"]
    p2 = net_sweep.res_line.loc[1, "p_from_mw"]
    load1 = net_sweep.res_line.loc[0, "loading_percent"]
    load2 = net_sweep.res_line.loc[1, "loading_percent"]
    losses = net_sweep.res_ext_grid.loc[0, "p_mw"] - 800.0
    vb_pu = net_sweep.res_bus.loc[1, "vm_pu"]
    vb_ang = net_sweep.res_bus.loc[1, "va_degree"]
    
    # DC Power Flow Theoretical Formula
    alpha_rad = np.radians(alpha)
    p_circ_dc = (alpha_rad / X_loop) * (Vn**2)
    p1_dc = P_total * (X2 / X_loop) + p_circ_dc
    p2_dc = P_total * (X1 / X_loop) - p_circ_dc
    
    sweep_records.append({
        "alpha_deg": alpha,
        "P1_AC_mw": p1,
        "P2_AC_mw": p2,
        "P1_DC_mw": p1_dc,
        "P2_DC_mw": p2_dc,
        "P_circ_mw": p1 - (P_total * (X2 / X_loop)),
        "loading1_pct": load1,
        "loading2_pct": load2,
        "losses_mw": losses,
        "vb_pu": vb_pu,
        "vb_ang_deg": vb_ang
    })

df_sweep = pd.DataFrame(sweep_records)
print(f"Sweep successfully evaluated {len(df_sweep)} operating points for alpha in [-20 deg, +20 deg].")"""
    )

    # -------------------------------------------------------------------------
    # 5. Visualization: Power Flows, Loading, and Losses
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 5. Visualizing Power Redirection, Thermal Relief & Safe Operating Envelope

We now generate a publication-quality 3-panel dashboard illustrating the physical effects of $\alpha$:
1. **Active Power Sharing $P_1(\alpha)$ vs $P_2(\alpha)$**:
   - Compares the non-linear AC power flow against the linear theoretical DC prediction.
   - Highlights the thermal limit lines for both transmission corridors.
2. **Corridor Loading & Identification of the Safe Operating Window**:
   - Identifies the range of $\alpha$ where neither line exceeds $100\%$ thermal loading.
3. **System Active Losses $P_{\text{loss}}(\alpha)$**:
   - Demonstrates that minimum transmission losses occur near the point of balanced current density."""
    )

    add_code(
r"""fig, axes = plt.subplots(3, 1, figsize=(11, 14), sharex=True)

c1 = "#D32F2F"   # Red for Path 1
c2 = "#1976D2"   # Blue for Path 2
c_dc = "#424242" # Dark gray for DC model

# =========================================================================
# Subplot 1: Active Power Flows vs Alpha
# =========================================================================
ax1 = axes[0]
ax1.plot(df_sweep["alpha_deg"], df_sweep["P1_AC_mw"], color=c1, lw=2.5, label="Path 1 Flow $P_1(\\alpha)$ (AC Power Flow)")
ax1.plot(df_sweep["alpha_deg"], df_sweep["P2_AC_mw"], color=c2, lw=2.5, label="Path 2 Flow $P_2(\\alpha)$ (AC Power Flow)")
ax1.plot(df_sweep["alpha_deg"], df_sweep["P1_DC_mw"], color=c1, ls="--", lw=1.5, alpha=0.7, label="Path 1 Linear DC Model")
ax1.plot(df_sweep["alpha_deg"], df_sweep["P2_DC_mw"], color=c2, ls="--", lw=1.5, alpha=0.7, label="Path 2 Linear DC Model")

# Thermal limits
ax1.axhline(493.6, color=c1, ls=":", lw=1.5, label="Line 1 Thermal Limit (494 MVA)")
ax1.axhline(658.2, color=c2, ls=":", lw=1.5, label="Line 2 Thermal Limit (658 MVA)")
ax1.axvline(0, color="gray", ls="-.", lw=1.0, alpha=0.6, label="Natural State ($\\alpha = 0^\\circ$)")
ax1.axhline(0, color="black", lw=0.8, alpha=0.4)

ax1.set_ylabel("Active Power Flow [MW]", fontsize=11, fontweight="bold")
ax1.set_title("Physical Principle: Controlling Parallel Path & Loop Flows with PST", fontsize=13, fontweight="bold", pad=10)
ax1.grid(True, linestyle="--", alpha=0.6)
ax1.legend(loc="center right", fontsize=8.5, framealpha=0.95)
ax1.set_ylim(-450, 1250)

# Annotations
ax1.annotate("Natural state ($\\alpha = 0^\\circ$):\nLine 1 near overload (481 MW)",
             xy=(0, 481.2), xytext=(2.5, 330),
             arrowprops=dict(arrowstyle="->", color=c1, lw=1.5),
             fontsize=9, fontweight="semibold", bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=c1, alpha=0.9))

ax1.annotate("Optimal Balance ($\\alpha = -3^\\circ$):\nBoth lines at ~70% loading",
             xy=(-3.0, 333.8), xytext=(-14, 150),
             arrowprops=dict(arrowstyle="->", color="#388E3C", lw=1.5),
             fontsize=9, fontweight="semibold", bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#388E3C", alpha=0.9))

ax1.annotate("Loop Flow Reversal ($P_2 < 0$):\nPower loops back from B to A!",
             xy=(10, -189), xytext=(3, -350),
             arrowprops=dict(arrowstyle="->", color=c2, lw=1.5),
             fontsize=9, fontweight="semibold", bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=c2, alpha=0.9))

# =========================================================================
# Subplot 2: Thermal Loading & Safe Operating Window
# =========================================================================
ax2 = axes[1]
ax2.plot(df_sweep["alpha_deg"], df_sweep["loading1_pct"], color=c1, lw=2.5, label="Line 1 Loading [%]")
ax2.plot(df_sweep["alpha_deg"], df_sweep["loading2_pct"], color=c2, lw=2.5, label="Line 2 Loading [%]")
ax2.axhline(100.0, color="darkred", ls="-", lw=1.8, label="Thermal Overload Limit (100%)")
ax2.axvline(0, color="gray", ls="-.", lw=1.0, alpha=0.6)

# Find safe operating window where both lines <= 100%
safe_mask = (df_sweep["loading1_pct"] <= 100.0) & (df_sweep["loading2_pct"] <= 100.0)
alpha_min_safe = df_sweep.loc[safe_mask, "alpha_deg"].min()
alpha_max_safe = df_sweep.loc[safe_mask, "alpha_deg"].max()

ax2.axvspan(alpha_min_safe, alpha_max_safe, color="#4CAF50", alpha=0.20,
            label=f"Safe Operating Window [{alpha_min_safe:.1f}$^\\circ$, {alpha_max_safe:.1f}$^\\circ$]")

ax2.set_ylabel("Thermal Loading [%]", fontsize=11, fontweight="bold")
ax2.set_title("Corridor Loading & Identification of the Safe Operating Window", fontsize=12, fontweight="bold", pad=8)
ax2.grid(True, linestyle="--", alpha=0.6)
ax2.legend(loc="upper right", fontsize=9, framealpha=0.95)
ax2.set_ylim(0, 260)

# =========================================================================
# Subplot 3: Transmission Losses
# =========================================================================
ax3 = axes[2]
ax3.plot(df_sweep["alpha_deg"], df_sweep["losses_mw"], color="#6A1B9A", lw=2.5, label="Total System Losses $P_{\\text{loss}}$ [MW]")
min_loss_idx = df_sweep["losses_mw"].idxmin()
min_loss_alpha = df_sweep.loc[min_loss_idx, "alpha_deg"]
min_loss_val = df_sweep.loc[min_loss_idx, "losses_mw"]
ax3.plot(min_loss_alpha, min_loss_val, marker="o", color="#E91E63", markersize=8,
         label=f"Minimum Loss Point: {min_loss_val:.2f} MW at $\\alpha = {min_loss_alpha:.1f}^\\circ$")

ax3.set_xlabel("PST Phase Shift Angle $\\alpha$ [degrees]", fontsize=11, fontweight="bold")
ax3.set_ylabel("Active Losses [MW]", fontsize=11, fontweight="bold")
ax3.set_title("Impact of Phase Shift on Transmission Losses ($I^2 R$ Optimization)", fontsize=12, fontweight="bold", pad=8)
ax3.grid(True, linestyle="--", alpha=0.6)
ax3.legend(loc="upper center", fontsize=9, framealpha=0.95)

plt.tight_layout()
plt.show()"""
    )

    # -------------------------------------------------------------------------
    # 6. Discrete Tap Operation (Belgian Grid Standard)
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 6. Discrete Tap Operation (Real-World Belgian Grid Standard)

In commercial transmission practice (e.g. Belgian TSO Elia at Zandvliet, Meerhout, and Gramme), PSTs do not rotate continuously. They are equipped with **On-Load Tap Changers (OLTC)** operating on discrete symmetrical tap positions:
* **Total Tap Positions**: 35 positions ($-17 \le \text{tap} \le +17$, with tap 0 being neutral).
* **Step Size**: $1.5^\circ$ per tap position (giving a total range of $\pm 25.5^\circ$).

Let us simulate integer tap positions from $-10$ to $+10$ and construct the operational dispatch table:"""
    )

    add_code(
r"""net_tap = create_parallel_pst_network()
tap_positions = list(range(-10, 11))
tap_records = []

for tap in tap_positions:
    net_tap.trafo.loc[0, "tap_pos"] = tap
    net_tap.trafo.loc[0, "tap_phase_shifter"] = True
    pp.runpp(net_tap, calculate_voltage_angles=True, numba=False)
    
    alpha_deg = tap * 1.5
    p1 = net_tap.res_line.loc[0, "p_from_mw"]
    p2 = net_tap.res_line.loc[1, "p_from_mw"]
    l1 = net_tap.res_line.loc[0, "loading_percent"]
    l2 = net_tap.res_line.loc[1, "loading_percent"]
    
    status = "SAFE" if (l1 <= 100.0 and l2 <= 100.0) else ("OVERLOAD (Line 1)" if l1 > 100.0 else "OVERLOAD (Line 2)")
    
    tap_records.append({
        "Tap": tap,
        "Shift alpha [deg]": alpha_deg,
        "P1 (Path 1) [MW]": round(p1, 1),
        "P2 (Path 2) [MW]": round(p2, 1),
        "Loading Line 1 [%]": round(l1, 1),
        "Loading Line 2 [%]": round(l2, 1),
        "Status": status
    })

df_taps = pd.DataFrame(tap_records)
print("=== DISCRETE TAP DISPATCH TABLE (1.5 deg / step) ===")
print(df_taps.to_string(index=False))"""
    )

    # -------------------------------------------------------------------------
    # 7. Discrete Tap Bar Chart
    # -------------------------------------------------------------------------
    add_markdown(
r"""### Visualizing Power Reallocation per Tap Step:"""
    )

    add_code(
r"""fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(df_taps))
width = 0.38

rects1 = ax.bar(x - width/2, df_taps["P1 (Path 1) [MW]"], width, label="Path 1 Flow (Line 1 + PST)", color="#D32F2F", alpha=0.85)
rects2 = ax.bar(x + width/2, df_taps["P2 (Path 2) [MW]"], width, label="Path 2 Flow (Line 2)", color="#1976D2", alpha=0.85)

ax.axhline(493.6, color="#D32F2F", ls="--", lw=1.3, label="Line 1 Thermal Limit (494 MW)")
ax.axhline(658.2, color="#1976D2", ls="--", lw=1.3, label="Line 2 Thermal Limit (658 MW)")
ax.axhline(0, color="black", lw=0.8, alpha=0.5)

ax.set_xticks(x)
ax.set_xticklabels([f"Tap {t}\n({a:+.1f}°)" for t, a in zip(df_taps["Tap"], df_taps["Shift alpha [deg]"])], fontsize=8)
ax.set_ylabel("Active Power [MW]", fontsize=11, fontweight="bold")
ax.set_title("Discrete Tap Operation: Active Power Reallocation and Congestion Relief", fontsize=12, fontweight="bold")
ax.grid(True, axis="y", linestyle="--", alpha=0.5)
ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
plt.tight_layout()
plt.show()"""
    )

    # -------------------------------------------------------------------------
    # 8. Sensitivity Analysis (dP / d_alpha)
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 7. Mathematical Sensitivity Verification ($\frac{dP_1}{d\alpha}$)

How sensitive is the power flow to changes in the PST phase shift angle?
We compare:
1. **Theoretical DC Power Flow Sensitivity**:
   $$\left(\frac{dP_1}{d\alpha}\right)_{\text{DC}} = \frac{V_n^2}{X_1 + X_2} \times \left(\frac{\pi}{180}\right) \quad \text{[MW / degree]}$$
2. **Simulated AC Power Flow Sensitivity**:
   $$\left(\frac{\Delta P_1}{\Delta \alpha}\right)_{\text{AC}} = \frac{P_1(\text{Tap } 0) - P_1(\text{Tap } -1)}{1.5^\circ}$$"""
    )

    add_code(
r"""# Theoretical DC sensitivity
sensitivity_dc = (Vn**2 / X_loop) * (np.pi / 180.0)

# Numerical AC sensitivity around alpha = 0 (from Tap 0 and Tap -1)
p1_tap0 = df_taps.loc[df_taps["Tap"] == 0, "P1 (Path 1) [MW]"].values[0]
p1_tap_minus1 = df_taps.loc[df_taps["Tap"] == -1, "P1 (Path 1) [MW]"].values[0]
delta_p = p1_tap0 - p1_tap_minus1
delta_alpha = 1.5  # degrees
sensitivity_ac = delta_p / delta_alpha

print("=" * 70)
print(" SENSITIVITY VALIDATION (dP1 / d_alpha)")
print("=" * 70)
print(f"Analytical DC Sensitivity: {sensitivity_dc:.2f} MW / degree  ({sensitivity_dc * 1.5:.2f} MW per 1.5 deg tap step)")
print(f"AC Simulation Sensitivity: {sensitivity_ac:.2f} MW / degree  ({delta_p:.2f} MW per 1.5 deg tap step)")
accuracy = (1.0 - abs(sensitivity_ac - sensitivity_dc) / sensitivity_dc) * 100.0
print(f"Model Agreement:           {accuracy:.2f}%")
print("=" * 70)"""
    )

    # -------------------------------------------------------------------------
    # 9. Final Summary (as required by notebook-guidance)
    # -------------------------------------------------------------------------
    add_markdown(
r"""---
## 8. Summary of Findings

### Q&A

* **How does a Phase-Shifting Transformer (PST) control power flow without generation redispatch?**
  A PST injects an in-quadrature voltage component $\Delta \bar{V}_q \perp \bar{V}$ into the series path, introducing an angular phase displacement $\alpha$. This phase shift modifies the loop voltage balance and drives an active circulating loop flow $P_{\text{circ}} = \alpha / (X_1 + X_2)$. By steering power from low-impedance congested corridors into higher-impedance underutilized paths, the TSO relieves branch overloads without modifying generator power outputs.

* **What is the difference between a negative and a positive phase shift in this configuration?**
  - **Negative phase shift ($\alpha < 0$, e.g. Taps $-1$ to $-4$):** "Closes the valve" on Path 1, relieving Line 1 and pushing power into Path 2.
  - **Positive phase shift ($\alpha > 0$, e.g. Taps $+1$ to $+10$):** "Opens the valve" on Path 1, pulling even more flow into Path 1. Beyond $\alpha \approx +6.8^\circ$ (Tap $+5$), the circulating flow exceeds the load drawn by Area B, forcing power on Path 2 to reverse direction and loop back to Area A ($P_2 < 0$).

### Data Analysis Key Findings

* **Natural Division at $\alpha = 0^\circ$ (Tap 0):** Path 1 naturally absorbs **$481.2\text{ MW}$ ($98.4\%$ loading)**, operating at the verge of thermal overload because its reactance ($20.16\,\Omega$) is substantially lower than Path 2 ($30.0\,\Omega$), which carries only **$323.6\text{ MW}$ ($49.5\%$ loading)**.
* **Optimal Balancing Point (Tap $-2$, $\alpha = -3.0^\circ$):** Shifting the PST to Tap $-2$ relieves Line 1 down to **$333.8\text{ MW}$ ($69.3\%$ loading)** while utilizing Path 2 up to **$472.2\text{ MW}$ ($72.0\%$ loading)**, achieving near-perfect thermal equilibrium across both corridors.
* **Safe Operating Window:** Both parallel lines operate safely below $100\%$ thermal loading within the tap window **$\text{Tap } -4 \le \text{tap} \le \text{Tap } 0$** (corresponding to $-6.0^\circ \le \alpha \le 0.0^\circ$).
* **Linear Sensitivity:** The transfer sensitivity is **$49.25\text{ MW / degree}$** (approx. **$73.9\text{ MW}$ per $1.5^\circ$ tap step**), matching the analytical DC linear formula ($50.25\text{ MW/deg}$) with **$98.01\%$ accuracy**.
* **Loss Optimization vs. Thermal Relief Tradeoff:** System transmission losses reach a global minimum of **$4.77\text{ MW}$** at $\alpha \approx +1.0^\circ$ because Line 1 has half the resistance of Line 2 ($1.5\,\Omega$ vs $3.0\,\Omega$). However, operating at minimum loss pushes Line 1 to $108.3\%$ thermal overload! Shifting to Tap $-2$ ($\alpha = -3.0^\circ$) safely balances corridor loadings at $\approx 70\%$ with only a minor loss penalty ($+0.7\text{ MW}$, total losses $5.45\text{ MW}$).

### Insights or Next Steps

* **Operational Insight:** Phase-shifting transformers provide Transmission System Operators with rapid, non-destructive, and cost-effective congestion control. They eliminate the need for out-of-merit fossil/nuclear generation redispatch (which can cost millions of euros per day).
* **Next Steps:**
  1. Investigate closed-loop automated PST tap control under dynamic contingency conditions ($N-1$ line tripping).
  2. Extend this 2-bus parallel corridor model to the multi-node meshed Belgian grid, simulating the real border PSTs at Zandvliet, Meerhout, and Gramme during German offshore wind export peaks."""
    )

    # -------------------------------------------------------------------------
    # Save Notebook
    # -------------------------------------------------------------------------
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "PST_controlling_parallel_flows.ipynb")
    with open(out_file, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"\nSuccessfully generated and saved notebook to:\n  {out_file}")
    print(f"Total cells: {len(nb.cells)} ({sum(1 for c in nb.cells if c.cell_type == 'code')} code cells, {sum(1 for c in nb.cells if c.cell_type == 'markdown')} markdown cells)")

if __name__ == "__main__":
    build_pst_notebook()
