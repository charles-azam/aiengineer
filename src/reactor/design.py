from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
from reactor.systems_reactor import reactor_system
from reactor.simulation_reactor import compute_power_density, compute_temperature_rise, compute_fuel_consumption
from reactor.simulation_thermal import compute_heat_exchanger_area, compute_pump_power, compute_turbine_power
from reactor.tools_economics import calculate_lcoe, calculate_payback_period
from reactor.tools_maintenance import calculate_refueling_outage_schedule, calculate_staff_requirements, calculate_availability_and_reliability
from reactor.simulation_fuel import calculate_fuel_cycle_length, calculate_reactivity_coefficients, calculate_shutdown_margin
from reactor.simulation_seismic import calculate_seismic_response, evaluate_seismic_margins
from reactor.tools_reliability import calculate_safety_system_reliability

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# 1. Document metadata
config = DocumentConfig(
    title="Small Modular Reactor Design Report",
    author="Nuclear Engineering Team",
    date="2025-05-18"
)
display(config)

# 2. Title
display(Title("# Small Modular Reactor (SMR) Design"))

# 3. Introduction
display(
    "## Introduction",
    "This report presents the design of a 20 MW electrical output small modular reactor (SMR) "
    "intended for distributed power generation. The design emphasizes safety, reliability, "
    "and ease of manufacturing to enable cost-effective deployment."
)

# 4. Core Parameters table
display(Title("## Reactor Core Design"))
df_core_params = pd.DataFrame([
    {"Parameter": "Thermal Power", "Value": f"{REACTOR_PARAMS.thermal_power}"},
    {"Parameter": "Electrical Power", "Value": f"{REACTOR_PARAMS.electrical_power}"},
    {"Parameter": "Thermal Efficiency", "Value": f"{REACTOR_PARAMS.efficiency*100:.1f}%"},
    {"Parameter": "Core Height", "Value": f"{REACTOR_PARAMS.core_height}"},
    {"Parameter": "Core Diameter", "Value": f"{REACTOR_PARAMS.core_diameter}"},
    {"Parameter": "Fuel Type", "Value": f"{REACTOR_PARAMS.fuel_type} at {REACTOR_PARAMS.enrichment}% enrichment"},
    {"Parameter": "Fuel Assemblies", "Value": f"{REACTOR_PARAMS.fuel_assemblies}"},
    {"Parameter": "Fuel Rods per Assembly", "Value": f"{REACTOR_PARAMS.fuel_rods_per_assembly}"},
    {"Parameter": "Control Rods", "Value": f"{REACTOR_PARAMS.control_rods}"},
    {"Parameter": "Design Life", "Value": f"{REACTOR_PARAMS.design_life} years"},
    {"Parameter": "Refueling Interval", "Value": f"{REACTOR_PARAMS.refueling_interval} years"},
])
display(Table(df_core_params, "Core Design Parameters", "tbl-core-params"))

# 5. Thermal Parameters table
display(Title("## Thermal-Hydraulic Design"))
df_thermal_params = pd.DataFrame([
    {"Parameter": "Primary Pressure", "Value": f"{THERMAL_PARAMS.primary_pressure}"},
    {"Parameter": "Primary Hot Leg Temperature", "Value": f"{THERMAL_PARAMS.primary_temp_hot}"},
    {"Parameter": "Primary Cold Leg Temperature", "Value": f"{THERMAL_PARAMS.primary_temp_cold}"},
    {"Parameter": "Primary Flow Rate", "Value": f"{THERMAL_PARAMS.primary_flow_rate}"},
    {"Parameter": "Primary Coolant", "Value": f"{THERMAL_PARAMS.primary_coolant}"},
    {"Parameter": "Secondary Pressure", "Value": f"{THERMAL_PARAMS.secondary_pressure}"},
    {"Parameter": "Secondary Hot Leg Temperature", "Value": f"{THERMAL_PARAMS.secondary_temp_hot}"},
    {"Parameter": "Secondary Cold Leg Temperature", "Value": f"{THERMAL_PARAMS.secondary_temp_cold}"},
    {"Parameter": "Heat Exchanger Type", "Value": f"{THERMAL_PARAMS.heat_exchanger_type}"},
    {"Parameter": "Heat Exchanger Material", "Value": f"{THERMAL_PARAMS.heat_exchanger_material}"},
    {"Parameter": "Turbine Type", "Value": f"{THERMAL_PARAMS.turbine_type}"},
    {"Parameter": "Turbine Efficiency", "Value": f"{THERMAL_PARAMS.turbine_efficiency*100:.1f}%"},
])
display(Table(df_thermal_params, "Thermal-Hydraulic Parameters", "tbl-thermal-params"))

