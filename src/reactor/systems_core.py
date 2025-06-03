"""
Core subsystem definition for the High-Temperature Gas-cooled Reactor (HTGR).

This module defines the hierarchical structure of the reactor core subsystem
using the pyforge.System class, including all major components and their
requirements.
"""

from pyforge import System, Requirement
from reactor.parameters_core import CORE_PARAMS

# Root "Core" system
core_system = System(
    name="Reactor Core System",
    description=(
        f"HTGR core system operating at {CORE_PARAMS.core_outlet_temp} "
        f"with {CORE_PARAMS.thermal_power} thermal output"
    ),
    requirements=[
        Requirement(
            name="Thermal Power Output",
            description=(
                f"Generate {CORE_PARAMS.thermal_power} of thermal power "
                f"continuously during normal operation."
            )
        ),
        Requirement(
            name="Core Temperature",
            description=(
                f"Maintain core outlet temperature of {CORE_PARAMS.core_outlet_temp} "
                f"during normal operation."
            )
        ),
        Requirement(
            name="Core Lifetime",
            description=(
                f"Operate for {CORE_PARAMS.core_lifetime} with minimal "
                f"refueling requirements."
            )
        ),
        Requirement(
            name="Passive Safety",
            description=(
                "Maintain passive decay heat removal capability under all "
                "design basis accident conditions."
            )
        )
    ]
)

# TRISO fuel elements subsystem
triso_fuel_system = System(
    name="TRISO Fuel Elements System",
    description=(
        f"TRISO fuel particles embedded in graphite matrix, "
        f"enriched to {CORE_PARAMS.fuel_enrichment}"
    ),
    requirements=[
        Requirement(
            name="Fuel Integrity",
            description=(
                "Maintain integrity of TRISO particles up to "
                f"1600 degC during accident conditions."
            )
        ),
        Requirement(
            name="Fission Product Retention",
            description=(
                "Retain >99.9% of fission products within TRISO particles "
                "during normal operation and accident conditions."
            )
        ),
        Requirement(
            name="Power Density",
            description=(
                f"Achieve average power density of {CORE_PARAMS.power_density} "
                f"in the active core region."
            )
        )
    ],
    parent=core_system
)

# Graphite moderator subsystem
graphite_moderator_system = System(
    name="Graphite Moderator System",
    description=(
        "Nuclear-grade graphite structures providing neutron moderation "
        "and structural support"
    ),
    requirements=[
        Requirement(
            name="Neutron Moderation",
            description=(
                "Provide sufficient neutron moderation to achieve "
                "designed neutron spectrum and reactivity."
            )
        ),
        Requirement(
            name="Thermal Stability",
            description=(
                f"Maintain structural integrity at temperatures up to "
                f"{CORE_PARAMS.max_graphite_temp} during normal operation."
            )
        ),
        Requirement(
            name="Radiation Resistance",
            description=(
                f"Withstand neutron fluence of {CORE_PARAMS.max_neutron_fluence} "
                f"over the core lifetime."
            )
        )
    ],
    parent=core_system
)

# Control rod system
control_rod_system = System(
    name="Control Rod System",
    description=(
        f"{CORE_PARAMS.control_rod_count} control rods with "
        f"{CORE_PARAMS.control_rod_material} absorber material"
    ),
    requirements=[
        Requirement(
            name="Reactivity Control",
            description=(
                f"Provide total reactivity worth of {CORE_PARAMS.total_rod_worth} "
                f"for reactor control and shutdown."
            )
        ),
        Requirement(
            name="Shutdown Margin",
            description=(
                f"Maintain shutdown margin of at least {CORE_PARAMS.shutdown_margin} "
                f"under all operating conditions."
            )
        ),
        Requirement(
            name="Insertion Time",
            description=(
                f"Complete full insertion within {CORE_PARAMS.rod_insertion_time} "
                f"under all design basis conditions."
            )
        )
    ],
    parent=core_system
)

# Neutron reflector system
neutron_reflector_system = System(
    name="Neutron Reflector System",
    description=(
        f"{CORE_PARAMS.reflector_material} reflector with "
        f"{CORE_PARAMS.reflector_thickness} thickness"
    ),
    requirements=[
        Requirement(
            name="Neutron Economy",
            description=(
                "Reduce neutron leakage to improve fuel utilization and "
                "flatten power distribution."
            )
        ),
        Requirement(
            name="Radiation Shielding",
            description=(
                "Provide initial neutron shielding to reduce activation "
                "of surrounding structures."
            )
        ),
        Requirement(
            name="Thermal Stability",
            description=(
                f"Maintain structural integrity at temperatures up to "
                f"{CORE_PARAMS.max_reflector_temp}."
            )
        )
    ],
    parent=core_system
)

# Core support structure
core_support_system = System(
    name="Core Support Structure",
    description=(
        f"Metallic and ceramic structures supporting the core components "
        f"made of {CORE_PARAMS.support_structure_material}"
    ),
    requirements=[
        Requirement(
            name="Structural Integrity",
            description=(
                "Support the weight of all core components under normal "
                "and seismic loading conditions."
            )
        ),
        Requirement(
            name="Thermal Expansion",
            description=(
                "Accommodate thermal expansion of core components during "
                "startup, operation, and shutdown."
            )
        ),
        Requirement(
            name="Radiation Resistance",
            description=(
                "Maintain structural properties under radiation exposure "
                f"for the full {CORE_PARAMS.core_lifetime}."
            )
        )
    ],
    parent=core_system
)

# Core instrumentation system
core_instrumentation_system = System(
    name="Core Instrumentation System",
    description=(
        "Temperature, neutron flux, and pressure sensors for core monitoring"
    ),
    requirements=[
        Requirement(
            name="Temperature Monitoring",
            description=(
                f"Monitor core temperatures from {CORE_PARAMS.min_operating_temp} "
                f"to {CORE_PARAMS.max_operating_temp} with accuracy of "
                f"{CORE_PARAMS.temp_measurement_accuracy}."
            )
        ),
        Requirement(
            name="Neutron Flux Monitoring",
            description=(
                "Monitor neutron flux across all operating ranges from "
                "startup to full power operation."
            )
        ),
        Requirement(
            name="Reliability",
            description=(
                f"Maintain instrumentation reliability for {CORE_PARAMS.instrument_lifetime} "
                f"in high temperature and radiation environment."
            )
        )
    ],
    parent=core_system
)

# Print statement to show the core system hierarchy
print("Core system hierarchy defined with all subsystems and requirements")
print(f"Core thermal power: {CORE_PARAMS.thermal_power}")
print(f"Core outlet temperature: {CORE_PARAMS.core_outlet_temp}")
