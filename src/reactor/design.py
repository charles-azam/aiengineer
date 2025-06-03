"""
High-Temperature Gas-cooled Reactor (HTGR) Design Report

This document presents the comprehensive design of a modular HTGR system
for industrial heat applications, focusing on decarbonizing industrial processes
through high-temperature nuclear heat.
"""

from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from reactor.parameters_core import CORE_PARAMS
from reactor.parameters_fuel import FUEL_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS, HEAT_EXCHANGER_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
from reactor.parameters_modular import MODULE_PHYSICAL_PARAMS, POWER_SCALING_PARAMS, INDUSTRIAL_INTERFACE_PARAMS
from reactor.parameters_htgr import OPERATIONAL_PARAMS
from reactor.simulation_thermal import calculate_helium_flow_rate, calculate_co2_flow_rate, calculate_heat_transfer_performance
from reactor.simulation_safety import evaluate_passive_safety_performance
from reactor.simulation_economics import calculate_lcoh

import pandas as pd
import numpy as np
from pathlib import Path

# Document configuration
config = DocumentConfig(
    title="Modular High-Temperature Gas-cooled Reactor (HTGR) Design",
    author="Reactor Design Team",
    date="2025-06-03"
)
display(config)

# Executive Summary
display(Title("# Executive Summary"))
display(
    "This document presents the design of a modular High-Temperature Gas-cooled Reactor (HTGR) "
    "system specifically engineered for decarbonizing industrial heat production. The system "
    f"provides thermal power outputs of {CORE_PARAMS.thermal_power_small.magnitude}, "
    f"{CORE_PARAMS.thermal_power_medium.magnitude}, or {CORE_PARAMS.thermal_power_large.magnitude} MW "
    f"using TRISO fuel and helium coolant, operating at temperatures up to "
    f"{CORE_PARAMS.core_outlet_temp.magnitude}°C. The design incorporates passive safety features "
    f"and has a design life of {CORE_PARAMS.design_life.magnitude} years with minimal refueling requirements."
)

# Introduction
display(Title("# 1. Introduction"))

display(Title("## 1.1 Design Objectives"))
display(
    "The HTGR system is designed to meet the following key objectives:"
    "\n\n"
    "- Provide carbon-free industrial process heat at temperatures up to 600°C"
    "\n"
    "- Ensure inherent safety through passive features and multiple barriers"
    "\n"
    "- Enable modular, factory-based manufacturing for cost reduction and quality control"
    "\n"
    "- Offer scalable configurations to match various industrial heat requirements"
    "\n"
    "- Maintain compatibility with existing industrial heat systems"
    "\n"
    "- Achieve competitive economics compared to fossil fuel alternatives"
)

display(Title("## 1.2 Key Design Features"))
key_features = pd.DataFrame([
    {"Feature": "TRISO Fuel", "Description": "Inherent fission product containment up to 1600°C"},
    {"Feature": "Helium Primary Coolant", "Description": "Chemically inert, single-phase cooling with excellent heat transfer"},
    {"Feature": "CO₂ Secondary Loop", "Description": "Efficient heat transfer to industrial processes without radioactive contamination"},
    {"Feature": "Passive Safety", "Description": "Natural circulation, conduction, and radiation for decay heat removal"},
    {"Feature": "Modular Design", "Description": "Factory fabrication with standardized modules for various power levels"},
    {"Feature": "Graphite Moderator", "Description": "High temperature stability and large thermal inertia"}
])
display(Table(key_features, "Key Design Features", "tbl-features"))

# Core Design
display(Title("# 2. Core Design"))

display(Title("## 2.1 TRISO Fuel"))
display(
    "The reactor utilizes Tri-structural Isotropic (TRISO) fuel particles, which consist of uranium "
    f"kernels ({FUEL_PARAMS.kernel_material}) coated with multiple barrier layers. These particles provide "
    "inherent containment of fission products even at extreme temperatures."
)

