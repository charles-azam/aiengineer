"""
Thermal Energy Storage System Design Document.
"""
from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from epyr.tools_units import Quantity
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS
from epyr.parameters_materials import (
    MOLTEN_SALT, SOLID_CERAMIC, HIGH_TEMP_CERAMIC, 
    MOLTEN_METAL, PHASE_CHANGE_MATERIAL
)
from epyr.parameters_industrial_applications import (
    FOOD_APPLICATIONS, CHEMICAL_APPLICATIONS, METAL_APPLICATIONS,
    PAPER_APPLICATIONS, CEMENT_APPLICATIONS, TEXTILE_APPLICATIONS,
    ALL_INDUSTRIAL_APPLICATIONS
)
from epyr.systems_thermal_storage import (
    thermal_storage_system, thermal_storage_medium,
    containment_system, heat_exchanger_system,
    control_system, integration_system
)
from epyr.simulation_thermal_storage import (
    calculate_energy_content, calculate_heat_loss,
    simulate_charging, simulate_discharging,
    calculate_round_trip_efficiency, compare_materials,
    simulate_full_cycle
)
from epyr.simulation_economics import (
    calculate_capex, calculate_annual_opex, calculate_lcoe,
    calculate_payback_period, calculate_roi, carbon_emission_reduction
)

import pandas as pd
import numpy as np

print("Loading design document")

# Document configuration
config = DocumentConfig(
    title="Thermal Energy Storage System Design Report",
    author="EPYR Engineering Team",
    date="2025-06-02"
)
display(config)

# Title and Executive Summary
display(Title("# Thermal Energy Storage System Design"))

display(Title("## Executive Summary"))
display(
    "EPYR has developed an innovative high-temperature thermal energy storage (TES) system "
    "designed to address the growing need for efficient energy storage solutions in industrial "
    "applications. This comprehensive design report details our modular, scalable TES system "
    "that can store excess energy as heat and deliver it on demand to various industrial processes."
    "\n\n"
    "Our system achieves a round-trip efficiency of over 90%, with storage capacities "
    f"starting at {THERMAL_STORAGE_PARAMS.storage_capacity} and maximum operating temperatures "
    f"of {THERMAL_STORAGE_PARAMS.max_temperature}. The design incorporates advanced materials "
    "including molten salts, ceramics, and phase change materials to optimize energy density "
    "and thermal performance."
    "\n\n"
    "This report outlines the system architecture, material selection rationale, performance "
    "simulations, integration pathways with industrial processes, and economic analysis. "
    "The EPYR TES system represents a significant advancement in industrial energy storage "
    "technology, offering both economic and environmental benefits through improved energy "
    "efficiency and reduced carbon emissions."
)

# Introduction and Background
display(Title("## Introduction and Background"))
display(
    "### The Need for Thermal Energy Storage"
    "\n\n"
    "Industrial processes account for approximately one-third of global energy consumption, "
    "with a significant portion used for thermal applications. As industries face increasing "
    "pressure to decarbonize operations and manage energy costs, thermal energy storage (TES) "
    "systems offer a promising solution by enabling:"
    "\n\n"
    "- Time-shifting of energy consumption to reduce peak demand charges"
    "\n"
    "- Integration of variable renewable energy sources"
    "\n"
    "- Recovery and utilization of waste heat"
    "\n"
    "- Improved process stability and reliability"
    "\n"
    "- Reduced carbon emissions through efficiency improvements"
    "\n\n"
    "### Current State of Technology"
    "\n\n"
    "Existing TES technologies include sensible heat storage (water tanks, molten salts), "
    "latent heat storage (phase change materials), and thermochemical storage. Each approach "
    "offers distinct advantages and limitations in terms of energy density, operating temperature "
    "range, cost, and complexity."
    "\n\n"
    "The EPYR TES system builds upon these foundations while addressing key limitations through "
    "innovative material combinations, advanced heat exchanger designs, and intelligent control "
    "systems optimized for industrial applications."
)

# Market Needs and Use Cases
display(Title("## Market Needs and Use Cases"))
display(
    "Industrial thermal processes represent a significant opportunity for energy storage "
    "applications. Our analysis of various industrial sectors has identified the following "
    "key use cases for thermal energy storage:"
)

