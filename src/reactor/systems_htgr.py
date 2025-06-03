"""
Hierarchical system definition for High-Temperature Gas-cooled Reactor (HTGR).
This module defines the complete system structure with all major subsystems
and their requirements.
"""

from pyforge import System, Requirement
from reactor.parameters_core import CORE_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
from reactor.parameters_modular import MODULAR_PARAMS

# Root HTGR system
htgr_system = System(
    name="High-Temperature Gas-cooled Reactor (HTGR)",
    description=(
        f"Modular HTGR system for industrial heat production with "
        f"{THERMAL_PARAMS.thermal_power.magnitude}{THERMAL_PARAMS.thermal_power.units} "
        f"thermal output and {CORE_PARAMS.core_outlet_temp.magnitude}"
        f"{CORE_PARAMS.core_outlet_temp.units} core outlet temperature"
    ),
    requirements=[
        Requirement(
            name="Thermal Power Output",
            description=(
                f"Deliver {THERMAL_PARAMS.thermal_power.magnitude}"
                f"{THERMAL_PARAMS.thermal_power.units} of thermal power for "
                f"industrial process heat applications"
            )
        ),
        Requirement(
            name="Operational Lifetime",
            description=(
                f"Maintain operational capability for {MODULAR_PARAMS.design_life} years "
                f"with minimal refueling requirements"
            )
        ),
        Requirement(
            name="Safety Performance",
            description=(
                f"Incorporate passive safety features to ensure containment of "
                f"radioactive materials under all credible accident scenarios"
            )
        ),
        Requirement(
            name="Modularity",
            description=(
                f"Design must be modular with factory-assembled components for "
                f"transportation to and installation at industrial sites"
            )
        )
    ]
)

# Core subsystem
core_subsystem = System(
    name="Reactor Core",
    description=(
        f"TRISO fuel-based reactor core operating at temperatures up to "
        f"{CORE_PARAMS.core_outlet_temp.magnitude}{CORE_PARAMS.core_outlet_temp.units}"
    ),
    requirements=[
        Requirement(
            name="Fuel Design",
            description=(
                f"Utilize TRISO fuel particles with {CORE_PARAMS.fuel_enrichment}% enriched uranium "
                f"to ensure fission product containment"
            )
        ),
        Requirement(
            name="Core Temperature",
            description=(
                f"Maintain core outlet temperature of {CORE_PARAMS.core_outlet_temp.magnitude}"
                f"{CORE_PARAMS.core_outlet_temp.units} during normal operation"
            )
        ),
        Requirement(
            name="Power Density",
            description=(
                f"Achieve power density of {CORE_PARAMS.power_density.magnitude}"
                f"{CORE_PARAMS.power_density.units} while maintaining fuel integrity"
            )
        ),
        Requirement(
            name="Reactivity Control",
            description=(
                f"Provide sufficient reactivity control margin of {CORE_PARAMS.reactivity_margin} "
                f"for safe shutdown under all conditions"
            )
        )
    ]
)

# Primary helium loop subsystem
primary_loop_subsystem = System(
    name="Primary Helium Loop",
    description=(
        f"Helium-based primary coolant loop operating at {THERMAL_PARAMS.primary_pressure.magnitude}"
        f"{THERMAL_PARAMS.primary_pressure.units} with flow rate of "
        f"{THERMAL_PARAMS.helium_flow_rate.magnitude}{THERMAL_PARAMS.helium_flow_rate.units}"
    ),
    requirements=[
        Requirement(
            name="Heat Transfer Capacity",
            description=(
                f"Transfer {THERMAL_PARAMS.thermal_power.magnitude}{THERMAL_PARAMS.thermal_power.units} "
                f"from the core to the secondary loop"
            )
        ),
        Requirement(
            name="Operating Pressure",
            description=(
                f"Maintain helium pressure at {THERMAL_PARAMS.primary_pressure.magnitude}"
                f"{THERMAL_PARAMS.primary_pressure.units} during normal operation"
            )
        ),
        Requirement(
            name="Flow Rate",
            description=(
                f"Provide helium flow rate of {THERMAL_PARAMS.helium_flow_rate.magnitude}"
                f"{THERMAL_PARAMS.helium_flow_rate.units} to ensure adequate cooling"
            )
        ),
        Requirement(
            name="Temperature Delta",
            description=(
                f"Maintain temperature difference of {THERMAL_PARAMS.primary_delta_t.magnitude}"
                f"{THERMAL_PARAMS.primary_delta_t.units} across the core"
            )
        )
    ]
)

