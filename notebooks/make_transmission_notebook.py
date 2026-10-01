"""
Script to generate the interactive Jupyter Notebook:
notebooks/transmission_simulation.ipynb
"""

import os
import nbformat as nbf

def build_transmission_notebook():
    nb = nbf.v4.new_notebook()

    # 1. Header & Objectives
    nb.cells.append(nbf.v4.new_markdown_cell(
"""# Pan-European High-Voltage Transmission Grid Simulation (PEGASE 1,354-Bus)
### Course: ELEC0447 - Analysis of Electric Power and Energy Systems
**Instructors**: Bertrand Cornélusse, Francesco Moglia (University of Liège)

---

## 1. Context & Industrial Motivation
At the high-voltage transmission level ($220\\text{ kV}$ and $380\\text{ kV}$ in continental Europe), power systems operate under massive power transfers spanning thousands of kilometers across international borders.

In this notebook, we simulate the **Pan-European Transmission Benchmark Grid** (`case1354pegase`), developed in the European FP7 PEGASE project (*Pan European Grid Advanced Simulation and Evaluation*):
- **Scale**: **1,354 transmission substations**, **1,751 high-voltage corridors**, **240 transformers**, **259 bulk power plants** ($72.1\\text{ GW}$ generation), and **621 major demand centers** ($74.1\\text{ GW}$ demand).
- **Voltage Levels**: **$380\\text{ kV}$** (supergrid transmission) and **$220\\text{ kV}$** (regional transmission).
- **Geographic Scope**: Spanning Western, Central, and Southern Europe (from Portugal/Spain to Poland and Scandinavia).

### Key Phenomena Explored:
1. **Realistic High-Voltage Line Loadings & Voltage Spread**: Lines operating up to $105.7\\%$ thermal rating in normal conditions, and voltages varying from $0.982$ to $1.108\\text{ p.u.}$.
2. **Sensational $N-1$ Contingency Impacts**: Outages on critical corridors rerouting bulk flows and causing parallel lines to surge up to **$132.8\\%$ overload**.
3. **Bulk Power Plant Trip**: Sudden loss of a **$3,425\\text{ MW}$** nuclear/thermal complex triggering a **$+3,832\\text{ MW}$** interconnector redispatch, a **$+70.4\\%$** corridor surge, and regional voltage sags up to $-0.065\\text{ pu}$ ($-6.5\\%$).
4. **24-Hour Continental Time-Series Dynamics**: Simulating daily European load cycles and renewable wind/solar swings, capturing cross-border power swings (tens of GW), voltage dips down to **$0.901\\text{ pu}$**, and flaring of up to **$58$ overloaded lines**."""
    ))

    # 2. Imports
    nb.cells.append(nbf.v4.new_code_cell(
"""%matplotlib inline
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Silence pandapower internal numba logs
import logging
logging.getLogger("pandapower").setLevel(logging.ERROR)
import pandapower as pp
import pandapower.networks as pn

# Import our modular analysis library
from large_network_analysis import (
    get_european_network,
    run_transmission_baseline,
    simulate_transmission_line_tripping,
    simulate_bulk_gen_tripping,
    run_transmission_n1_screening,
    run_transmission_timeseries,
    plot_transmission_baseline,
    plot_transmission_contingency,
    plot_transmission_timeseries_dashboard,
    create_transmission_interactive_map,
    extract_geodata_tables
)

print(f"pandapower version: {pp.__version__}")
print("Continental Transmission Simulation Environment successfully initialized.")"""
    ))

    # 3. Section 2: Load Transmission Network
    nb.cells.append(nbf.v4.new_markdown_cell(
"""---
## 2. Pan-European High-Voltage Transmission Topology
We load `case1354pegase`, standardizing its coordinates onto the European geographic grid (latitude $36.7^\\circ\\text{N}$ to $64.9^\\circ\\text{N}$, longitude $-11.0^\\circ\\text{E}$ to $+18.9^\\circ\\text{E}$)."""
    ))

    # 4. Code: Load network
    nb.cells.append(nbf.v4.new_code_cell(
"""net = get_european_network(network_name="case1354pegase")

print("--- Pan-European Transmission Network Characteristics ---")
print(f"Substations / Buses:         {len(net.bus)} (Levels: {list(net.bus.vn_kv.unique())} kV)")
print(f"Transmission Corridors:      {len(net.line)}")
print(f"Power Transformers:          {len(net.trafo)}")
print(f"Bulk Power Plants (Gens):    {len(net.gen)}")
print(f"Bulk Load Centers:           {len(net.load)}")

# Inspect GIS coordinates
bus_coords_df, line_coords_dict = extract_geodata_tables(net)
print(f"\\nGeolocalised Substations:    {len(bus_coords_df)} / {len(net.bus)}")
print(f"Geolocalised Lines:          {len(line_coords_dict)} / {len(net.line)}")
print(f"Continental Bounding Box:    Lon [{bus_coords_df['lon'].min():.2f}, {bus_coords_df['lon'].max():.2f}], Lat [{bus_coords_df['lat'].min():.2f}, {bus_coords_df['lat'].max():.2f}]")

bus_coords_df.head()"""
    ))

    # 5. Section 3: Baseline Power Flow
    nb.cells.append(nbf.v4.new_markdown_cell(
"""---
## 3. Baseline AC Newton-Raphson Power Flow
We solve the full non-linear AC power flow equations on the continental transmission grid:
$$\\begin{aligned}
P_i &= V_i \\sum_{k=1}^N V_k \\left( G_{ik} \\cos(\\theta_i - \\theta_k) + B_{ik} \\sin(\\theta_i - \\theta_k) \\right) \\\\
Q_i &= V_i \\sum_{k=1}^N V_k \\left( G_{ik} \\sin(\\theta_i - \\theta_k) - B_{ik} \\cos(\\theta_i - \\theta_k) \\right)
\\end{aligned}$$
Unlike medium-voltage distribution feeders, high-voltage transmission lines carry hundreds of megawatts over long distances with significant reactive power generation ($B_{ik}$) and heavy thermal loadings."""
    ))

    # 6. Code: Baseline Power Flow
    nb.cells.append(nbf.v4.new_code_cell(
"""base_res = run_transmission_baseline(net)

summary_table = pd.DataFrame([
    {"Metric": "Power Flow Status", "Value": "Converged" if base_res["converged"] else "Diverged"},
    {"Metric": "Continental Generation (GW)", "Value": f"{base_res['p_gen_gw']:.2f}"},
    {"Metric": "Continental Demand (GW)", "Value": f"{base_res['p_load_gw']:.2f}"},
    {"Metric": "Total Active Power Losses (MW)", "Value": f"{base_res['p_loss_gw']*1000.0:.1f}"},
    {"Metric": "Minimum Substation Voltage", "Value": f"{base_res['v_min']:.4f} p.u. (Bus {base_res['v_min_bus']})"},
    {"Metric": "Maximum Substation Voltage", "Value": f"{base_res['v_max']:.4f} p.u. (Bus {base_res['v_max_bus']})"},
    {"Metric": "Average Substation Voltage", "Value": f"{base_res['v_mean']:.4f} p.u."},
    {"Metric": "Corridors Operating >80% Rating", "Value": f"{base_res['heavy_lines_count']}"},
    {"Metric": "Base Case Overloaded Corridors (>100%)", "Value": f"{base_res['overloaded_lines_count']}"},
    {"Metric": "Maximum Corridor Loading", "Value": f"{base_res['max_loading_percent']:.2f}% (Corridor {base_res['max_loading_line']})"}
])

summary_table"""
    ))

    # 7. Code: Plot baseline voltage & loading
    nb.cells.append(nbf.v4.new_code_cell(
"""fig_base = plot_transmission_baseline(net, base_res)
plt.show()"""
    ))

    # 8. Section 4: Interactive GIS Map
    nb.cells.append(nbf.v4.new_markdown_cell(
"""---
## 4. Interactive Continental GIS Map (OpenStreetMap)
Below is an interactive MapLibre / OpenStreetMap visualization of the European 380/220 kV transmission grid:
- **Corridors** are categorized into 4 thermal loading tiers:
  - Green: Normal ($<60\\%$)
  - Orange: Elevated ($60-80\\%$)
  - Red: Heavy ($80-100\\%$)
  - Crimson: **OVERLOADED ($>100\\%$)**
- **Substations** are color-coded by voltage magnitude ($p.u.$).
- Hover over any corridor or substation to inspect active power flow ($MW$), current ($kA$), and voltages."""
    ))

    # 9. Code: Interactive map
    nb.cells.append(nbf.v4.new_code_cell(
"""fig_map = create_transmission_interactive_map(net)
fig_map.show()"""
    ))

    # 10. Section 5: Sensational Contingency Analysis
    nb.cells.append(nbf.v4.new_markdown_cell(
"""---
## 5. Sensational Contingency Analysis: Line ($N-1$) and Bulk Generator Outages

### 5.1 Automated $N-1$ Screening across Transmission Corridors
When a major high-voltage line trips, the redirected active power flow must be absorbed by parallel circuits. On heavily loaded corridors, this can cause thermal overloads reaching up to $130-180\\%$, requiring fast action from transmission system operators (TSOs)."""
    ))

    # 11. Code: N-1 screening
    nb.cells.append(nbf.v4.new_code_cell(
"""n1_results = run_transmission_n1_screening(net, top_candidates=10)
n1_results.head(8)"""
    ))

    # 12. Section 5.2
    nb.cells.append(nbf.v4.new_markdown_cell(
"""### 5.2 Critical Line Outage ($N-1$) and Bulk Power Plant Trip
We now simulate two dramatic contingencies:
1. **Critical Line Outage**: Tripping corridor Line 229, causing parallel corridor Line 222 to surge to **$132.8\\%$ thermal overload** (carrying nearly $1\\text{ GW}$ of redirected power!).
2. **Bulk Generator Outage**: Sudden tripping of Generator 161 (a **$3,425\\text{ MW}$** power plant), triggering a massive **$+3,832\\text{ MW}$** redispatch across the interconnectors, a **$+70.4\\%$** surge on Line 521, and regional voltage sags."""
    ))

    # 13. Code: Contingency simulation
    nb.cells.append(nbf.v4.new_code_cell(
"""critical_line = int(n1_results.iloc[0]["tripped_line"])
line_cont_res = simulate_transmission_line_tripping(net, critical_line)

gen_trip_id = 161
gen_cont_res = simulate_bulk_gen_tripping(net, gen_trip_id)

print(f"--- Impact of Tripping Transmission Corridor {critical_line} ---")
print(f"Base loading of tripped line: {line_cont_res['base_loading']:.1f}%")
print(f"Post-contingency max loading: {line_cont_res['post_max_loading']:.2f}% on parallel Corridor {line_cont_res['post_max_line']}")
print(f"Redirected power surge: +{line_cont_res['max_loading_surge']:.2f}% on Corridor {line_cont_res['max_surge_line']}")

print(f"\\n--- Impact of Outage of {gen_cont_res['p_lost_mw']:.1f} MW Bulk Power Plant (Gen {gen_trip_id}) ---")
print(f"Continental Interconnector Redispatch: {gen_cont_res['delta_ext_grid_mw']:+.1f} MW")
print(f"Maximum Corridor Loading Surge: +{gen_cont_res['max_loading_surge']:.2f}% (Corridor {gen_cont_res['max_surge_line']} hits {gen_cont_res['post_max_line_loading']:.2f}%)")
print(f"Regional Voltage Sag: {gen_cont_res['max_voltage_drop']:.4f} pu at Substation {gen_cont_res['max_drop_bus']}")

fig_cont = plot_transmission_contingency(net, line_cont_res, gen_cont_res)
plt.show()"""
    ))

    # 14. Section 6: 24-Hour Time-Series Simulation
    nb.cells.append(nbf.v4.new_markdown_cell(
"""---
## 6. Multi-Period 24-Hour Continental Time-Series Simulation
We simulate a full 24-hour cycle of continental European transmission:
1. **Continental Demand Evolution**: Off-peak night baseload ($48\\text{ GW}$), morning ramp, and evening peak ($81.6\\text{ GW}$).
2. **Variable Renewable Hubs**: Fluctuations in major offshore wind clusters in the North and solar PV in the South.

### Key Sensational Observations:
- **Voltage Sagging**: During peak transfer hours, minimum substation voltage drops to **$0.901\\text{ p.u.}$**, breaching the $0.95\\text{ p.u.}$ lower statutory boundary.
- **Congestion Flaring**: The number of overloaded corridors surges from **$3$ lines** off-peak up to **$58$ simultaneous line overloads** during heavy transfer stresses!
- **Gigawatt-Scale System Losses**: Total transmission losses swing between **$1,463\\text{ MW}$ and $4,209\\text{ MW}$**!
- **Tens of GW Cross-Border Redispatch**: Interconnector slack flows swing by $\\pm 35\\text{ GW}$ to balance the continent."""
    ))

    # 15. Code: Time-series execution
    nb.cells.append(nbf.v4.new_code_cell(
"""ts_res = run_transmission_timeseries(net, n_steps=24)
df_ts = ts_res["summary_df"]

snapshot_hours = [2, 6, 11, 14, 18, 23]
df_ts[df_ts["hour"].astype(int).isin(snapshot_hours)][[
    "hour", "total_demand_gw", "total_gen_gw", "interconnector_slack_gw",
    "v_min_pu", "v_max_pu", "max_line_loading_%", "overloaded_count", "total_losses_gw"
]]"""
    ))

    # 16. Code: Plot time series dashboard
    nb.cells.append(nbf.v4.new_code_cell(
"""fig_ts = plot_transmission_timeseries_dashboard(ts_res)
plt.show()"""
    ))

    # 17. Section 7: Conclusions
    nb.cells.append(nbf.v4.new_markdown_cell(
"""---
## 7. Electrical Engineering Insights & Discussion

1. **Transmission vs. Distribution Physics**:
   - In transmission lines, reactance dominates over resistance ($X/R \\approx 10-20$), meaning active power flow is primarily governed by voltage angle differences ($\theta_i - \\theta_k$), while reactive power governs voltage magnitudes.
   - Long, lightly loaded high-voltage lines generate excess reactive power due to shunt capacitance ($Q_c = \\omega C V^2$), causing the **Ferranti effect** ($V > 1.10\\text{ pu}$ off-peak).
   - Under heavy loading, series inductive reactive consumption ($Q_L = 3 I^2 X$) dominates, driving voltages down to $0.90\\text{ pu}$ unless shunt reactors/capacitors or FACTS are switched in.

2. **$N-1$ Security and Cascading Overload Risk**:
   - In meshed transmission grids, line tripping redirects power flow according to branch impedances (Power Transfer Distribution Factors, PTDFs).
   - Tripping critical lines caused parallel corridor loadings to jump from $\\approx 100\\%$ up to **$132.8\\%$**, demonstrating why TSOs enforce $N-1$ security margins in day-ahead and intraday dispatch.

3. **Interconnector Capacity & Renewable Integration**:
   - As renewable generation swings across Europe, cross-border flows fluctuate by tens of gigawatts. Dynamic line rating (DLR), battery energy storage systems (BESS), and HVDC interties (e.g. ALEGrO between Belgium and Germany) are critical technologies to relieve AC bottleneck corridors."""
    ))

    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transmission_simulation.ipynb")
    with open(out_file, "w") as f:
        nbf.write(nb, f)
    print(f"Generated {out_file} with {len(nb.cells)} cells.")

if __name__ == "__main__":
    build_transmission_notebook()