# Create table of industrial applications
industry_data = []
for industry_group in [FOOD_APPLICATIONS, CHEMICAL_APPLICATIONS, METAL_APPLICATIONS, 
                      PAPER_APPLICATIONS, CEMENT_APPLICATIONS, TEXTILE_APPLICATIONS]:
    for app in industry_group:
        industry_data.append({
            "Industry": app.industry,
            "Process": app.name,
            "Temperature Range": f"{app.temperature_range.min} - {app.temperature_range.max}",
            "Energy Intensity": f"{app.energy_intensity}",
            "Potential Savings": f"{app.potential_energy_savings * 100:.1f}%"
        })

df_industries = pd.DataFrame(industry_data)
display(Table(df_industries, "Industrial Applications for Thermal Energy Storage", "tbl-industries"))

# Design Criteria and Requirements
display(Title("## Design Criteria and Requirements"))
display(thermal_storage_system.display())

# Material Selection Analysis
display(Title("## Material Selection Analysis"))
display(
    "The selection of appropriate storage media is critical to the performance, cost, and "
    "safety of thermal energy storage systems. We evaluated multiple material options across "
    "key performance criteria to identify optimal solutions for different temperature ranges "
    "and applications."
)

# Create materials comparison table
materials_data = [
    {
        "Material Type": MOLTEN_SALT.name,
        "Energy Density": f"{MOLTEN_SALT.energy_density}",
        "Temperature Range": f"{MOLTEN_SALT.min_temperature} - {MOLTEN_SALT.max_temperature}",
        "Cost": f"{MOLTEN_SALT.cost_per_kg}",
        "Advantages": "High heat capacity, proven technology",
        "Limitations": "Corrosion concerns, freezing risk"
    },
    {
        "Material Type": SOLID_CERAMIC.name,
        "Energy Density": f"{SOLID_CERAMIC.energy_density}",
        "Temperature Range": f"{SOLID_CERAMIC.min_temperature} - {SOLID_CERAMIC.max_temperature}",
        "Cost": f"{SOLID_CERAMIC.cost_per_kg}",
        "Advantages": "No leakage risk, long lifetime",
        "Limitations": "Lower heat transfer rates"
    },
    {
        "Material Type": HIGH_TEMP_CERAMIC.name,
        "Energy Density": f"{HIGH_TEMP_CERAMIC.energy_density}",
        "Temperature Range": f"{HIGH_TEMP_CERAMIC.min_temperature} - {HIGH_TEMP_CERAMIC.max_temperature}",
        "Cost": f"{HIGH_TEMP_CERAMIC.cost_per_kg}",
        "Advantages": "Very high temperature capability",
        "Limitations": "Higher cost, thermal stress management"
    },
    {
        "Material Type": MOLTEN_METAL.name,
        "Energy Density": f"{MOLTEN_METAL.energy_density}",
        "Temperature Range": f"{MOLTEN_METAL.min_temperature} - {MOLTEN_METAL.max_temperature}",
        "Cost": f"{MOLTEN_METAL.cost_per_kg}",
        "Advantages": "Excellent thermal conductivity",
        "Limitations": "Safety concerns, oxidation risk"
    },
    {
        "Material Type": PHASE_CHANGE_MATERIAL.name,
        "Energy Density": f"{PHASE_CHANGE_MATERIAL.energy_density}",
        "Temperature Range": f"{PHASE_CHANGE_MATERIAL.min_temperature} - {PHASE_CHANGE_MATERIAL.max_temperature}",
        "Cost": f"{PHASE_CHANGE_MATERIAL.cost_per_kg}",
        "Advantages": "High energy density at phase transition",
        "Limitations": "Limited temperature range, cycling stability"
    }
]

df_materials = pd.DataFrame(materials_data)
display(Table(df_materials, "Comparison of Thermal Storage Materials", "tbl-materials"))

# System Architecture and Subsystems
display(Title("## System Architecture and Subsystems"))
display(
    "The EPYR thermal energy storage system consists of five primary subsystems, each designed "
    "for modularity, scalability, and reliability:"
)

# Display subsystem information
display("### Heat Storage Core")
display(thermal_storage_medium.display())

display("### Containment System")
display(containment_system.display())

display("### Heat Exchanger Network")
display(heat_exchanger_system.display())

display("### Control and Monitoring System")
display(control_system.display())

display("### Integration Interface")
display(integration_system.display())

# Thermal Performance Analysis
display(Title("## Thermal Performance Analysis"))