# Secondary CO2 loop subsystem
secondary_loop_subsystem = System(
    name="Secondary CO2 Loop",
    description=(
        f"CO2-based secondary heat transfer loop for industrial process heat delivery "
        f"operating at {THERMAL_PARAMS.secondary_pressure.magnitude}{THERMAL_PARAMS.secondary_pressure.units}"
    ),
    requirements=[
        Requirement(
            name="Heat Delivery",
            description=(
                f"Deliver {THERMAL_PARAMS.process_heat_output.magnitude}"
                f"{THERMAL_PARAMS.process_heat_output.units} to industrial processes"
            )
        ),
        Requirement(
            name="Interface Compatibility",
            description=(
                f"Provide compatible interfaces for steam, hot air, and thermal oil "
                f"industrial heat systems"
            )
        ),
        Requirement(
            name="Operating Pressure",
            description=(
                f"Maintain CO2 pressure at {THERMAL_PARAMS.secondary_pressure.magnitude}"
                f"{THERMAL_PARAMS.secondary_pressure.units} during normal operation"
            )
        ),
        Requirement(
            name="Temperature Range",
            description=(
                f"Deliver process heat at temperatures between "
                f"{THERMAL_PARAMS.process_heat_min_temp.magnitude}{THERMAL_PARAMS.process_heat_min_temp.units} and "
                f"{THERMAL_PARAMS.process_heat_max_temp.magnitude}{THERMAL_PARAMS.process_heat_max_temp.units}"
            )
        )
    ]
)

# Safety systems
safety_systems = System(
    name="Safety Systems",
    description="Passive and active safety systems to ensure reactor integrity and public protection",
    requirements=[
        Requirement(
            name="Passive Heat Removal",
            description=(
                f"Remove decay heat passively with capacity of "
                f"{SAFETY_PARAMS.passive_cooling_capacity.magnitude}{SAFETY_PARAMS.passive_cooling_capacity.units} "
                f"without external power for {SAFETY_PARAMS.passive_cooling_duration} hours"
            )
        ),
        Requirement(
            name="Containment",
            description=(
                f"Provide containment structure with leak rate less than "
                f"{SAFETY_PARAMS.containment_leak_rate.magnitude}{SAFETY_PARAMS.containment_leak_rate.units} "
                f"under design basis accidents"
            )
        ),
        Requirement(
            name="Radiation Protection",
            description=(
                f"Limit maximum worker dose to {SAFETY_PARAMS.max_worker_dose.magnitude}"
                f"{SAFETY_PARAMS.max_worker_dose.units} per year and public dose to "
                f"{SAFETY_PARAMS.max_public_dose.magnitude}{SAFETY_PARAMS.max_public_dose.units} per year"
            )
        ),
        Requirement(
            name="Emergency Response",
            description=(
                f"Provide {SAFETY_PARAMS.emergency_response_time} minutes of operator response time "
                f"for any credible accident scenario"
            )
        )
    ]
)

# Modular structure and interfaces
modular_structure = System(
    name="Modular Structure and Interfaces",
    description=(
        f"Modular design approach with standardized components and interfaces "
        f"for factory assembly and site installation"
    ),
    requirements=[
        Requirement(
            name="Module Size",
            description=(
                f"Limit individual module dimensions to {MODULAR_PARAMS.max_module_width.magnitude}"
                f"{MODULAR_PARAMS.max_module_width.units} width, {MODULAR_PARAMS.max_module_length.magnitude}"
                f"{MODULAR_PARAMS.max_module_length.units} length for transportability"
            )
        ),
        Requirement(
            name="Assembly Time",
            description=(
                f"Enable complete on-site assembly within {MODULAR_PARAMS.assembly_time} months "
                f"from module delivery"
            )
        ),
        Requirement(
            name="Scalability",
            description=(
                f"Support scalable configurations of {MODULAR_PARAMS.min_modules} to "
                f"{MODULAR_PARAMS.max_modules} modules per installation"
            )
        ),
        Requirement(
            name="Site Footprint",
            description=(
                f"Require maximum site area of {MODULAR_PARAMS.site_area.magnitude}"
                f"{MODULAR_PARAMS.site_area.units} for complete installation"
            )
        )
    ]
)