# 6. Safety Parameters table
display(Title("## Safety Systems Design"))
df_safety_params = pd.DataFrame([
    {"Parameter": "Containment Type", "Value": f"{SAFETY_PARAMS.containment_type}"},
    {"Parameter": "Containment Thickness", "Value": f"{SAFETY_PARAMS.containment_thickness}"},
    {"Parameter": "Containment Design Pressure", "Value": f"{SAFETY_PARAMS.containment_design_pressure}"},
    {"Parameter": "Emergency Cooling System", "Value": f"{SAFETY_PARAMS.eccs_type}"},
    {"Parameter": "ECCS Water Volume", "Value": f"{SAFETY_PARAMS.eccs_water_volume}"},
    {"Parameter": "ECCS Activation Time", "Value": f"{SAFETY_PARAMS.eccs_activation_time}"},
    {"Parameter": "Passive Cooling Capacity", "Value": f"{SAFETY_PARAMS.passive_cooling_capacity}"},
    {"Parameter": "Passive Cooling Duration", "Value": f"{SAFETY_PARAMS.passive_cooling_duration}"},
    {"Parameter": "Radiation Shield Material", "Value": f"{SAFETY_PARAMS.radiation_shield_material}"},
    {"Parameter": "Radiation Shield Thickness", "Value": f"{SAFETY_PARAMS.radiation_shield_thickness}"},
    {"Parameter": "Seismic Design Basis", "Value": f"{SAFETY_PARAMS.seismic_design_basis}"},
    {"Parameter": "Safety Train Redundancy", "Value": f"{SAFETY_PARAMS.safety_train_redundancy}"},
])
display(Table(df_safety_params, "Safety System Parameters", "tbl-safety-params"))

# 7. System description & requirements
display("## System Architecture")
display(reactor_system.display())

# 8. Performance Analysis
power_density = compute_power_density()
temp_rise = compute_temperature_rise()
fuel_consumption = compute_fuel_consumption()
heat_exchanger_area = compute_heat_exchanger_area()
pump_power = compute_pump_power()
turbine_power = compute_turbine_power()

df_perf = pd.DataFrame([
    {"Metric": "Core Power Density", "Value": f"{power_density:.2f} MW/m³"},
    {"Metric": "Primary Loop Temperature Rise", "Value": f"{temp_rise:.2f} °C"},
    {"Metric": "Annual U-235 Consumption", "Value": f"{fuel_consumption:.2f} kg/year"},
    {"Metric": "Heat Exchanger Surface Area", "Value": f"{heat_exchanger_area:.2f} m²"},
    {"Metric": "Primary Pump Power", "Value": f"{pump_power:.2f} kW"},
    {"Metric": "Turbine Power Output", "Value": f"{turbine_power:.2f} MW"},
])
display(Title("## Performance Analysis"))
display(Table(df_perf, "Performance estimates", "tbl-perf"))

# 9. Fuel Cycle Analysis
fuel_cycle = calculate_fuel_cycle_length()
reactivity_coeffs = calculate_reactivity_coefficients()
shutdown_margin = calculate_shutdown_margin()