# Parameters table
df_params = pd.DataFrame([
    {"Parameter": "Storage Capacity", "Value": f"{THERMAL_STORAGE_PARAMS.storage_capacity}"},
    {"Parameter": "Maximum Power Output", "Value": f"{THERMAL_STORAGE_PARAMS.max_power_output}"},
    {"Parameter": "Maximum Temperature", "Value": f"{THERMAL_STORAGE_PARAMS.max_temperature}"},
    {"Parameter": "Minimum Temperature", "Value": f"{THERMAL_STORAGE_PARAMS.min_temperature}"},
    {"Parameter": "Storage Volume", "Value": f"{THERMAL_STORAGE_PARAMS.storage_volume}"},
    {"Parameter": "Charge Efficiency", "Value": f"{THERMAL_STORAGE_PARAMS.charge_efficiency * 100}%"},
    {"Parameter": "Discharge Efficiency", "Value": f"{THERMAL_STORAGE_PARAMS.discharge_efficiency * 100}%"},
    {"Parameter": "Design Life", "Value": f"{THERMAL_STORAGE_PARAMS.design_life} years"},
])
display(Table(df_params, "Core design parameters", "tbl-params"))

# Energy content calculation
max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
max_energy = calculate_energy_content(max_temp)
min_energy = calculate_energy_content(min_temp)
usable_energy = max_energy - min_energy

display("### Energy Storage Capacity")
display(f"The system can store approximately {usable_energy:.2f} kWh of usable thermal energy.")

# Charging/discharging profiles
display("### Charging and Discharging Performance")
display(
    "Our simulations demonstrate the charging and discharging characteristics of the system "
    "under various operating conditions. The following results show temperature profiles and "
    "energy transfer rates during typical charge/discharge cycles."
)

# Create performance data table
charge_times = [2, 4, 8]
charge_results = [simulate_charging(hours) for hours in charge_times]
discharge_times = [2, 4, 6]
discharge_results = [simulate_discharging(hours) for hours in discharge_times]

charge_data = []
for i, hours in enumerate(charge_times):
    charge_data.append({
        "Charging Time (hours)": hours,
        "Final Temperature (°C)": f"{charge_results[i]['final_temp']:.1f}",
        "Energy Stored (kWh)": f"{charge_results[i]['energy_stored']:.2f}",
        "Average Power (kW)": f"{charge_results[i]['avg_power']:.2f}"
    })

discharge_data = []
for i, hours in enumerate(discharge_times):
    discharge_data.append({
        "Discharging Time (hours)": hours,
        "Final Temperature (°C)": f"{discharge_results[i]['final_temp']:.1f}",
        "Energy Delivered (kWh)": f"{discharge_results[i]['energy_delivered']:.2f}",
        "Average Power (kW)": f"{discharge_results[i]['avg_power']:.2f}"
    })

df_charge = pd.DataFrame(charge_data)
df_discharge = pd.DataFrame(discharge_data)

display(Table(df_charge, "Charging Performance", "tbl-charge"))
display(Table(df_discharge, "Discharging Performance", "tbl-discharge"))

# Heat loss analysis
display("### Heat Loss Analysis")
daily_heat_loss = calculate_heat_loss(24)
weekly_heat_loss = calculate_heat_loss(168)
monthly_heat_loss = calculate_heat_loss(720)

display(
    f"The system experiences a heat loss of approximately {daily_heat_loss:.2f} kWh per day "
    f"({(daily_heat_loss/max_energy)*100:.2f}% of full capacity), "
    f"{weekly_heat_loss:.2f} kWh per week, and {monthly_heat_loss:.2f} kWh per month. "
    "These values represent the self-discharge rate of the system when not in active use."
)

# Efficiency calculations
round_trip = calculate_round_trip_efficiency()

display("### System Efficiency")
display(
    f"The round-trip efficiency of the system is {round_trip*100:.1f}%, accounting for "
    "thermal losses during storage and conversion inefficiencies during charge and discharge."
)

# Material comparison
display("### Storage Material Comparison")
material_comparison = compare_materials()

material_comp_data = []
for name, metrics in material_comparison.items():
    material_comp_data.append({
        "Material": name,
        "Energy Density (kWh/m³)": f"{metrics['energy_density']:.1f}",
        "Temperature Range (°C)": f"{metrics['temp_range']:.1f}",
        "Relative Heat Loss": f"{metrics['relative_heat_loss']:.2f}",
        "Cost ($/kWh)": f"{metrics['cost_per_kwh']:.2f}"
    })

df_material_comp = pd.DataFrame(material_comp_data)
display(Table(df_material_comp, "Storage Material Performance Comparison", "tbl-material-comp"))

# Full cycle simulation
display("### Full Cycle Simulation")
cycle_results = simulate_full_cycle()

