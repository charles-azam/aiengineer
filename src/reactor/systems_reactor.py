"""
Systems definition for the Small Modular Reactor.
Defines the hierarchical system structure and requirements.
"""

from pyforge import System, Requirement
from reactor.parameters_reactor import (REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, 
                                       SECONDARY_LOOP_PARAMS, CONTAINMENT_PARAMS)

# Root system
smr_system = System(
    name="20 MW Small Modular Reactor",
    description=(
        f"A {REACTOR_PARAMS.electrical_power.magnitude}{REACTOR_PARAMS.electrical_power.units} "
        f"small modular reactor with a design lifetime of "
        f"{REACTOR_PARAMS.design_lifetime.magnitude}{REACTOR_PARAMS.design_lifetime.units}."
    ),
    requirements=[
        Requirement(
            name="Power Output",
            description=(
                f"The reactor shall produce {REACTOR_PARAMS.electrical_power.magnitude}"
                f"{REACTOR_PARAMS.electrical_power.units} of electrical power."
            )
        ),
        Requirement(
            name="Design Lifetime",
            description=(
                f"The reactor shall have a design lifetime of at least "
                f"{REACTOR_PARAMS.design_lifetime.magnitude}{REACTOR_PARAMS.design_lifetime.units}."
            )
        ),
        Requirement(
            name="Safety",
            description=(
                "The reactor shall incorporate passive safety features to ensure safe operation "
                "and shutdown without operator intervention or external power for at least 72 hours."
            )
        ),
        Requirement(
            name="Manufacturability",
            description=(
                "The reactor shall be designed for factory fabrication and modular assembly "
                "to reduce construction time and costs."
            )
        ),
    ]
)

# Reactor Core System
reactor_core_system = System(
    name="Reactor Core System",
    description=(
        f"A {REACTOR_PARAMS.thermal_power.magnitude}{REACTOR_PARAMS.thermal_power.units} thermal "
        f"reactor core using {REACTOR_PARAMS.fuel_type} fuel with "
        f"{REACTOR_PARAMS.fuel_enrichment.magnitude}{REACTOR_PARAMS.fuel_enrichment.units} enrichment."
    ),
    requirements=[
        Requirement(
            name="Thermal Power",
            description=(
                f"The reactor core shall produce {REACTOR_PARAMS.thermal_power.magnitude}"
                f"{REACTOR_PARAMS.thermal_power.units} of thermal power."
            )
        ),
        Requirement(
            name="Fuel Specifications",
            description=(
                f"The reactor shall use {REACTOR_PARAMS.fuel_type} fuel with "
                f"{REACTOR_PARAMS.fuel_enrichment.magnitude}{REACTOR_PARAMS.fuel_enrichment.units} enrichment, "
                f"arranged in {REACTOR_PARAMS.fuel_assembly_count} assemblies."
            )
        ),
        Requirement(
            name="Temperature Limits",
            description=(
                f"The maximum fuel temperature shall not exceed "
                f"{REACTOR_PARAMS.max_fuel_temperature.magnitude}{REACTOR_PARAMS.max_fuel_temperature.units} "
                f"during normal operation or anticipated operational occurrences."
            )
        ),
        Requirement(
            name="Refueling Interval",
            description=(
                f"The reactor shall operate for {REACTOR_PARAMS.refueling_interval.magnitude}"
                f"{REACTOR_PARAMS.refueling_interval.units} between refueling outages."
            )
        ),
    ]
)

# Control and Protection System
control_system = System(
    name="Reactor Control and Protection System",
    description=(
        "Control and protection system for safe operation and shutdown of the reactor."
    ),
    requirements=[
        Requirement(
            name="Reactivity Control",
            description=(
                "The system shall provide precise control of reactor power through control rod "
                "movement and soluble boron concentration."
            )
        ),
        Requirement(
            name="Shutdown Capability",
            description=(
                "The system shall be capable of shutting down the reactor from any operational "
                "state and maintaining subcriticality."
            )
        ),
        Requirement(
            name="Redundancy",
            description=(
                "The protection system shall incorporate triple redundancy with 2-out-of-3 "
                "voting logic for all safety-critical functions."
            )
        ),
    ]
)

# Primary Loop System
primary_loop_system = System(
    name="Primary Cooling Loop",
    description=(
        f"A {PRIMARY_LOOP_PARAMS.coolant_type} cooling system operating at "
        f"{PRIMARY_LOOP_PARAMS.operating_pressure.magnitude}{PRIMARY_LOOP_PARAMS.operating_pressure.units} "
        f"with {PRIMARY_LOOP_PARAMS.primary_pump_count} redundant pumps."
    ),
    requirements=[
        Requirement(
            name="Heat Removal",
            description=(
                f"The primary loop shall remove {REACTOR_PARAMS.thermal_power.magnitude}"
                f"{REACTOR_PARAMS.thermal_power.units} of thermal power from the reactor core."
            )
        ),
        Requirement(
            name="Coolant Flow",
            description=(
                f"The primary loop shall maintain a coolant flow rate of "
                f"{PRIMARY_LOOP_PARAMS.coolant_flow_rate.magnitude}{PRIMARY_LOOP_PARAMS.coolant_flow_rate.units}."
            )
        ),
        Requirement(
            name="Temperature Control",
            description=(
                f"The primary loop shall maintain the reactor coolant outlet temperature at "
                f"{PRIMARY_LOOP_PARAMS.outlet_temperature.magnitude}{PRIMARY_LOOP_PARAMS.outlet_temperature.units} "
                f"during normal operation."
            )
        ),
        Requirement(
            name="Pressure Boundary",
            description=(
                f"The primary loop pressure boundary shall be designed to withstand "
                f"{PRIMARY_LOOP_PARAMS.operating_pressure.magnitude}{PRIMARY_LOOP_PARAMS.operating_pressure.units} "
                f"with appropriate safety margins."
            )
        ),
    ]
)