df_fuel = pd.DataFrame([
    {"Metric": "Total Uranium in Core", "Value": f"{fuel_cycle['total_uranium_mass']:.2f} kg"},
    {"Metric": "Average Power Density", "Value": f"{fuel_cycle['power_density_per_uranium']:.2f} MW/tU"},
    {"Metric": "Maximum Fuel Burnup", "Value": f"{fuel_cycle['max_burnup']:.2f} MWd/tU"},
    {"Metric": "Fuel Cycle Length", "Value": f"{fuel_cycle['cycle_length_efpd']:.2f} EFPD ({fuel_cycle['cycle_length_months']:.2f} months)"},
    {"Metric": "Doppler Coefficient", "Value": f"{reactivity_coeffs['doppler']:.2f} pcm/°C"},
    {"Metric": "Moderator Temperature Coefficient", "Value": f"{reactivity_coeffs['moderator_temperature']:.2f} pcm/°C"},
    {"Metric": "Shutdown Margin", "Value": f"{shutdown_margin['actual_margin']:.2f}% dk/k"},
])
display(Title("## Fuel Cycle Analysis"))
display(Table(df_fuel, "Fuel cycle parameters", "tbl-fuel"))

# 10. Operational Analysis
refueling_schedule = calculate_refueling_outage_schedule()
staffing = calculate_staff_requirements()
availability = calculate_availability_and_reliability()

df_ops = pd.DataFrame([
    {"Metric": "Refueling Outage Duration", "Value": f"{refueling_schedule['expected_outage_duration']:.2f} days"},
    {"Metric": "Lifetime Number of Refuelings", "Value": f"{refueling_schedule['lifetime_refuelings']}"},
    {"Metric": "Total Staff Requirement", "Value": f"{staffing['total_staff']} personnel"},
    {"Metric": "Operations Staff", "Value": f"{staffing['operations_staff']} personnel"},
    {"Metric": "Maintenance Staff", "Value": f"{staffing['maintenance_staff']} personnel"},
    {"Metric": "Technical Staff", "Value": f"{staffing['technical_staff']} personnel"},
    {"Metric": "Expected Capacity Factor", "Value": f"{availability['capacity_factor']:.2f}%"},
    {"Metric": "Forced Outage Rate", "Value": f"{availability['forced_outage_rate']:.2f}%"},
])
display(Title("## Operational Analysis"))
display(Table(df_ops, "Operational parameters", "tbl-ops"))

# 11. Economic Analysis
lcoe = calculate_lcoe()
payback = calculate_payback_period()

df_econ = pd.DataFrame([
    {"Metric": "Levelized Cost of Electricity (LCOE)", "Value": f"${lcoe:.2f}/MWh"},
    {"Metric": "Simple Payback Period", "Value": f"{payback:.2f} years"},
    {"Metric": "Staff Cost per MWh", "Value": f"${staffing['staff_cost_per_mwh']:.2f}/MWh"},
])
display(Title("## Economic Analysis"))
display(Table(df_econ, "Economic parameters", "tbl-econ"))