# Control and instrumentation
control_instrumentation = System(
    name="Control and Instrumentation",
    description="Digital control systems for reactor operation, monitoring, and safety functions",
    requirements=[
        Requirement(
            name="Control System",
            description=(
                f"Provide automated control with manual override capability and "
                f"{SAFETY_PARAMS.control_redundancy}x redundancy for critical functions"
            )
        ),
        Requirement(
            name="Monitoring Coverage",
            description=(
                f"Monitor {SAFETY_PARAMS.monitored_parameters} critical parameters "
                f"with {SAFETY_PARAMS.sensor_redundancy}x sensor redundancy"
            )
        ),
        Requirement(
            name="Response Time",
            description=(
                f"Ensure control system response time of less than "
                f"{SAFETY_PARAMS.control_response_time.magnitude}{SAFETY_PARAMS.control_response_time.units} "
                f"for safety-critical functions"
            )
        ),
        Requirement(
            name="Remote Operation",
            description=(
                f"Support remote monitoring and limited operation capabilities "
                f"from centralized control facilities"
            )
        )
    ]
)

# Add subsystems to the main HTGR system
htgr_system.add_subsystem(core_subsystem)
htgr_system.add_subsystem(primary_loop_subsystem)
htgr_system.add_subsystem(secondary_loop_subsystem)
htgr_system.add_subsystem(safety_systems)
htgr_system.add_subsystem(modular_structure)
htgr_system.add_subsystem(control_instrumentation)

# Print system structure for verification
print("HTGR System Structure:")
print(htgr_system.display())
print("HTGR System Definition Complete")
"""
System definitions for the High-Temperature Gas-cooled Reactor (HTGR).
Defines the hierarchical system structure using pyforge.
"""

from pyforge import System, Requirement
from reactor.parameters_htgr import (
    CORE_PARAMS, THERMAL_PARAMS, FUEL_PARAMS, 
    HX_PARAMS, OPERATIONAL_PARAMS, SAFETY_PARAMS
)

# Root HTGR system
htgr_system = System(
    name="Modular HTGR System",
    description=(
        f"High-Temperature Gas-cooled Reactor system for industrial heat applications, "
        f"with thermal power options of {CORE_PARAMS.thermal_power_small}, "
        f"{CORE_PARAMS.thermal_power_medium}, and {CORE_PARAMS.thermal_power_large}, "
        f"delivering process heat at up to {THERMAL_PARAMS.core_outlet_temp}."
    ),
    requirements=[
        Requirement(
            name="Industrial Heat Supply",
            description=(
                f"Deliver process heat at temperatures up to {THERMAL_PARAMS.core_outlet_temp} "
                f"for industrial applications."
            )
        ),
        Requirement(
            name="Passive Safety",
            description=(
                f"Maintain core integrity without active cooling for at least "
                f"{SAFETY_PARAMS.passive_cooling_duration}."
            )
        ),
        Requirement(
            name="Operational Lifetime",
            description=(
                f"Operate for {OPERATIONAL_PARAMS.design_life} with refueling "
                f"every {OPERATIONAL_PARAMS.refueling_interval}."
            )
        ),
        Requirement(
            name="Modular Design",
            description=(
                "Enable factory fabrication and modular installation with minimal "
                "on-site construction."
            )
        )
    ]
)

# Reactor Core subsystem
reactor_core = System(
    name="Reactor Core",
    description=(
        f"Cylindrical core with graphite moderator and TRISO fuel, "
        f"{CORE_PARAMS.core_height} high and {CORE_PARAMS.core_diameter} in diameter."
    ),
    requirements=[
        Requirement(
            name="Power Generation",
            description=(
                f"Generate thermal power of {CORE_PARAMS.thermal_power_large} "
                f"at a power density of {CORE_PARAMS.power_density}."
            )
        ),
        Requirement(
            name="Temperature Limit",
            description=(
                f"Maintain fuel temperature below {FUEL_PARAMS.failure_temp} "
                f"under all conditions."
            )
        )
    ],
    parent=htgr_system
)

