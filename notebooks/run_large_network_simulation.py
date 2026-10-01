#!/usr/bin/env python3
"""
Run Large Geolocalised European Network Simulation
==================================================
This script executes the complete simulation pipeline:
  1. Loads the 179-bus Oberrhein European benchmark grid with GIS coordinates.
  2. Solves AC Newton-Raphson power flow and displays baseline voltages & line loadings.
  3. Simulates N-1 line outages and distributed generator tripping scenarios.
  4. Runs a 24-hour time-series simulation with demand and solar profiles.
  5. Generates publication-ready figures in notebooks/figures/ and an interactive
     Plotly OpenStreetMap visualization (grid_power_flow_map.html).

Usage:
  python notebooks/run_large_network_simulation.py
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless figure generation

# Add directory to sys.path if running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from large_network_analysis import (
    get_european_network,
    run_baseline_power_flow,
    simulate_line_tripping,
    simulate_gen_tripping,
    run_n1_contingency_screening,
    generate_diurnal_profiles,
    run_timeseries_powerflow,
    plot_voltage_and_loading_profiles,
    plot_contingency_comparison,
    plot_timeseries_dashboard,
    create_interactive_map,
)


def main():
    figures_dir = os.path.join(current_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    print("=" * 80)
    print(" ELEC0447: LARGE GEOLOCALISED EUROPEAN GRID SIMULATION (PANDAPOWER)")
    print(" Benchmark Network: Oberrhein 20 kV (179 Buses, Upper Rhine Region, Germany)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. LOAD NETWORK & RUN BASELINE POWER FLOW
    # -------------------------------------------------------------------------
    print("\n[Step 1] Loading network and solving baseline AC Newton-Raphson power flow...")
    net = get_european_network(network_name="mv_oberrhein", scenario="generation", meshed=True)
    base_res = run_baseline_power_flow(net)

    print(f"  ✓ Power Flow Converged: {base_res['converged']}")
    print(f"  ✓ Grid Topology: {base_res['n_buses']} buses, {base_res['n_lines']} lines, {base_res['n_loads']} loads, {base_res['n_sgens']} solar PV generators")
    print(f"  ✓ Total Demand: {base_res['p_load_mw']:.2f} MW / {base_res['q_load_mvar']:.2f} MVAr")
    print(f"  ✓ Total PV Generation: {base_res['p_sgen_mw']:.2f} MW")
    print(f"  ✓ Substation Grid Exchange: {base_res['p_ext_grid_mw']:.2f} MW ({'Export to HV (Reverse Flow)' if base_res['p_ext_grid_mw'] < 0 else 'Import from HV'})")
    print(f"  ✓ Total Losses: {base_res['p_loss_mw']:.3f} MW (Lines: {base_res['line_loss_mw']:.3f} MW, Trafos: {base_res['trafo_loss_mw']:.3f} MW)")
    print(f"  ✓ Bus Voltages: Min = {base_res['v_min']:.4f} pu (Bus {base_res['v_min_bus']}), Max = {base_res['v_max']:.4f} pu (Bus {base_res['v_max_bus']}), Mean = {base_res['v_mean']:.4f} pu")
    print(f"  ✓ Line Loadings: Max = {base_res['max_loading_percent']:.2f}% (Line {base_res['max_loading_line']}), Mean = {base_res['mean_loading_percent']:.2f}%")
    print(f"  ✓ Under-voltage buses (<0.95 pu): {len(base_res['under_voltage_buses'])} | Over-voltage buses (>1.05 pu): {len(base_res['over_voltage_buses'])}")

    # Save baseline plot
    fig_base_path = os.path.join(figures_dir, "baseline_voltage_loading.png")
    plot_voltage_and_loading_profiles(net, base_res, save_path=fig_base_path)
    print(f"  -> Saved baseline plot: {fig_base_path}")

    # Generate interactive HTML map
    map_html_path = os.path.join(figures_dir, "grid_power_flow_map.html")
    create_interactive_map(net, output_html=map_html_path)
    print(f"  -> Saved interactive GIS map: {map_html_path}")

    # -------------------------------------------------------------------------
    # 2. CONTINGENCY ANALYSIS (N-1 LINE & GENERATOR TRIPPING)
    # -------------------------------------------------------------------------
    print("\n[Step 2] Conducting Contingency Analysis...")

    # A. N-1 Line Screening
    print("  A. Running automated N-1 screening on candidate lines...")
    n1_table = run_n1_contingency_screening(net, top_candidates=8)
    print("\nTop Critical N-1 Line Outages:")
    print(n1_table[["tripped_line", "base_loading_%", "post_max_loading_%", "most_loaded_line", "n_overloaded", "max_loading_increase_%"]].to_string(index=False))

    # Pick the most severe line outage for detailed inspection
    critical_line = int(n1_table.iloc[0]["tripped_line"])
    line_cont_res = simulate_line_tripping(net, critical_line)
    print(f"\n  Detailed Impact for tripping Line {critical_line}:")
    print(f"    - Post-trip max loading: {line_cont_res['max_loading_percent']:.2f}% on Line {line_cont_res['max_loading_line']}")
    print(f"    - Max loading surge on parallel path: +{line_cont_res['max_loading_increase']:.2f}% on Line {line_cont_res['max_loading_increase_line']}")
    print(f"    - Number of newly overloaded lines (>100%): {len(line_cont_res['overloaded_lines'])} {line_cont_res['overloaded_lines']}")

    # B. Generator Tripping Scenario
    print("\n  B. Simulating Renewable Generator Tripping...")
    # Find the top 5 largest PV installations
    top_pv = net.sgen.sort_values(by="p_mw", ascending=False).head(5)
    gen_trip_ids = top_pv.index.tolist()
    total_pv_lost = float(top_pv["p_mw"].sum())
    print(f"    - Tripping cluster of {len(gen_trip_ids)} largest solar PV units (total loss = {total_pv_lost:.2f} MW)")
    gen_cont_res = simulate_gen_tripping(net, gen_trip_ids)

    print(f"    - Pre-trip Substation Active Power: {gen_cont_res['pre_ext_grid_p_mw']:.2f} MW")
    print(f"    - Post-trip Substation Active Power: {gen_cont_res['post_ext_grid_p_mw']:.2f} MW")
    print(f"    - Substation Dispatch Shift: {gen_cont_res['delta_ext_grid_p_mw']:+.2f} MW (HV grid picks up the lost generation)")
    print(f"    - Max Local Voltage Drop: {gen_cont_res['max_voltage_drop']:.4f} pu at Bus {gen_cont_res['max_voltage_drop_bus']}")

    # Save contingency plot
    fig_cont_path = os.path.join(figures_dir, "contingency_impact.png")
    plot_contingency_comparison(net, line_cont_res, gen_cont_res, save_path=fig_cont_path)
    print(f"  -> Saved contingency comparison plot: {fig_cont_path}")

    # -------------------------------------------------------------------------
    # 3. 24-HOUR TIME-SERIES SIMULATION
    # -------------------------------------------------------------------------
    print("\n[Step 3] Running 24-Hour Time-Series Simulation (Demand Evolution + Solar PV Variation)...")
    load_prof, pv_prof, prof_df = generate_diurnal_profiles(n_steps=24)
    ts_results = run_timeseries_powerflow(net, n_steps=24, load_profile=load_prof, pv_profile=pv_prof, pv_scaling=2.0)
    df_ts = ts_results["summary_df"]

    # Detect reverse power flow hours
    rev_hours = df_ts[df_ts["is_reverse_flow"]]["hour"].tolist()
    max_export = float(df_ts["ext_grid_p_mw"].min())
    peak_demand_hour = int(df_ts.loc[df_ts["total_load_p_mw"].idxmax(), "hour"])
    peak_pv_hour = int(df_ts.loc[df_ts["total_pv_p_mw"].idxmax(), "hour"])

    print(f"  ✓ 24 hourly power flows solved successfully.")
    print(f"  ✓ Peak Demand Hour: {peak_demand_hour}:00 ({df_ts['total_load_p_mw'].max():.2f} MW)")
    print(f"  ✓ Peak Solar PV Hour: {peak_pv_hour}:00 ({df_ts['total_pv_p_mw'].max():.2f} MW)")
    if rev_hours:
        print(f"  ✓ Reverse Power Flow detected between {min(rev_hours):02.0f}:00 and {max(rev_hours):02.0f}:00!")
        print(f"    Maximum feed-in export back to the 110 kV transmission grid: {abs(max_export):.2f} MW")
    else:
        print("  ✓ No reverse power flow with this scaling.")

    print(f"  ✓ Voltage Bounds over 24h: [{df_ts['vm_min'].min():.4f} pu, {df_ts['vm_max'].max():.4f} pu]")
    print(f"  ✓ Maximum Line Loading observed over 24h: {df_ts['max_line_loading_%'].max():.2f}%")
    print(f"  ✓ Total Daily Losses: {df_ts['total_losses_mw'].sum():.2f} MWh")

    # Save time-series dashboard
    fig_ts_path = os.path.join(figures_dir, "timeseries_dashboard.png")
    plot_timeseries_dashboard(ts_results, save_path=fig_ts_path)
    print(f"  -> Saved 24h time-series dashboard: {fig_ts_path}")

    print("\n" + "=" * 80)
    print(" SIMULATION COMPLETE!")
    print(f" All outputs generated in: {figures_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()