# 12. Key Suppliers and Manufacturing
display(Title("## Key Suppliers and Manufacturing"))
df_suppliers = pd.DataFrame([
    {"Component": "Reactor Pressure Vessel", "Supplier": "Japan Steel Works", "Manufacturing Technique": "Ring-forging"},
    {"Component": "Fuel Assemblies", "Supplier": "Westinghouse", "Manufacturing Technique": "Automated assembly line"},
    {"Component": "Control Rod Drives", "Supplier": "Rolls-Royce", "Manufacturing Technique": "Precision machining"},
    {"Component": "Primary Pumps", "Supplier": "Flowserve", "Manufacturing Technique": "Casting and precision machining"},
    {"Component": "Steam Generators", "Supplier": "BWXT", "Manufacturing Technique": "Tube expansion and welding"},
    {"Component": "Turbine-Generator", "Supplier": "GE Power", "Manufacturing Technique": "Blade milling and rotor balancing"},
    {"Component": "Containment Structure", "Supplier": "Bechtel", "Manufacturing Technique": "Slip-forming concrete"},
    {"Component": "I&C Systems", "Supplier": "Framatome", "Manufacturing Technique": "Digital system integration"},
    {"Component": "Neutron Monitoring", "Supplier": "Mirion Technologies", "Manufacturing Technique": "Precision electronics assembly"},
    {"Component": "Process Instrumentation", "Supplier": "Emerson Process Management", "Manufacturing Technique": "Calibrated sensor manufacturing"},
    {"Component": "Control Room Systems", "Supplier": "Westinghouse", "Manufacturing Technique": "Human-centered design and integration"},
])
display(Table(df_suppliers, "Key Suppliers and Manufacturing Techniques", "tbl-suppliers"))

# 13. Safety and Reliability Analysis
seismic_response = calculate_seismic_response(SAFETY_PARAMS.seismic_design_basis.magnitude)
seismic_margins = evaluate_seismic_margins()
safety_reliability = calculate_safety_system_reliability()

df_safety = pd.DataFrame([
    {"Metric": "Seismic Design Basis", "Value": f"{SAFETY_PARAMS.seismic_design_basis}"},
    {"Metric": "Building Fundamental Frequency", "Value": f"{seismic_response['building_fundamental_frequency']:.2f} Hz"},
    {"Metric": "Base Shear at Design Basis", "Value": f"{seismic_response['base_shear']:.2f} MN"},
    {"Metric": "Plant HCLPF Capacity", "Value": f"{seismic_margins['plant_hclpf']:.2f} g"},
    {"Metric": "Limiting Seismic Component", "Value": f"{seismic_margins['limiting_component']} (margin: {seismic_margins['limiting_margin']:.2f})"},
    {"Metric": "Safety System Reliability", "Value": f"{safety_reliability['overall_safety_system_reliability']:.6f}"},
    {"Metric": "Core Damage Frequency", "Value": f"{safety_reliability['core_damage_frequency']:.2e} per reactor-year"},
])
display(Title("## Safety and Reliability Analysis"))
display(Table(df_safety, "Safety and reliability metrics", "tbl-safety"))

# 14. Conclusion
display(
    Title("## Conclusion"),
    "This report presents a comprehensive design for a 20 MW electrical output small modular reactor. "
    "The design incorporates proven technologies from established suppliers to ensure reliability "
    "and ease of manufacturing. Key features include:",
    "- Compact core design with high power density",
    "- Passive safety systems for enhanced safety",
    "- Modular construction approach for cost reduction",
    "- Long refueling intervals for operational flexibility",
    "- Advanced instrumentation and control systems for reliable operation",
    "- Optimized fuel cycle for extended operation between refuelings",
    "- Robust seismic design with adequate safety margins",
    "- High reliability safety systems with redundancy",
    "",
    "The economic analysis shows a competitive LCOE of $" + f"{lcoe:.2f}" + "/MWh with a payback period of " + 
    f"{payback:.2f}" + " years. The design achieves a high capacity factor of " + f"{availability['capacity_factor']:.2f}" + "% "
    "through reliable components and optimized maintenance schedules.",
    "",
    "The safety analysis demonstrates that the plant can withstand the design basis earthquake of " +
    f"{SAFETY_PARAMS.seismic_design_basis.magnitude}" + " g with adequate margins, and the probabilistic risk assessment " +
    f"shows a core damage frequency of {safety_reliability['core_damage_frequency']:.2e} per reactor-year, well below " +
    "regulatory requirements.",
    "",
    "The next steps in the design process include detailed engineering, regulatory approval, "
    "and preparation for manufacturing and construction."
)

print("Enhanced design document generated with comprehensive analysis of performance, fuel cycle, operations, economics, and safety")
