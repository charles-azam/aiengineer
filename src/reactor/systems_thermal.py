"""
Thermal-hydraulic subsystem for the High-Temperature Gas-cooled Reactor (HTGR).

This module defines the structure of the thermal-hydraulic subsystem using
pyforge.System class, including the primary helium loop, secondary CO2 loop,
heat exchangers, and interfaces for industrial heat applications.
"""

from pyforge import System, Requirement
from reactor.parameters_thermal import (
    THERMAL_PARAMS,
    PRIMARY_LOOP_PARAMS,
    SECONDARY_LOOP_PARAMS,
    IHX_PARAMS
)

# Primary Helium Loop System
primary_helium_loop = System(
    name="Primary Helium Loop",
    description=f"Helium coolant loop operating at {THERMAL_PARAMS.core_outlet_temperature} "
                f"with flow rate of {PRIMARY_LOOP_PARAMS.mass_flow_rate}",
    requirements=[
        Requirement(
            name="Operating Temperature",
            description=f"Maintain core outlet temperature of {THERMAL_PARAMS.core_outlet_temperature} "
                        f"and inlet temperature of {THERMAL_PARAMS.core_inlet_temperature}"
        ),
        Requirement(
            name="Operating Pressure",
            description=f"Maintain system pressure of {THERMAL_PARAMS.core_pressure}"
        ),
        Requirement(
            name="Flow Rate",
            description=f"Maintain helium flow rate of {PRIMARY_LOOP_PARAMS.mass_flow_rate}"
        ),
        Requirement(
            name="Heat Transfer",
            description=f"Transfer {THERMAL_PARAMS.core_thermal_power_options['medium']} of thermal power from reactor core"
        )
    ]
)

# Helium Circulators System
helium_circulators = System(
    name="Helium Circulators",
    description=f"Helium circulators with {PRIMARY_LOOP_PARAMS.circulator_efficiency * 100}% efficiency",
    requirements=[
        Requirement(
            name="Flow Generation",
            description=f"Generate helium flow of {PRIMARY_LOOP_PARAMS.mass_flow_rate}"
        ),
        Requirement(
            name="Pressure Head",
            description=f"Provide pressure head to overcome {PRIMARY_LOOP_PARAMS.design_pressure_drop}"
        ),
        Requirement(
            name="Reliability",
            description=f"Achieve high reliability over {THERMAL_PARAMS.design_life} years of operation"
        )
    ]
)

# Secondary CO2 Loop System
secondary_co2_loop = System(
    name="Secondary CO2 Loop",
    description=f"CO2 heat transfer loop operating at {SECONDARY_LOOP_PARAMS.co2_outlet_temperature} "
                f"with flow rate of {SECONDARY_LOOP_PARAMS.mass_flow_rate}",
    requirements=[
        Requirement(
            name="Operating Temperature",
            description=f"Operate between {SECONDARY_LOOP_PARAMS.co2_inlet_temperature} and "
                        f"{SECONDARY_LOOP_PARAMS.co2_outlet_temperature}"
        ),
        Requirement(
            name="Operating Pressure",
            description=f"Maintain system pressure of {SECONDARY_LOOP_PARAMS.co2_pressure}"
        ),
        Requirement(
            name="Flow Rate",
            description=f"Maintain CO2 flow rate of {SECONDARY_LOOP_PARAMS.mass_flow_rate}"
        ),
        Requirement(
            name="Heat Transfer",
            description=f"Transfer {THERMAL_PARAMS.core_thermal_power_options['medium']} of thermal power to industrial applications"
        )
    ]
)

# CO2 Compressors System
co2_compressors = System(
    name="CO2 Compressors",
    description=f"CO2 compressors with {SECONDARY_LOOP_PARAMS.compressor_efficiency * 100}% efficiency",
    requirements=[
        Requirement(
            name="Flow Generation",
            description=f"Generate CO2 flow of {SECONDARY_LOOP_PARAMS.mass_flow_rate}"
        ),
        Requirement(
            name="Pressure Ratio",
            description=f"Provide pressure ratio of {SECONDARY_LOOP_PARAMS.pressure_ratio}"
        ),
        Requirement(
            name="Reliability",
            description=f"Achieve high reliability over {THERMAL_PARAMS.design_life} years of operation"
        )
    ]
)