# Secondary Loop System
secondary_loop_system = System(
    name="Secondary Steam Loop",
    description=(
        f"A {SECONDARY_LOOP_PARAMS.working_fluid} power conversion system with a "
        f"{SECONDARY_LOOP_PARAMS.turbine_type} and electrical generator."
    ),
    requirements=[
        Requirement(
            name="Power Generation",
            description=(
                f"The secondary loop shall convert thermal energy to {REACTOR_PARAMS.electrical_power.magnitude}"
                f"{REACTOR_PARAMS.electrical_power.units} of electrical power."
            )
        ),
        Requirement(
            name="Steam Conditions",
            description=(
                f"The system shall produce steam at {SECONDARY_LOOP_PARAMS.steam_temperature.magnitude}"
                f"{SECONDARY_LOOP_PARAMS.steam_temperature.units} and "
                f"{SECONDARY_LOOP_PARAMS.steam_pressure.magnitude}{SECONDARY_LOOP_PARAMS.steam_pressure.units}."
            )
        ),
        Requirement(
            name="Efficiency",
            description=(
                f"The turbine shall operate with an efficiency of at least "
                f"{SECONDARY_LOOP_PARAMS.turbine_efficiency.magnitude}{SECONDARY_LOOP_PARAMS.turbine_efficiency.units}."
            )
        ),
        Requirement(
            name="Heat Rejection",
            description=(
                f"The condenser shall reject waste heat using {SECONDARY_LOOP_PARAMS.condenser_cooling_method} "
                f"with a capacity of {SECONDARY_LOOP_PARAMS.condenser_cooling_capacity.magnitude}"
                f"{SECONDARY_LOOP_PARAMS.condenser_cooling_capacity.units}."
            )
        ),
    ]
)

# Containment System
containment_system = System(
    name="Containment System",
    description=(
        f"A {CONTAINMENT_PARAMS.containment_type} containment structure with "
        f"{CONTAINMENT_PARAMS.wall_thickness.magnitude}{CONTAINMENT_PARAMS.wall_thickness.units} thick walls."
    ),
    requirements=[
        Requirement(
            name="Pressure Containment",
            description=(
                f"The containment shall withstand an internal pressure of "
                f"{CONTAINMENT_PARAMS.design_pressure.magnitude}{CONTAINMENT_PARAMS.design_pressure.units} "
                f"without exceeding the design leak rate."
            )
        ),
        Requirement(
            name="Leak Tightness",
            description=(
                f"The containment leak rate shall not exceed "
                f"{CONTAINMENT_PARAMS.leak_rate.magnitude}{CONTAINMENT_PARAMS.leak_rate.units} "
                f"at design pressure."
            )
        ),
        Requirement(
            name="Passive Cooling",
            description=(
                f"The containment shall incorporate passive cooling systems capable of removing "
                f"{CONTAINMENT_PARAMS.passive_cooling_capacity.magnitude}{CONTAINMENT_PARAMS.passive_cooling_capacity.units} "
                f"of decay heat without external power."
            )
        ),
        Requirement(
            name="External Events Protection",
            description=(
                "The containment shall protect the reactor from external events including "
                "aircraft impact, extreme weather, and seismic events."
            )
        ),
    ]
)

# Import seismic protection system
try:
    from reactor.systems_seismic import seismic_protection_system
    print("Successfully imported seismic protection system")
except ImportError:
    try:
        from .systems_seismic import seismic_protection_system
        print("Imported seismic protection system from relative path")
    except ImportError:
        print("ERROR: Could not import seismic_protection_system - creating a placeholder")
        from pyforge import System, Requirement
        # Create a placeholder seismic system
        seismic_protection_system = System(
            name="Seismic Protection System (Placeholder)",
            description="Placeholder for seismic protection system"
        )

# Import manufacturing analysis
try:
    from reactor.tools_manufacturing import analyze_manufacturability
    print("Successfully imported manufacturing analysis")
except ImportError:
    print("Note: Manufacturing analysis will be imported in design.py")

# Import I&C system
try:
    from reactor.systems_instrumentation import instrumentation_control_system
    print("Successfully imported instrumentation and control system")
except ImportError:
    try:
        from .systems_instrumentation import instrumentation_control_system
        print("Imported instrumentation and control system from relative path")
    except ImportError:
        print("ERROR: Could not import instrumentation_control_system - creating a placeholder")
        from pyforge import System
        # Create a placeholder I&C system
        instrumentation_control_system = System(
            name="Instrumentation and Control System (Placeholder)",
            description="Placeholder for instrumentation and control system"
        )

# Build the system hierarchy
reactor_core_system.add_child(control_system)
smr_system.add_child(reactor_core_system)
smr_system.add_child(primary_loop_system)
smr_system.add_child(secondary_loop_system)
smr_system.add_child(containment_system)
smr_system.add_child(seismic_protection_system)
smr_system.add_child(instrumentation_control_system)

# Initialize children attribute for all systems if not already present
for system in [smr_system, reactor_core_system, control_system, primary_loop_system, secondary_loop_system, containment_system]:
    if not hasattr(system, 'children') or system.children is None:
        system.children = []

# Print system structure for verification
print("SMR System Structure:")
print(f"- {smr_system.name}")
for system in smr_system.children:
    print(f"  - {system.name}")
    for subsystem in system.children if hasattr(system, 'children') and system.children is not None else []:
        print(f"    - {subsystem.name}")
