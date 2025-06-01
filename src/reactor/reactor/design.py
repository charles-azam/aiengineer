"""
Main design file for the Small Modular Reactor (SMR).
"""

from pyforge.note import (Citation, DocumentConfig, Figure, Table, Title,
                          display)

from .parameters_reactor import REACTOR_PARAMS
from .simulation_reactor import (calculate_annual_energy_production,
                                 calculate_fuel_consumption,
                                 calculate_power_output,
                                 calculate_primary_loop_parameters,
                                 calculate_secondary_loop_parameters,
                                 run_all_simulations)
from .systems_reactor import (containment, primary_loop, reactor_core,
                              secondary_loop, smr_system)
from .tools_reactor import (calculate_containment_volume,
                            calculate_core_power_density,
                            calculate_core_volume, calculate_levelized_cost,
                            estimate_construction_time)

print("Loaded design module")

from pathlib import Path

import pandas as pd

# 1. Document metadata
config = DocumentConfig(
    title="Small Modular Reactor Design Report",
    author="Nuclear Engineering Team",
    date="2025-05-18",
)
display(config)

# 2. Title and introduction
display(Title("# Small Modular Reactor (SMR) Design"))

display(
    "## Executive Summary",
    "This report presents the design of a 20 MW electrical output Small Modular Reactor (SMR) "
    "that is optimized for cost-effectiveness and ease of industrialization. The design "
    "incorporates passive safety features, modular construction techniques, and a simplified "
    "system architecture to reduce construction time and operational complexity.",
)

# 3. Key parameters table
df_params = pd.DataFrame(
    [
        {"Parameter": "Thermal Output", "Value": f"{REACTOR_PARAMS.thermal_power}"},
        {
            "Parameter": "Electrical Output",
            "Value": f"{REACTOR_PARAMS.electrical_power}",
        },
        {
            "Parameter": "Thermal Efficiency",
            "Value": f"{REACTOR_PARAMS.thermal_efficiency*100:.1f}%",
        },
        {"Parameter": "Design Life", "Value": f"{REACTOR_PARAMS.design_life} years"},
        {
            "Parameter": "Refueling Interval",
            "Value": f"{REACTOR_PARAMS.refueling_interval} months",
        },
        {
            "Parameter": "Availability Factor",
            "Value": f"{REACTOR_PARAMS.availability_factor*100:.1f}%",
        },
        {
            "Parameter": "Core Dimensions",
            "Value": f"{REACTOR_PARAMS.core_height} × {REACTOR_PARAMS.core_diameter} (H×D)",
        },
        {
            "Parameter": "Containment Dimensions",
            "Value": f"{REACTOR_PARAMS.containment_height} × {REACTOR_PARAMS.containment_diameter} (H×D)",
        },
    ]
)
display(Table(df_params, "Core design parameters", "tbl-params"))

# 4. System description & requirements
display("## System Overview")
display(smr_system.display())

display("### Reactor Core")
display(reactor_core.display())

display("### Primary Coolant Loop")
display(primary_loop.display())

display("### Secondary Loop")
display(secondary_loop.display())

display("### Containment Structure")
display(containment.display())

# 5. Technical specifications
display(Title("## Technical Specifications"))

display("### Reactor Core Technology")
display(
    "The reactor core utilizes pressurized water reactor (PWR) technology with the following specifications:",
    "- **Fuel Type**: UO₂ ceramic pellets in zirconium alloy cladding",
    "- **Enrichment**: 4.95% U-235, below the 5% threshold for commercial fuel",
    "- **Core Configuration**: 37 fuel assemblies in a compact hexagonal arrangement",
    "- **Control System**: Control rod clusters with boron carbide neutron absorbers",
    "- **Manufacturer**: Westinghouse AP300 derived technology",
    "- **Materials**: Nuclear-grade zirconium alloys for fuel cladding, 316L stainless steel for structural components",
)

display("### Primary Loop Technology")
display(
    "The primary cooling system uses proven PWR technology with the following features:",
    "- **Coolant**: Light water (H₂O) at 15.5 MPa",
    "- **Configuration**: 2 coolant loops with integral steam generators",
    "- **Pumps**: Canned motor reactor coolant pumps by Flowserve",
    "- **Passive Safety**: Natural circulation capability for decay heat removal",
    "- **Materials**: 316L stainless steel for piping and components",
    "- **Manufacturing**: Factory-assembled modules with field welding of major connections",
)