# Intermediate Heat Exchanger System
intermediate_heat_exchanger = System(
    name="Intermediate Heat Exchanger",
    description=f"{IHX_PARAMS.type} heat exchanger with {IHX_PARAMS.heat_transfer_capacity} "
                f"capacity and {IHX_PARAMS.effectiveness} effectiveness",
    requirements=[
        Requirement(
            name="Heat Transfer Capacity",
            description=f"Transfer {IHX_PARAMS.heat_transfer_capacity} between primary and secondary loops"
        ),
        Requirement(
            name="Temperature Effectiveness",
            description=f"Achieve heat exchange effectiveness of {IHX_PARAMS.effectiveness}"
        ),
        Requirement(
            name="Pressure Drop",
            description=f"Limit pressure drop to {IHX_PARAMS.primary_pressure_drop} on primary side and "
                        f"{IHX_PARAMS.secondary_pressure_drop} on secondary side"
        ),
        Requirement(
            name="Design Life",
            description=f"Operate reliably for {IHX_PARAMS.design_life}"
        )
    ]
)

# Piping Systems
piping_systems = System(
    name="Piping Systems",
    description=f"High-temperature piping systems for helium and CO2 loops",
    requirements=[
        Requirement(
            name="Temperature Resistance",
            description=f"Withstand temperatures up to {THERMAL_PARAMS.core_outlet_temperature}"
        ),
        Requirement(
            name="Pressure Rating",
            description=f"Withstand pressures up to {THERMAL_PARAMS.core_pressure}"
        ),
        Requirement(
            name="Thermal Insulation",
            description=f"Limit heat loss with {THERMAL_PARAMS.insulation_thickness} insulation"
        ),
        Requirement(
            name="Design Life",
            description=f"Maintain integrity for {THERMAL_PARAMS.design_life} years"
        )
    ]
)

# Heat Delivery Interface System
heat_delivery_interface = System(
    name="Heat Delivery Interface",
    description=f"Interface for delivering heat to industrial applications",
    requirements=[
        Requirement(
            name="Temperature Range",
            description=f"Deliver heat at temperatures between {THERMAL_PARAMS.industrial_steam_temperature} and "
                        f"{THERMAL_PARAMS.industrial_hot_air_temperature}"
        ),
        Requirement(
            name="Heat Transfer Capacity",
            description=f"Transfer up to {THERMAL_PARAMS.core_thermal_power_options['medium']} to industrial processes"
        ),
        Requirement(
            name="Medium Compatibility",
            description=f"Support heat delivery via steam, hot air, and thermal oil"
        ),
        Requirement(
            name="Control System",
            description=f"Maintain temperature control within industrial requirements"
        )
    ]
)

# Overall Thermal-Hydraulic System
thermal_hydraulic_system = System(
    name="Thermal-Hydraulic System",
    description=f"Complete thermal-hydraulic system for {THERMAL_PARAMS.core_thermal_power_options['medium']} HTGR",
    subsystems=[
        primary_helium_loop,
        helium_circulators,
        intermediate_heat_exchanger,
        secondary_co2_loop,
        co2_compressors,
        piping_systems,
        heat_delivery_interface
    ],
    requirements=[
        Requirement(
            name="Thermal Power Output",
            description=f"Deliver {THERMAL_PARAMS.core_thermal_power_options['medium']} thermal power to industrial applications"
        ),
        Requirement(
            name="System Efficiency",
            description=f"Achieve thermal efficiency of at least {THERMAL_PARAMS.thermal_efficiency * 100}%"
        ),
        Requirement(
            name="Operational Lifetime",
            description=f"Operate reliably for {THERMAL_PARAMS.design_life} years"
        ),
        Requirement(
            name="Safety",
            description="Incorporate passive safety features for decay heat removal"
        ),
        Requirement(
            name="Modularity",
            description="Design system to be modular and scalable for different industrial applications"
        )
    ]
)

# Print system structure for verification
print("Thermal-Hydraulic System Structure:")
print(thermal_hydraulic_system.display())
print("THERMAL_HYDRAULIC_SYSTEM_DEFINED with fixed imports")