# TRISO fuel parameters table
triso_params = pd.DataFrame([
    {"Parameter": "Kernel Material", "Value": f"{FUEL_PARAMS.kernel_material}"},
    {"Parameter": "Kernel Diameter", "Value": f"{FUEL_PARAMS.kernel_diameter}"},
    {"Parameter": "Buffer Layer Thickness", "Value": f"{FUEL_PARAMS.buffer_thickness}"},
    {"Parameter": "IPyC Layer Thickness", "Value": f"{FUEL_PARAMS.ipyc_thickness}"},
    {"Parameter": "SiC Layer Thickness", "Value": f"{FUEL_PARAMS.sic_thickness}"},
    {"Parameter": "OPyC Layer Thickness", "Value": f"{FUEL_PARAMS.opyc_thickness}"},
    {"Parameter": "Total Particle Diameter", "Value": f"{FUEL_PARAMS.total_particle_diameter}"},
    {"Parameter": "Enrichment", "Value": f"{FUEL_PARAMS.enrichment}"},
    {"Parameter": "Failure Temperature", "Value": f"{FUEL_PARAMS.failure_temperature}"}
])
display(Table(triso_params, "TRISO Fuel Parameters", "tbl-triso"))

display(Title("## 2.2 Core Configuration"))
display(
    "The reactor core consists of a cylindrical arrangement of graphite blocks containing "
    "TRISO fuel particles and coolant channels. The graphite serves as both moderator and "
    "structural material, providing excellent neutron moderation and high temperature stability."
)

# Core parameters table
core_params = pd.DataFrame([
    {"Parameter": "Core Height", "Value": f"{CORE_PARAMS.core_height}"},
    {"Parameter": "Core Diameter", "Value": f"{CORE_PARAMS.core_diameter}"},
    {"Parameter": "Reflector Thickness", "Value": f"{CORE_PARAMS.reflector_thickness}"},
    {"Parameter": "Power Density", "Value": f"{CORE_PARAMS.power_density}"},
    {"Parameter": "Number of Fuel Elements (15 MW)", "Value": f"{FUEL_PARAMS.fuel_elements_medium}"},
    {"Parameter": "Core Inlet Temperature", "Value": f"{CORE_PARAMS.core_inlet_temp}"},
    {"Parameter": "Core Outlet Temperature", "Value": f"{CORE_PARAMS.core_outlet_temp}"},
    {"Parameter": "Primary Pressure", "Value": f"{CORE_PARAMS.primary_pressure}"}
])
display(Table(core_params, "Core Design Parameters", "tbl-core"))

# Thermal-Hydraulic System
display(Title("# 3. Thermal-Hydraulic System"))

display(Title("## 3.1 Primary Helium Loop"))
display(
    "The primary coolant system uses helium gas to transfer heat from the reactor core to the "
    "intermediate heat exchanger. Helium is chosen for its excellent heat transfer properties, "
    "chemical inertness, and transparency to neutrons."
)

# Calculate helium flow rates for different power levels
helium_flow_small = calculate_helium_flow_rate(CORE_PARAMS.thermal_power_small.magnitude)
helium_flow_medium = calculate_helium_flow_rate(CORE_PARAMS.thermal_power_medium.magnitude)
helium_flow_large = calculate_helium_flow_rate(CORE_PARAMS.thermal_power_large.magnitude)

# Primary loop parameters table
primary_params = pd.DataFrame([
    {"Parameter": "Coolant", "Value": "Helium"},
    {"Parameter": "Core Inlet Temperature", "Value": f"{CORE_PARAMS.core_inlet_temp}"},
    {"Parameter": "Core Outlet Temperature", "Value": f"{CORE_PARAMS.core_outlet_temp}"},
    {"Parameter": "System Pressure", "Value": f"{CORE_PARAMS.primary_pressure}"},
    {"Parameter": "Flow Rate (10 MW)", "Value": f"{helium_flow_small:.2f} kg/s"},
    {"Parameter": "Flow Rate (15 MW)", "Value": f"{helium_flow_medium:.2f} kg/s"},
    {"Parameter": "Flow Rate (20 MW)", "Value": f"{helium_flow_large:.2f} kg/s"},
    {"Parameter": "Core Pressure Drop", "Value": f"{CORE_PARAMS.core_pressure_drop}"}
])
display(Table(primary_params, "Primary Helium Loop Parameters", "tbl-primary"))