# Fuel System
fuel_system = System(
    name="TRISO Fuel System",
    description=(
        f"TRISO fuel particles with {FUEL_PARAMS.kernel_material} kernels of "
        f"{FUEL_PARAMS.kernel_diameter} diameter and {FUEL_PARAMS.enrichment} enrichment."
    ),
    requirements=[
        Requirement(
            name="Fission Product Retention",
            description=(
                f"Retain > {SAFETY_PARAMS.fission_product_retention * 100}% of fission products "
                f"within fuel particles up to {FUEL_PARAMS.failure_temp}."
            )
        ),
        Requirement(
            name="Fuel Lifetime",
            description=(
                f"Maintain integrity for {OPERATIONAL_PARAMS.refueling_interval} "
                f"of operation."
            )
        )
    ],
    parent=reactor_core
)

# Primary Cooling System
primary_cooling = System(
    name="Primary Cooling System",
    description=(
        f"Helium cooling system operating at {THERMAL_PARAMS.primary_pressure} "
        f"with inlet temperature of {THERMAL_PARAMS.core_inlet_temp} and outlet "
        f"temperature of {THERMAL_PARAMS.core_outlet_temp}."
    ),
    requirements=[
        Requirement(
            name="Heat Removal",
            description=(
                f"Remove {CORE_PARAMS.thermal_power_large} of thermal power "
                f"with a temperature rise of {THERMAL_PARAMS.core_outlet_temp.magnitude - THERMAL_PARAMS.core_inlet_temp.magnitude}°C."
            )
        ),
        Requirement(
            name="Pressure Maintenance",
            description=(
                f"Maintain helium pressure at {THERMAL_PARAMS.primary_pressure} "
                f"during normal operation."
            )
        )
    ],
    parent=htgr_system
)

# Secondary Heat Transfer System
secondary_system = System(
    name="Secondary Heat Transfer System",
    description=(
        f"CO2 secondary loop operating at {THERMAL_PARAMS.secondary_pressure} "
        f"with maximum temperature of {THERMAL_PARAMS.secondary_max_temp}."
    ),
    requirements=[
        Requirement(
            name="Heat Transfer",
            description=(
                f"Transfer {CORE_PARAMS.thermal_power_large} of thermal power "
                f"with {OPERATIONAL_PARAMS.thermal_efficiency * 100}% efficiency."
            )
        ),
        Requirement(
            name="Industrial Interface",
            description=(
                "Provide flexible heat delivery options including steam, hot air, "
                "and thermal oil interfaces."
            )
        )
    ],
    parent=htgr_system
)

# Intermediate Heat Exchanger
heat_exchanger = System(
    name="Intermediate Heat Exchanger",
    description=(
        f"{HX_PARAMS.type} heat exchanger with {HX_PARAMS.effectiveness * 100}% "
        f"effectiveness, made of {HX_PARAMS.material}."
    ),
    requirements=[
        Requirement(
            name="Heat Transfer Capacity",
            description=(
                f"Transfer {HX_PARAMS.capacity} of thermal power from helium to CO2."
            )
        ),
        Requirement(
            name="Pressure Boundary",
            description=(
                "Maintain separation between primary and secondary loops under all "
                "operating conditions."
            )
        )
    ],
    parent=secondary_system
)

# Safety Systems
safety_systems = System(
    name="Safety Systems",
    description=(
        "Passive and inherent safety features ensuring core integrity and "
        "fission product retention under all conditions."
    ),
    requirements=[
        Requirement(
            name="Passive Heat Removal",
            description=(
                f"Remove decay heat passively for {SAFETY_PARAMS.passive_cooling_duration} "
                f"without exceeding {SAFETY_PARAMS.max_accident_temp}."
            )
        ),
        Requirement(
            name="Reactivity Control",
            description=(
                "Provide redundant means of reactor shutdown and maintain "
                "subcriticality under all conditions."
            )
        )
    ],
    parent=htgr_system
)

# Control and Instrumentation System
control_system = System(
    name="Control and Instrumentation",
    description=(
        "Digital control system with redundant safety-related instrumentation "
        "and operator interfaces."
    ),
    requirements=[
        Requirement(
            name="Normal Operation Control",
            description=(
                "Maintain reactor parameters within normal operating range during "
                "steady-state and transient conditions."
            )
        ),
        Requirement(
            name="Safety Monitoring",
            description=(
                "Monitor and display all safety-related parameters and initiate "
                "protective actions when required."
            )
        )
    ],
    parent=htgr_system
)

print("HTGR system hierarchy defined with requirements")
"""
System definitions for the High-Temperature Gas-cooled Reactor (HTGR).
"""
from pyforge import System, Requirement
from reactor.parameters_core import CORE_PARAMS
from reactor.parameters_fuel import FUEL_PARAMS
from reactor.parameters_coolant import COOLANT_PARAMS

