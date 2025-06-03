"""
Cost analysis for thermal energy storage systems.
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
from epyr.simulation_economics import (
    calculate_capex, calculate_annual_opex, calculate_lcoe,
    calculate_payback_period, calculate_roi, carbon_emission_reduction,
    sensitivity_analysis
)

import pandas as pd
import numpy as np

print("Loading cost analysis module")

# Document configuration
config = DocumentConfig(
    title="Thermal Energy Storage System: Cost Analysis",
    author="EPYR Engineering Team",
    date="2025-06-02"
)
display(config)

# Executive Summary
display(Title("# Executive Summary"))
display(
    "This document provides a comprehensive cost analysis of EPYR's high-temperature "
    "thermal energy storage system compared to conventional heating technologies. "
    "The analysis demonstrates that our thermal storage solution offers significant "
    "cost advantages and carbon emission reductions across multiple industrial applications, "
    "particularly as renewable electricity prices continue to decline and carbon pricing mechanisms expand."
    "\n\n"
    "Key findings include:"
    "\n\n"
    f"- Levelized cost of heat (LCOH) from our thermal storage system is ${calculate_lcoe():.4f}/kWh, "
    "competitive with or better than conventional fossil fuel heating in many applications"
    "\n\n"
    f"- Payback period of {calculate_payback_period():.2f} years depending on the industrial application and local energy prices"
    "\n\n"
    f"- Carbon emission reductions of {carbon_emission_reduction():.2f} tonnes CO2 per year"
    "\n\n"
    "- Increasing economic advantage over time as renewable electricity costs decline and carbon pricing increases"
)

# Capital Cost Analysis
display(Title("# Capital Cost Analysis"))
display(
    "The capital cost of the thermal energy storage system includes all equipment, "
    "materials, installation, and engineering costs. The breakdown below shows the "
    "contribution of each component to the total capital expenditure."
)

# Calculate capital costs
capex = calculate_capex()

# Create capital cost breakdown
storage_medium_cost = capex * 0.35
containment_cost = capex * 0.25
heat_exchanger_cost = capex * 0.20
control_system_cost = capex * 0.10
integration_cost = capex * 0.10

df_capital_costs = pd.DataFrame([
    {"Component": "Storage Medium", "Cost ($)": f"{storage_medium_cost:,.2f}", "Percentage": "35%"},
    {"Component": "Containment System", "Cost ($)": f"{containment_cost:,.2f}", "Percentage": "25%"},
    {"Component": "Heat Exchanger", "Cost ($)": f"{heat_exchanger_cost:,.2f}", "Percentage": "20%"},
    {"Component": "Control System", "Cost ($)": f"{control_system_cost:,.2f}", "Percentage": "10%"},
    {"Component": "Integration & Installation", "Cost ($)": f"{integration_cost:,.2f}", "Percentage": "10%"},
    {"Component": "Total Capital Cost", "Cost ($)": f"{capex:,.2f}", "Percentage": "100%"},
])
display(Table(df_capital_costs, "Capital Cost Breakdown", "tbl-capital-costs"))

# Operational Cost Analysis
display(Title("# Operational Cost Analysis"))
display(
    "Operational costs include electricity for charging the thermal storage system, "
    "maintenance, labor, and other ongoing expenses. These costs are calculated on "
    "an annual basis and projected over the system lifetime."
)

# Calculate operational costs
annual_opex = calculate_annual_opex()

# Estimate breakdown of operational costs
electricity_cost = annual_opex * 0.60
maintenance_cost = annual_opex * 0.25
labor_cost = annual_opex * 0.10
other_costs = annual_opex * 0.05

df_opex = pd.DataFrame([
    {"Category": "Electricity", "Annual Cost ($)": f"{electricity_cost:,.2f}", "Percentage": "60%"},
    {"Category": "Maintenance", "Annual Cost ($)": f"{maintenance_cost:,.2f}", "Percentage": "25%"},
    {"Category": "Labor", "Annual Cost ($)": f"{labor_cost:,.2f}", "Percentage": "10%"},
    {"Category": "Other", "Annual Cost ($)": f"{other_costs:,.2f}", "Percentage": "5%"},
    {"Category": "Total Annual OPEX", "Annual Cost ($)": f"{annual_opex:,.2f}", "Percentage": "100%"},
])
display(Table(df_opex, "Annual Operational Costs", "tbl-opex"))

# Levelized Cost Analysis
display(Title("# Levelized Cost Analysis"))
display(
    "The Levelized Cost of Heat (LCOH) represents the average cost per unit of heat "
    "energy produced over the entire lifetime of the system. It accounts for all capital "
    "costs, operational costs, and the time value of money using a discount rate."
)

lcoe = calculate_lcoe()
display(f"The calculated LCOH for our thermal storage system is **${lcoe:.4f}/kWh**.")

# Comparison with Conventional Heating
display(Title("# Comparison with Conventional Heating"))
display(
    "To evaluate the economic competitiveness of our thermal storage system, "
    "we compare its costs with conventional heating technologies commonly used "
    "in industrial applications."
)

# Create comparison data
conventional_systems = [
    {
        "System": "Natural Gas Boiler",
        "LCOH ($/kWh)": 0.06,
        "Capital Cost ($/kW)": 150,
        "Fuel Cost ($/kWh)": 0.04,
        "CO2 Emissions (kg/kWh)": 0.20
    },
    {
        "System": "Oil Boiler",
        "LCOH ($/kWh)": 0.09,
        "Capital Cost ($/kW)": 180,
        "Fuel Cost ($/kWh)": 0.07,
        "CO2 Emissions (kg/kWh)": 0.27
    },
    {
        "System": "Electric Resistance",
        "LCOH ($/kWh)": 0.12,
        "Capital Cost ($/kW)": 100,
        "Fuel Cost ($/kWh)": 0.12,
        "CO2 Emissions (kg/kWh)": 0.15
    },
    {
        "System": "Thermal Storage",
        "LCOH ($/kWh)": lcoe,
        "Capital Cost ($/kW)": capex / THERMAL_STORAGE_PARAMS.max_power_output.magnitude,
        "Fuel Cost ($/kWh)": electricity_cost / (THERMAL_STORAGE_PARAMS.storage_capacity.magnitude * THERMAL_STORAGE_PARAMS.cycles_per_year),
        "CO2 Emissions (kg/kWh)": 0.15 / THERMAL_STORAGE_PARAMS.discharge_efficiency
    }
]

df_comparison = pd.DataFrame(conventional_systems)
display(Table(df_comparison, "Heating Technology Comparison", "tbl-comparison"))

# Payback and ROI Analysis
display(Title("# Payback and ROI Analysis"))
display(
    "This section analyzes the payback period and return on investment (ROI) for "
    "the thermal storage system when replacing different conventional heating technologies."
)

payback = calculate_payback_period()
roi = calculate_roi()

display(f"When replacing a natural gas heating system, the thermal storage system offers:")
display(f"- Simple payback period: **{payback:.2f} years**")
display(f"- Return on investment (ROI): **{roi:.2f}%** over the {THERMAL_STORAGE_PARAMS.design_life}-year lifetime")

# Carbon Pricing Impact
display(Title("# Carbon Pricing Impact"))
display(
    "Carbon pricing mechanisms are increasingly being implemented worldwide to internalize "
    "the external costs of greenhouse gas emissions. This analysis examines how different "
    "carbon price scenarios would affect the economic comparison between our thermal storage "
    "system and conventional heating technologies."
)

# Create carbon pricing scenarios
carbon_prices = [0, 25, 50, 75, 100]
carbon_reduction = carbon_emission_reduction()

carbon_impact_data = []
for price in carbon_prices:
    carbon_cost = carbon_reduction * price
    adjusted_payback = payback * (1 - (carbon_cost / (electricity_cost - maintenance_cost)))
    adjusted_roi = roi * (1 + (carbon_cost / (electricity_cost - maintenance_cost)) * 0.5)
    
    carbon_impact_data.append({
        "Carbon Price ($/tonne)": price,
        "Annual Carbon Value ($)": f"{carbon_cost:,.2f}",
        "Adjusted Payback (years)": f"{adjusted_payback:.2f}",
        "Adjusted ROI (%)": f"{adjusted_roi:.2f}"
    })

df_carbon_impact = pd.DataFrame(carbon_impact_data)
display(Table(df_carbon_impact, "Carbon Pricing Impact", "tbl-carbon-impact"))

# Sensitivity Analysis
display(Title("# Sensitivity Analysis"))
display(
    "This section examines how changes in key parameters affect the economic performance "
    "of the thermal storage system. Understanding these sensitivities helps identify the "
    "most critical factors for cost optimization and risk assessment."
)

# Get sensitivity analysis results
sensitivity_results = sensitivity_analysis()

# Create sensitivity table for LCOE
lcoe_sensitivity_data = []
for param, results in sensitivity_results.items():
    for result in results:
        lcoe_sensitivity_data.append({
            "Parameter": param,
            "Change": f"{(result['factor']-1)*100:+.0f}%",
            "LCOE ($/kWh)": f"{result['lcoe']:.4f}",
            "Change from Base": f"{(result['lcoe']/lcoe-1)*100:+.1f}%"
        })

df_lcoe_sensitivity = pd.DataFrame(lcoe_sensitivity_data)
display(Table(df_lcoe_sensitivity, "LCOE Sensitivity Analysis", "tbl-lcoe-sensitivity"))

# Cost Optimization Strategies
display(Title("# Cost Optimization Strategies"))
display(
    "Several strategies can be employed to further reduce the cost of thermal energy storage systems:"
    "\n\n"
    "1. **Scale Optimization**: Increasing system size to benefit from economies of scale"
    "\n\n"
    "2. **Material Selection**: Using lower-cost storage media for applications with less demanding temperature requirements"
    "\n\n"
    "3. **Cycle Optimization**: Increasing the number of charge/discharge cycles per year to improve utilization"
    "\n\n"
    "4. **Integration with Variable Electricity Pricing**: Charging during low-price periods to reduce operating costs"
    "\n\n"
    "5. **Heat Recovery**: Capturing and utilizing waste heat from the system"
    "\n\n"
    "6. **Modular Design**: Enabling incremental capacity expansion and reducing initial capital requirements"
)

# Conclusions
display(Title("# Conclusions"))
display(
    "This comprehensive cost analysis demonstrates that EPYR's thermal energy storage system "
    "offers a compelling economic case for industrial heat decarbonization, particularly in "
    "industries with high-temperature requirements and consistent heat demand patterns."
    "\n\n"
    "Key conclusions include:"
    "\n\n"
    f"- The thermal storage system is already cost-competitive with conventional fossil fuel heating "
    f"in many applications, with LCOH of ${lcoe:.4f}/kWh"
    "\n\n"
    "- When carbon pricing is included, the economic advantage of thermal storage increases significantly"
    "\n\n"
    "- The system offers substantial carbon emission reductions compared to fossil fuel alternatives"
    "\n\n"
    "- Continued improvements in system design and manufacturing processes are expected to "
    "further reduce costs and improve economic performance"
)

print("Cost analysis complete")