display(Title("## 3.2 Secondary CO₂ Loop"))
display(
    "A secondary carbon dioxide (CO₂) loop transfers heat from the intermediate heat exchanger "
    "to the industrial process heat exchangers. CO₂ is selected for its favorable heat transfer "
    "properties and compatibility with high-temperature operation."
)

# Calculate CO2 flow rates for different power levels
co2_flow_small = calculate_co2_flow_rate(CORE_PARAMS.thermal_power_small.magnitude)
co2_flow_medium = calculate_co2_flow_rate(CORE_PARAMS.thermal_power_medium.magnitude)
co2_flow_large = calculate_co2_flow_rate(CORE_PARAMS.thermal_power_large.magnitude)

# Secondary loop parameters table
secondary_params = pd.DataFrame([
    {"Parameter": "Coolant", "Value": "CO₂"},
    {"Parameter": "Inlet Temperature", "Value": f"{SECONDARY_LOOP_PARAMS.inlet_temperature}"},
    {"Parameter": "Outlet Temperature", "Value": f"{SECONDARY_LOOP_PARAMS.co2_outlet_temperature}"},
    {"Parameter": "System Pressure", "Value": f"{SECONDARY_LOOP_PARAMS.operating_pressure}"},
    {"Parameter": "Flow Rate (10 MW)", "Value": f"{co2_flow_small:.2f} kg/s"},
    {"Parameter": "Flow Rate (15 MW)", "Value": f"{co2_flow_medium:.2f} kg/s"},
    {"Parameter": "Flow Rate (20 MW)", "Value": f"{co2_flow_large:.2f} kg/s"}
])
display(Table(secondary_params, "Secondary CO₂ Loop Parameters", "tbl-secondary"))

display(Title("## 3.3 Heat Exchangers"))
display(
    "The heat transfer system includes two main types of heat exchangers:"
    "\n\n"
    "1. **Intermediate Heat Exchanger (IHX)**: Transfers heat from the primary helium loop to the secondary CO₂ loop"
    "\n"
    "2. **Process Heat Exchangers**: Transfer heat from the secondary CO₂ loop to various industrial process mediums"
)

# Heat exchanger parameters table
hx_params = pd.DataFrame([
    {"Parameter": "IHX Type", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_type}"},
    {"Parameter": "IHX Effectiveness", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_effectiveness:.2f}"},
    {"Parameter": "Primary Side Pressure Drop", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_primary_side_pressure_drop}"},
    {"Parameter": "Secondary Side Pressure Drop", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_secondary_side_pressure_drop}"},
    {"Parameter": "Heat Transfer Coefficient", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_heat_transfer_coefficient}"},
    {"Parameter": "Surface Area (20 MW)", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_surface_area_large}"}
])
display(Table(hx_params, "Heat Exchanger Parameters", "tbl-hx"))

display(Title("## 3.4 Industrial Process Interfaces"))
display(
    "The HTGR system is designed to interface with various industrial processes through customizable "
    "heat delivery systems. The secondary CO₂ loop can provide heat to generate:"
)

# Industrial interface parameters table
interface_params = pd.DataFrame([
    {"Interface Type": "Process Steam", "Temperature": f"{INDUSTRIAL_INTERFACE_PARAMS.steam_output_temperature}", "Connection": f"{INDUSTRIAL_INTERFACE_PARAMS.steam_connection_type}"},
    {"Interface Type": "Hot Air", "Temperature": f"{INDUSTRIAL_INTERFACE_PARAMS.hot_air_output_temperature}", "Connection": f"{INDUSTRIAL_INTERFACE_PARAMS.air_connection_type}"},
    {"Interface Type": "Thermal Oil", "Temperature": f"{INDUSTRIAL_INTERFACE_PARAMS.thermal_oil_output_temperature}", "Connection": f"{INDUSTRIAL_INTERFACE_PARAMS.oil_connection_type}"}
])
display(Table(interface_params, "Industrial Process Interfaces", "tbl-interfaces"))

# Safety Features
display(Title("# 4. Safety Features"))

