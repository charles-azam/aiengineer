"""
High-Temperature Gas-cooled Reactor (HTGR) system hierarchy.
This module defines the complete system structure for the HTGR
using pyforge Systems and Requirements.
"""
from pyforge import System, Requirement
from reactor.parameters_htgr import HTGR_PARAMS

print("Loading HTGR system definitions...")

# Top level HTGR system
htgr_system = System(
    name="High-Temperature Gas-cooled Reactor",
    description=(
        f"Modular HTGR system providing {HTGR_PARAMS.selected_power} "
        f"of industrial heat at temperatures up to {HTGR_PARAMS.core_outlet_temperature}"
    ),
    requirements=[
        Requirement(
            name="Thermal Output",
            description=f"Deliver {HTGR_PARAMS.selected_power} thermal power"
        ),
        Requirement(
            name="Operating Temperature",
            description=f"Maintain core outlet temperature of {HTGR_PARAMS.core_outlet_temperature}"
        ),
        Requirement(
            name="Design Life",
            description=f"Operational lifetime of {HTGR_PARAMS.design_lifetime}"
        ),
        Requirement(
            name="Modularity",
            description="System must be modular and scalable for various industrial sites"
        )
    ]
)

# Reactor Core subsystem
reactor_core = System(
    name="Reactor Core",
    description="HTGR core containing TRISO fuel elements and moderator",
    requirements=[
        Requirement(
            name="Power Density",
            description=f"Maintain power density of {HTGR_PARAMS.power_density}"
        ),
        Requirement(
            name="Temperature Limit",
            description=f"Maximum core temperature below {HTGR_PARAMS.core_outlet_temperature}"
        ),
        Requirement(
            name="Core Geometry",
            description=f"Core diameter of {HTGR_PARAMS.core_diameter} and height of {HTGR_PARAMS.core_height}"
        )
    ],
    parent=htgr_system
)

# Fuel System subsystem
fuel_system = System(
    name="Fuel System",
    description="TRISO fuel particles in graphite matrix",
    requirements=[
        Requirement(
            name="Fuel Type",
            description="TRISO coated fuel particles with multiple containment layers"
        ),
        Requirement(
            name="Enrichment",
            description=f"Uranium enrichment of {HTGR_PARAMS.fuel_enrichment}"
        ),
        Requirement(
            name="Fuel Lifetime",
            description=f"Minimum {HTGR_PARAMS.fuel_cycle_length} between refueling"
        )
    ],
    parent=reactor_core
)

# Primary Coolant System
primary_coolant_system = System(
    name="Primary Coolant System",
    description="Helium-based primary cooling circuit",
    requirements=[
        Requirement(
            name="Coolant Type",
            description="Helium gas coolant"
        ),
        Requirement(
            name="Flow Rate",
            description=f"Maintain helium flow rate of {HTGR_PARAMS.helium_flow_rate}"
        ),
        Requirement(
            name="Operating Pressure",
            description=f"Maintain helium pressure of {HTGR_PARAMS.helium_pressure}"
        ),
        Requirement(
            name="Temperature Rise",
            description=(
                f"Temperature rise from {HTGR_PARAMS.core_inlet_temperature} to "
                f"{HTGR_PARAMS.core_outlet_temperature} across core"
            )
        )
    ],
    parent=htgr_system
)

# Secondary Coolant System
secondary_coolant_system = System(
    name="Secondary Coolant System",
    description="CO2-based secondary heat transfer loop",
    requirements=[
        Requirement(
            name="Coolant Type",
            description="Carbon dioxide (CO2) coolant"
        ),
        Requirement(
            name="Flow Rate",
            description=f"Maintain CO2 flow rate of {HTGR_PARAMS.secondary_flow_rate}"
        ),
        Requirement(
            name="Operating Pressure",
            description=f"Maintain CO2 pressure of {HTGR_PARAMS.secondary_pressure}"
        ),
        Requirement(
            name="Industrial Compatibility",
            description="Compatible with existing industrial heat systems"
        )
    ],
    parent=htgr_system
)

# Safety Systems
safety_systems = System(
    name="Safety Systems",
    description="Passive and active safety features",
    requirements=[
        Requirement(
            name="Passive Heat Removal",
            description="Passive decay heat removal capability"
        ),
        Requirement(
            name="Containment",
            description="Multiple barriers for fission product containment"
        ),
        Requirement(
            name="Emergency Shutdown",
            description=f"Reactor shutdown within {HTGR_PARAMS.emergency_shutdown_time} under emergency conditions"
        ),
        Requirement(
            name="Radiation Protection",
            description=f"Limit radiation exposure to less than {HTGR_PARAMS.radiation_exposure_limit}"
        )
    ],
    parent=htgr_system
)

# Control Systems
control_systems = System(
    name="Control Systems",
    description="Reactor control and instrumentation",
    requirements=[
        Requirement(
            name="Power Control",
            description="Maintain power output within ±2% of setpoint"
        ),
        Requirement(
            name="Temperature Control",
            description=f"Maintain outlet temperature within ±{HTGR_PARAMS.temperature_tolerance}"
        ),
        Requirement(
            name="Monitoring",
            description="Continuous monitoring of all critical parameters"
        ),
        Requirement(
            name="Automation",
            description="Automated operation with minimal operator intervention"
        )
    ],
    parent=htgr_system
)

# Heat Transfer System
heat_transfer_system = System(
    name="Heat Transfer System",
    description="System for transferring heat to industrial processes",
    requirements=[
        Requirement(
            name="Heat Exchanger Efficiency",
            description=f"Minimum efficiency of {HTGR_PARAMS.heat_exchanger_efficiency}"
        ),
        Requirement(
            name="Output Media",
            description="Capable of delivering heat via steam, hot air, or thermal oil"
        ),
        Requirement(
            name="Temperature Range",
            description=f"Deliver process heat at {HTGR_PARAMS.process_temperature}"
        ),
        Requirement(
            name="Industrial Interface",
            description="Standardized connections to industrial heat consumers"
        )
    ],
    parent=htgr_system
)

# Print system hierarchy for verification
print("HTGR System Hierarchy:")
print(htgr_system.display())
print("DESIGN_COMPLETE")

# Export the htgr_system for use in other modules
__all__ = ["htgr_system"]