display("### Secondary Loop Technology")
display(
    "The power conversion system employs a conventional Rankine cycle with the following components:",
    "- **Turbine**: Siemens SST-150 compact steam turbine",
    "- **Generator**: Brushless synchronous generator by ABB",
    "- **Condenser**: Shell and tube design with titanium tubes for corrosion resistance",
    "- **Feedwater System**: Integrated deaerator and feedwater heaters",
    "- **Materials**: Carbon steel for main steam lines, stainless steel for wet steam components",
    "- **Manufacturing**: Skid-mounted modular assembly for rapid installation",
)

display("### Containment Technology")
display(
    "The containment structure employs modern compact design with enhanced safety features:",
    "- **Design**: Steel-lined reinforced concrete structure",
    "- **Configuration**: Cylindrical design with hemispherical dome",
    "- **Passive Cooling**: External air cooling channels for containment heat removal",
    "- **Materials**: High-strength reinforced concrete with steel liner",
    "- **Manufacturing**: Modular construction with prefabricated steel sections and concrete pouring on site",
    "- **Provider**: Bechtel Corporation specialized nuclear construction",
)

# 6. Performance calculations
display(Title("## Performance Analysis"))

# Run simulations and get results
sim_results = run_all_simulations()

# Calculate additional metrics
core_volume = calculate_core_volume(
    REACTOR_PARAMS.core_height, REACTOR_PARAMS.core_diameter
)
power_density = calculate_core_power_density(REACTOR_PARAMS.thermal_power, core_volume)
construction_time = estimate_construction_time(REACTOR_PARAMS.electrical_power)
containment_volume = calculate_containment_volume(
    REACTOR_PARAMS.containment_height, REACTOR_PARAMS.containment_diameter
)

# Economic analysis
capital_cost = 5000 * REACTOR_PARAMS.electrical_power.magnitude  # $5000/kW
annual_om_cost = 40 * REACTOR_PARAMS.electrical_power.magnitude * 8760 * 0.9  # $40/MWh
fuel_cost = 7 * REACTOR_PARAMS.electrical_power.magnitude * 8760 * 0.9  # $7/MWh
decommissioning_cost = 500 * REACTOR_PARAMS.electrical_power.magnitude * 1000  # $500/kW
annual_energy = (
    REACTOR_PARAMS.electrical_power.magnitude
    * 8760
    * REACTOR_PARAMS.availability_factor
)
discount_rate = 0.07  # 7%

lcoe = calculate_levelized_cost(
    capital_cost,
    annual_om_cost,
    fuel_cost,
    decommissioning_cost,
    annual_energy,
    discount_rate,
    REACTOR_PARAMS.design_life,
)

# Display additional metrics
df_metrics = pd.DataFrame(
    [
        {"Metric": "Core Volume", "Value": f"{core_volume:.2f}"},
        {"Metric": "Power Density", "Value": f"{power_density:.2f}"},
        {"Metric": "Construction Time", "Value": f"{construction_time} months"},
        {"Metric": "Containment Volume", "Value": f"{containment_volume:.2f}"},
        {"Metric": "Levelized Cost of Electricity", "Value": f"${lcoe:.2f}/MWh"},
        {"Metric": "Capital Cost", "Value": f"${capital_cost/1e6:.1f} million"},
    ]
)
display(Table(df_metrics, "Performance and economic metrics", "tbl-metrics"))

# 7. Conclusion
display(
    Title("# Conclusion"),
    "This report presents a comprehensive design for a 20 MW Small Modular Reactor that "
    "balances performance, safety, and economic considerations. The design leverages "
    "proven PWR technology while incorporating modern passive safety features and "
    "modular construction techniques to reduce costs and construction time.",
    "",
    "Key advantages of this SMR design include:",
    "- **Modularity**: Factory fabrication of major components reduces on-site work",
    "- **Scalability**: Multiple units can be deployed to match demand growth",
    "- **Safety**: Passive safety systems eliminate dependence on external power",
    "- **Economics**: Competitive LCOE with reduced upfront capital requirements",
    "",
    "The next steps in the development process would include detailed engineering design, "
    "regulatory approval, and prototype construction to validate the design concepts.",
)

# Print key results for the next iteration
print(f"SMR Design: {REACTOR_PARAMS.electrical_power} electrical output")
print(f"Thermal efficiency: {REACTOR_PARAMS.thermal_efficiency*100:.1f}%")
print(f"Levelized cost: ${lcoe:.2f}/MWh")
print(f"Construction time: {construction_time} months")