display(Title("## 4.1 Passive Safety Systems"))
display(
    "The HTGR design incorporates multiple passive safety features that do not require active systems "
    "or operator intervention to maintain safe conditions:"
    "\n\n"
    "- **TRISO Fuel Containment**: Multiple barriers within the fuel particles contain fission products"
    "\n"
    "- **Negative Temperature Coefficient**: Inherent reactivity feedback for self-regulation"
    "\n"
    "- **Passive Decay Heat Removal**: Natural circulation, conduction, and radiation heat transfer"
    "\n"
    "- **High Heat Capacity**: Graphite moderator provides thermal inertia during transients"
)

# Safety parameters table
safety_params = pd.DataFrame([
    {"Parameter": "Maximum Fuel Temperature (Normal)", "Value": f"{SAFETY_PARAMS.max_fuel_temp}"},
    {"Parameter": "Maximum Fuel Temperature (Accident)", "Value": f"{SAFETY_PARAMS.max_accident_fuel_temp}"},
    {"Parameter": "Temperature Coefficient", "Value": f"{SAFETY_PARAMS.temperature_coefficient}"},
    {"Parameter": "Passive Cooling Duration", "Value": f"{SAFETY_PARAMS.passive_cooling_duration}"},
    {"Parameter": "Shutdown Margin", "Value": f"{SAFETY_PARAMS.shutdown_margin}"}
])
display(Table(safety_params, "Safety Parameters", "tbl-safety"))

display(Title("## 4.2 Safety Performance Analysis"))
display(
    "Comprehensive safety analyses have been performed to evaluate the response of the HTGR design "
    "to various postulated events. The results demonstrate robust safety performance with significant margins."
)

# Run safety performance evaluation
safety_performance = evaluate_passive_safety_performance()

# Safety performance results table
safety_results = pd.DataFrame([
    {"Parameter": "Maximum Accident Temperature", "Value": f"{safety_performance['max_accident_temp']}°C"},
    {"Parameter": "Temperature Margin to Failure", "Value": f"{FUEL_PARAMS.failure_temperature.magnitude - safety_performance['max_accident_temp']}°C"},
    {"Parameter": "Passive Cooling Duration", "Value": f"{safety_performance['passive_cooling_duration']} hours"},
    {"Parameter": "Fission Product Retention", "Value": f"{safety_performance['fission_product_retention']*100:.4f}%"},
    {"Parameter": "Operator Response Grace Period", "Value": f"{safety_performance['grace_period']} hours"}
])
display(Table(safety_results, "Safety Performance Results", "tbl-safety-results"))

# Modular Design
display(Title("# 5. Modular Design"))

display(Title("## 5.1 Module Configuration"))
display(
    "The HTGR system is designed with a modular architecture that enables factory fabrication, "
    "efficient transportation, and simplified on-site assembly. The modular approach allows for "
    "scaling between different power levels by adjusting the number and configuration of modules."
)

# Module configuration table
module_config = pd.DataFrame([
    {"Configuration": "10 MW", "Core Modules": f"{POWER_SCALING_PARAMS.core_modules_10MW}", "Heat Exchanger Modules": f"{POWER_SCALING_PARAMS.hx_modules_10MW}", "Control Modules": f"{POWER_SCALING_PARAMS.control_modules_10MW}", "Total Modules": f"{POWER_SCALING_PARAMS.modules_10MW}"},
    {"Configuration": "15 MW", "Core Modules": f"{POWER_SCALING_PARAMS.core_modules_15MW}", "Heat Exchanger Modules": f"{POWER_SCALING_PARAMS.hx_modules_15MW}", "Control Modules": f"{POWER_SCALING_PARAMS.control_modules_15MW}", "Total Modules": f"{POWER_SCALING_PARAMS.modules_15MW}"},
    {"Configuration": "20 MW", "Core Modules": f"{POWER_SCALING_PARAMS.core_modules_20MW}", "Heat Exchanger Modules": f"{POWER_SCALING_PARAMS.hx_modules_20MW}", "Control Modules": f"{POWER_SCALING_PARAMS.control_modules_20MW}", "Total Modules": f"{POWER_SCALING_PARAMS.modules_20MW}"}
])
display(Table(module_config, "Module Configuration by Power Level", "tbl-modules"))

display(Title("## 5.2 Module Physical Characteristics"))
display(
    "Each module is designed to comply with standard transportation limits for road, rail, or sea shipping. "
    "The physical dimensions and weights are carefully controlled to ensure transportability while "
    "maximizing factory completion."
)