display(
    f"A full cycle simulation with {cycle_results['charge_hours']} hours charging, "
    f"{cycle_results['storage_hours']} hours storage, and {cycle_results['discharge_hours']} "
    f"hours discharging yields an overall cycle efficiency of {cycle_results['cycle_efficiency']*100:.1f}%. "
    f"The system stores {cycle_results['energy_input']:.1f} kWh of input energy and "
    f"delivers {cycle_results['energy_output']:.1f} kWh of output energy, with "
    f"{cycle_results['total_heat_loss']:.1f} kWh of heat loss during the complete cycle."
)

# Economic Analysis
display(Title("## Economic Analysis"))

# Calculate economic metrics
capex = calculate_capex()
annual_opex = calculate_annual_opex()
lcoe = calculate_lcoe()
payback = calculate_payback_period()
roi = calculate_roi()
carbon_reduction = carbon_emission_reduction()

display("### Capital and Operational Costs")
display(
    f"The thermal storage system has an estimated capital cost of ${capex:,.2f}, "
    f"with annual operational costs of ${annual_opex:,.2f}. "
    f"This results in a levelized cost of energy (LCOE) of ${lcoe:.4f}/kWh."
)

# Create cost breakdown table
cost_components = [
    {"Component": "Storage Medium", "Percentage": "35%", "Cost": f"${capex * 0.35:,.2f}"},
    {"Component": "Containment System", "Percentage": "25%", "Cost": f"${capex * 0.25:,.2f}"},
    {"Component": "Heat Exchangers", "Percentage": "20%", "Cost": f"${capex * 0.20:,.2f}"},
    {"Component": "Control Systems", "Percentage": "10%", "Cost": f"${capex * 0.10:,.2f}"},
    {"Component": "Integration & Installation", "Percentage": "10%", "Cost": f"${capex * 0.10:,.2f}"}
]
df_costs = pd.DataFrame(cost_components)
display(Table(df_costs, "Capital Cost Breakdown", "tbl-costs"))

display("### Financial Performance")
display(
    f"When compared to conventional heating systems, the thermal storage system offers:"
    "\n\n"
    f"- Payback period: {payback:.2f} years"
    "\n"
    f"- Return on Investment (ROI): {roi:.2f}%"
    "\n"
    f"- Annual carbon emission reduction: {carbon_reduction:.2f} tonnes CO2"
    "\n\n"
    "These economics vary by application, with more favorable returns in industries with high "
    "energy costs, significant peak demand charges, or process-critical thermal requirements."
)

# Implementation and Integration
display(Title("## Implementation and Integration"))
display(
    "The EPYR thermal storage system is designed for seamless integration with existing "
    "industrial processes. Our modular approach allows for customization to meet specific "
    "industry requirements while minimizing disruption to operations."
    "\n\n"
    "### Integration Approaches"
    "\n\n"
    "1. **Direct Heat Integration**: Connecting directly to process heating systems"
    "\n"
    "2. **Steam Generation**: Producing steam for various industrial applications"
    "\n"
    "3. **Hot Air Supply**: Providing heated air for drying and other processes"
    "\n"
    "4. **Waste Heat Recovery**: Capturing and storing heat from exhaust streams"
    "\n\n"
    "### Implementation Timeline"
    "\n\n"
    "- Site assessment and energy audit: 2-4 weeks"
    "\n"
    "- System design and engineering: 4-6 weeks"
    "\n"
    "- Equipment manufacturing: 8-12 weeks"
    "\n"
    "- Installation and commissioning: 2-4 weeks"
    "\n"
    "- Operator training and handover: 1-2 weeks"
)

# Conclusions and Next Steps
display(Title("## Conclusions and Next Steps"))
display(
    "The EPYR thermal energy storage system represents a significant advancement in industrial "
    "energy management technology. Our design offers:"
    "\n\n"
    "- High-temperature thermal storage with excellent efficiency"
    "\n"
    "- Modular, scalable architecture adaptable to various industries"
    "\n"
    "- Robust safety features and control systems"
    "\n"
    "- Compelling economic benefits through energy cost reduction"
    "\n"
    "- Substantial carbon emission reductions"
    "\n\n"
    "### Next Development Steps"
    "\n\n"
    "1. **Pilot Installations**: Deploy demonstration systems in key industrial sectors"
    "\n"
    "2. **Material Optimization**: Continue research on advanced storage materials"
    "\n"
    "3. **Control System Enhancement**: Develop AI-driven predictive control algorithms"
    "\n"
    "4. **Integration Packages**: Create standardized integration solutions for common industrial processes"
)

print("DESIGN_COMPLETE")