# Root HTGR system
htgr_system = System(
    name="Modular High-Temperature Gas-cooled Reactor System",
    description=(
        f"Modular HTGR system with thermal power options of "
        f"{CORE_PARAMS.thermal_power_small.magnitude}, "
        f"{CORE_PARAMS.thermal_power_medium.magnitude}, or "
        f"{CORE_PARAMS.thermal_power_large.magnitude} MW, "
        f"utilizing TRISO fuel and helium coolant for industrial heat applications"
    ),
    requirements=[
        Requirement(
            name="Thermal Output",
            description=(
                f"Deliver thermal power of 10-20 MW at "
                f"{CORE_PARAMS.core_outlet_temp.magnitude}°C"
            )
        ),
        Requirement(
            name="Safety Performance",
            description=(
                f"Maintain passive safety with no operator action for at least 72 hours "
                f"and prevent fuel temperature from exceeding "
                f"{FUEL_PARAMS.failure_temperature.magnitude}°C in any accident scenario"
            )
        ),
        Requirement(
            name="Design Life",
            description=(
                f"Operate for {CORE_PARAMS.design_life.magnitude} years with "
                f"refueling every {CORE_PARAMS.refueling_interval.magnitude} years"
            )
        )
    ]
)

# Reactor Core subsystem
reactor_core = System(
    name="Reactor Core",
    description=(
        f"Cylindrical core with graphite moderator and TRISO fuel, "
        f"operating at temperatures up to {CORE_PARAMS.core_outlet_temp.magnitude}°C"
    ),
    requirements=[
        Requirement(
            name="Power Density",
            description=(
                f"Maintain power density of {CORE_PARAMS.power_density.magnitude} MW/m³"
            )
        ),
        Requirement(
            name="Temperature Limits",
            description=(
                f"Maintain core outlet temperature at {CORE_PARAMS.core_outlet_temp.magnitude}°C "
                f"and inlet temperature at {CORE_PARAMS.core_inlet_temp.magnitude}°C"
            )
        )
    ],
    parent=htgr_system
)

# Primary Cooling System
primary_cooling = System(
    name="Primary Cooling System",
    description=(
        f"Helium-based cooling system operating at {CORE_PARAMS.primary_pressure.magnitude} MPa"
    ),
    requirements=[
        Requirement(
            name="Heat Removal",
            description=(
                f"Remove up to {CORE_PARAMS.thermal_power_large.magnitude} MW of thermal power "
                f"with a temperature rise of {CORE_PARAMS.temp_differential.magnitude}°C"
            )
        ),
        Requirement(
            name="Flow Rate",
            description=(
                f"Provide helium flow rate of up to {COOLANT_PARAMS.helium_flow_rate_large.magnitude} kg/s"
            )
        )
    ],
    parent=htgr_system
)

# Secondary Heat Transfer System
secondary_heat = System(
    name="Secondary Heat Transfer System",
    description=(
        f"CO2-based heat transfer system operating at {COOLANT_PARAMS.secondary_pressure.magnitude} MPa"
    ),
    requirements=[
        Requirement(
            name="Heat Transfer",
            description=(
                f"Transfer up to {CORE_PARAMS.thermal_power_large.magnitude} MW of thermal power "
                f"to industrial processes at temperatures up to {COOLANT_PARAMS.secondary_max_temp.magnitude}°C"
            )
        ),
        Requirement(
            name="Flow Rate",
            description=(
                f"Provide CO2 flow rate of up to {COOLANT_PARAMS.co2_flow_rate_large.magnitude} kg/s"
            )
        )
    ],
    parent=htgr_system
)

# Safety Systems
safety_systems = System(
    name="Safety Systems",
    description=(
        "Passive and inherent safety features ensuring core cooling and "
        "fission product containment under all credible accident scenarios"
    ),
    requirements=[
        Requirement(
            name="Passive Heat Removal",
            description=(
                "Remove decay heat passively for at least 7 days without external power"
            )
        ),
        Requirement(
            name="Fission Product Containment",
            description=(
                f"Retain >99.9% of fission products within TRISO particles "
                f"up to {FUEL_PARAMS.failure_temperature.magnitude}°C"
            )
        )
    ],
    parent=htgr_system
)

print("HTGR system hierarchy defined with all major subsystems")