# Module physical parameters table
module_physical = pd.DataFrame([
    {"Module Type": "Core Module", "Length": f"{MODULE_PHYSICAL_PARAMS.core_module_length}", "Width": f"{MODULE_PHYSICAL_PARAMS.core_module_width}", "Height": f"{MODULE_PHYSICAL_PARAMS.core_module_height}", "Weight": f"{MODULE_PHYSICAL_PARAMS.core_module_weight}"},
    {"Module Type": "Heat Exchanger Module", "Length": f"{MODULE_PHYSICAL_PARAMS.hx_module_length}", "Width": f"{MODULE_PHYSICAL_PARAMS.hx_module_width}", "Height": f"{MODULE_PHYSICAL_PARAMS.hx_module_height}", "Weight": f"{MODULE_PHYSICAL_PARAMS.hx_module_weight}"},
    {"Module Type": "Control System Module", "Length": f"{MODULE_PHYSICAL_PARAMS.control_module_length}", "Width": f"{MODULE_PHYSICAL_PARAMS.control_module_width}", "Height": f"{MODULE_PHYSICAL_PARAMS.control_module_height}", "Weight": f"{MODULE_PHYSICAL_PARAMS.control_module_weight}"}
])
display(Table(module_physical, "Module Physical Characteristics", "tbl-physical"))

# Performance Analysis
display(Title("# 6. Performance Analysis"))

display(Title("## 6.1 Thermal Performance"))
display(
    "The thermal performance of the HTGR system has been analyzed for different power levels. "
    "The high operating temperatures enable efficient heat transfer to industrial processes."
)

# Run thermal performance analysis for medium configuration
thermal_performance = calculate_heat_transfer_performance(CORE_PARAMS.thermal_power_medium.magnitude)

# Thermal performance results table
thermal_results = pd.DataFrame([
    {"Parameter": "Primary Helium Flow Rate", "Value": f"{thermal_performance['helium_flow_rate']:.2f} kg/s"},
    {"Parameter": "Secondary CO₂ Flow Rate", "Value": f"{thermal_performance['co2_flow_rate']:.2f} kg/s"},
    {"Parameter": "Primary Temperature Differential", "Value": f"{thermal_performance['delta_t_primary']:.1f}°C"},
    {"Parameter": "Secondary Temperature Differential", "Value": f"{thermal_performance['delta_t_secondary']:.1f}°C"},
    {"Parameter": "Heat Transfer Efficiency", "Value": f"{HEAT_EXCHANGER_PARAMS.hx_effectiveness:.1%}"}
])
display(Table(thermal_results, "Thermal Performance Results (15 MW Configuration)", "tbl-thermal"))

display(Title("## 6.2 Economic Performance"))
display(
    "The economic performance of the HTGR system has been analyzed to assess its competitiveness "
    "with conventional fossil fuel heating systems. The analysis includes capital costs, operating "
    "costs, and the impact of carbon pricing."
)

# Calculate LCOH for different configurations
lcoh_small = calculate_lcoh("small")
lcoh_medium = calculate_lcoh("medium")
lcoh_large = calculate_lcoh("large")

# Economic performance results table
economic_results = pd.DataFrame([
    {"Configuration": "10 MW", "LCOH ($/MWh thermal)": f"${lcoh_small:.2f}"},
    {"Configuration": "15 MW", "LCOH ($/MWh thermal)": f"${lcoh_medium:.2f}"},
    {"Configuration": "20 MW", "LCOH ($/MWh thermal)": f"${lcoh_large:.2f}"}
])
display(Table(economic_results, "Levelized Cost of Heat by Configuration", "tbl-economics"))

display(Title("## 6.3 Operational Performance"))
display(
    "The HTGR system is designed for high availability and minimal maintenance requirements. "
    "The long refueling intervals and robust component design contribute to excellent operational performance."
)

# Operational performance table
operational_params = pd.DataFrame([
    {"Parameter": "Design Life", "Value": f"{CORE_PARAMS.design_life}"},
    {"Parameter": "Refueling Interval", "Value": f"{CORE_PARAMS.refueling_interval}"},
    {"Parameter": "Availability Factor", "Value": f"{OPERATIONAL_PARAMS.availability:.1f}%"},
    {"Parameter": "Planned Outage Duration", "Value": f"{OPERATIONAL_PARAMS.planned_outage_duration}"}
])
display(Table(operational_params, "Operational Performance Parameters", "tbl-operational"))

# Conclusion
display(Title("# 7. Conclusion"))
display(
    "The modular High-Temperature Gas-cooled Reactor (HTGR) design presented in this document "
    "offers a viable solution for decarbonizing industrial heat production. Key advantages include:"
    "\n\n"
    "- **High Temperature Operation**: Providing process heat at temperatures up to 600°C"
    "\n"
    "- **Inherent Safety**: Multiple passive safety features ensuring robust accident response"
    "\n"
    "- **Modular Design**: Factory fabrication and scalable deployment options"
    "\n"
    "- **Operational Flexibility**: Adaptable to various industrial heat applications"
    "\n"
    "- **Economic Competitiveness**: Particularly in scenarios with carbon pricing"
    "\n\n"
    "The design meets all specified requirements and provides a comprehensive solution "
    "for industrial decarbonization through nuclear process heat. The modular approach "
    "enables cost-effective deployment across a range of industrial applications, with "
    "configurations available from 10 MW to 20 MW thermal output."
)

print("DESIGN_COMPLETE")
"""
Design document for the modular high-temperature gas-cooled reactor (HTGR) system
for industrial heat applications.
"""
from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from reactor.parameters_reactor import REACTOR_PARAMS

import pandas as pd
from pathlib import Path

# Document metadata
config = DocumentConfig(
    title="Modular HTGR Design for Industrial Heat Applications",
    author="Reactor Design Team",
    date="2025-06-03"
)
display(config)

# Title and introduction
display(Title("# Modular High-Temperature Gas-cooled Reactor (HTGR) System"))

display(
    "This document presents the design of a modular high-temperature gas-cooled reactor "
    "(HTGR) system specifically engineered for decarbonizing industrial heat production. "
    "The system utilizes TRISO fuel particles and helium coolant, operating at temperatures "
    "suitable for various industrial heat applications."
)

# Core design parameters
display(Title("## Core Design Parameters"))

df_core_params = pd.DataFrame([
    {"Parameter": "Thermal Power Options", "Value": f"{REACTOR_PARAMS.thermal_power_options} MWth"},
    {"Parameter": "Current Design Power", "Value": f"{REACTOR_PARAMS.thermal_power}"},
    {"Parameter": "Core Height", "Value": f"{REACTOR_PARAMS.core_height}"},
    {"Parameter": "Core Diameter", "Value": f"{REACTOR_PARAMS.core_diameter}"},
    {"Parameter": "Core Inlet Temperature", "Value": f"{REACTOR_PARAMS.core_inlet_temp}"},
    {"Parameter": "Core Outlet Temperature", "Value": f"{REACTOR_PARAMS.core_outlet_temp}"},
    {"Parameter": "Helium Pressure", "Value": f"{REACTOR_PARAMS.helium_pressure}"},
    {"Parameter": "Helium Flow Rate", "Value": f"{REACTOR_PARAMS.helium_flow_rate}"},
])
display(Table(df_core_params, "Core Design Parameters", "tbl-core-params"))

# Fuel parameters
display(Title("## Fuel Design"))

df_fuel_params = pd.DataFrame([
    {"Parameter": "Fuel Type", "Value": REACTOR_PARAMS.fuel_type},
    {"Parameter": "Enrichment", "Value": f"{REACTOR_PARAMS.enrichment}"},
    {"Parameter": "Fuel Loading", "Value": f"{REACTOR_PARAMS.fuel_loading}"},
    {"Parameter": "Kernel Diameter", "Value": f"{REACTOR_PARAMS.kernel_diameter}"},
    {"Parameter": "Packing Fraction", "Value": f"{REACTOR_PARAMS.packing_fraction}"},
])
display(Table(df_fuel_params, "Fuel Parameters", "tbl-fuel-params"))

# Physical and operational parameters
display(Title("## Physical and Operational Parameters"))

df_physical_params = pd.DataFrame([
    {"Parameter": "Module Height", "Value": f"{REACTOR_PARAMS.module_height}"},
    {"Parameter": "Module Diameter", "Value": f"{REACTOR_PARAMS.module_diameter}"},
    {"Parameter": "Module Weight", "Value": f"{REACTOR_PARAMS.module_weight}"},
    {"Parameter": "Design Lifetime", "Value": f"{REACTOR_PARAMS.design_lifetime}"},
    {"Parameter": "Refueling Interval", "Value": f"{REACTOR_PARAMS.refueling_interval}"},
    {"Parameter": "Capacity Factor", "Value": f"{REACTOR_PARAMS.capacity_factor}"},
    {"Parameter": "Availability", "Value": f"{REACTOR_PARAMS.availability}"},
])
display(Table(df_physical_params, "Physical and Operational Parameters", "tbl-physical-params"))

# Secondary loop parameters
display(Title("## Heat Transfer System"))

df_heat_params = pd.DataFrame([
    {"Parameter": "Secondary Fluid", "Value": REACTOR_PARAMS.secondary_fluid},
    {"Parameter": "Secondary Temperature", "Value": f"{REACTOR_PARAMS.secondary_temp}"},
    {"Parameter": "Secondary Pressure", "Value": f"{REACTOR_PARAMS.secondary_pressure}"},
    {"Parameter": "Heat Exchanger Type", "Value": REACTOR_PARAMS.heat_exchanger_type},
])
display(Table(df_heat_params, "Heat Transfer Parameters", "tbl-heat-params"))

# Safety features
display(Title("## Safety Features"))

df_safety_params = pd.DataFrame([
    {"Parameter": "Decay Heat Removal", "Value": REACTOR_PARAMS.decay_heat_removal},
    {"Parameter": "Containment Type", "Value": REACTOR_PARAMS.containment_type},
    {"Parameter": "Emergency Shutdown", "Value": REACTOR_PARAMS.emergency_shutdown},
    {"Parameter": "Fission Product Barrier", "Value": REACTOR_PARAMS.fission_product_barrier},
])
display(Table(df_safety_params, "Safety Features", "tbl-safety-params"))

# Industrial applications
display(Title("## Industrial Applications"))

display(
    "The modular HTGR system is designed to provide industrial heat for various applications, "
    "including but not limited to:"
)

df_applications = pd.DataFrame([
    {"Application": "Process Steam Generation", "Temperature Range": "150-550°C", "Industries": "Chemical, Refining, Paper"},
    {"Application": "District Heating", "Temperature Range": "80-150°C", "Industries": "Urban infrastructure, Commercial buildings"},
    {"Application": "Hydrogen Production", "Temperature Range": "500-600°C", "Industries": "Chemical, Transportation"},
    {"Application": "Desalination", "Temperature Range": "70-130°C", "Industries": "Water treatment, Coastal communities"},
])
display(Table(df_applications, "Industrial Heat Applications", "tbl-applications"))

# Deployment considerations
display(Title("## Deployment Considerations"))

display(
    "The modular design allows for scalable deployment at various industrial sites. "
    "Key considerations for deployment include:"
)

df_deployment = pd.DataFrame([
    {"Consideration": "Site Requirements", "Details": "Approximately 1-2 hectares per module, access to cooling water or dry cooling capability"},
    {"Consideration": "Regulatory Compliance", "Details": "Requires nuclear site license, environmental permits, and safety case approval"},
    {"Consideration": "Manufacturing", "Details": "Factory fabrication of modules with final assembly on site"},
    {"Consideration": "Grid Connection", "Details": "Optional for cogeneration applications, not required for pure heat production"},
    {"Consideration": "Scalability", "Details": f"Multiple modules can be installed to match demand, available in {REACTOR_PARAMS.thermal_power_options} MWth sizes"},
])
display(Table(df_deployment, "Deployment Considerations", "tbl-deployment"))

# Conclusion
display(Title("## Conclusion"))

display(
    "The modular HTGR system presented in this design document offers a viable solution "
    "for decarbonizing industrial heat production. With its scalable design, passive safety "
    "features, and high-temperature capability, it can serve a wide range of industrial "
    "applications while minimizing carbon emissions."
)

print("DESIGN_COMPLETE")
