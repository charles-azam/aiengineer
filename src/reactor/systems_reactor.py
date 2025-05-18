from pyforge import System, Requirement
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS

# Root "Reactor" system
reactor_system = System(
    name="Small Modular Reactor System",
    description=(
        f"{REACTOR_PARAMS.electrical_power} electrical output modular reactor "
        f"with {REACTOR_PARAMS.design_life} year design life"
    ),
    requirements=[
        Requirement(
            name="Power Output",
            description=(
                f"Deliver {REACTOR_PARAMS.electrical_power} electrical power "
                f"with {REACTOR_PARAMS.efficiency*100:.1f}% thermal efficiency."
            )
        ),
        Requirement(
            name="Design Life",
            description=(
                f"Minimum operational lifetime of {REACTOR_PARAMS.design_life} years "
                f"with refueling every {REACTOR_PARAMS.refueling_interval} years."
            )
        ),
        Requirement(
            name="Safety Rating",
            description=(
                f"Meet or exceed IAEA safety standards with {SAFETY_PARAMS.safety_train_redundancy}-train "
                f"redundancy for all safety systems."
            )
        ),
        Requirement(
            name="Manufacturability",
            description=(
                f"Design for factory fabrication with modular components transportable by standard shipping methods."
            )
        ),
        Requirement(
            name="Licensing",
            description=(
                f"Comply with regulatory requirements for simplified licensing process based on standardized design."
            )
        )
    ]
)

# Initialize children attribute
reactor_system.children = []

# Reactor Core subsystem
reactor_core = System(
    name="Reactor Core",
    description=(
        f"{REACTOR_PARAMS.thermal_power} thermal output core with "
        f"{REACTOR_PARAMS.fuel_assemblies} {REACTOR_PARAMS.fuel_type} fuel assemblies "
        f"at {REACTOR_PARAMS.enrichment}% enrichment"
    ),
    requirements=[
        Requirement(
            name="Power Density",
            description=(
                f"Maintain average power density below 100 MW/m³ for thermal margin."
            )
        ),
        Requirement(
            name="Reactivity Control",
            description=(
                f"Provide sufficient negative reactivity with {REACTOR_PARAMS.control_rods} "
                f"control rod assemblies for safe shutdown under all conditions."
            )
        ),
        Requirement(
            name="Fuel Performance",
            description=(
                f"Achieve minimum average burnup of 45 GWd/tU with less than 1% fuel failure rate."
            )
        )
    ],
    parent=reactor_system
)

# Initialize children attribute
reactor_core.children = []

# Primary Loop subsystem
primary_loop = System(
    name="Primary Cooling Loop",
    description=(
        f"Pressurized {THERMAL_PARAMS.primary_coolant} cooling system operating at "
        f"{THERMAL_PARAMS.primary_pressure} with {THERMAL_PARAMS.primary_flow_rate} flow rate"
    ),
    requirements=[
        Requirement(
            name="Heat Removal",
            description=(
                f"Remove {REACTOR_PARAMS.thermal_power} of thermal energy from the core "
                f"with temperature rise from {THERMAL_PARAMS.primary_temp_cold} to "
                f"{THERMAL_PARAMS.primary_temp_hot}."
            )
        ),
        Requirement(
            name="Pressure Boundary",
            description=(
                f"Maintain pressure boundary integrity at {THERMAL_PARAMS.primary_pressure} "
                f"under all normal and accident conditions."
            )
        ),
        Requirement(
            name="Natural Circulation",
            description=(
                f"Support natural circulation cooling at minimum 10% of rated power during loss of forced flow events."
            )
        )
    ],
    parent=reactor_system
)

# Initialize children attribute
primary_loop.children = []

# Secondary Loop subsystem
secondary_loop = System(
    name="Secondary Loop and Power Conversion",
    description=(
        f"Steam generation and power conversion system with "
        f"{THERMAL_PARAMS.turbine_type} operating at {THERMAL_PARAMS.turbine_efficiency*100:.1f}% efficiency"
    ),
    requirements=[
        Requirement(
            name="Power Generation",
            description=(
                f"Convert thermal energy to {REACTOR_PARAMS.electrical_power} electrical output "
                f"using {THERMAL_PARAMS.turbine_type}."
            )
        ),
        Requirement(
            name="Thermal Efficiency",
            description=(
                f"Achieve minimum {REACTOR_PARAMS.efficiency*100:.1f}% thermal-to-electrical conversion efficiency."
            )
        ),
        Requirement(
            name="Load Following",
            description=(
                f"Support load following operation between 50-100% power with ramp rate of 5% per minute."
            )
        )
    ],
    parent=reactor_system
)

# Initialize children attribute
secondary_loop.children = []

# Safety Systems
safety_systems = System(
    name="Safety Systems",
    description=(
        f"{SAFETY_PARAMS.containment_type} containment with {SAFETY_PARAMS.eccs_type} "
        f"and {SAFETY_PARAMS.safety_train_redundancy}-train redundancy"
    ),
    requirements=[
        Requirement(
            name="Containment Integrity",
            description=(
                f"Maintain containment integrity under design basis accidents with "
                f"{SAFETY_PARAMS.containment_design_pressure} internal pressure."
            )
        ),
        Requirement(
            name="Passive Safety",
            description=(
                f"Provide {SAFETY_PARAMS.passive_cooling_duration} of passive cooling "
                f"at {SAFETY_PARAMS.passive_cooling_capacity} capacity without external power."
            )
        ),
        Requirement(
            name="Radiation Protection",
            description=(
                f"Limit worker exposure to below {SAFETY_PARAMS.max_worker_dose} "
                f"using {SAFETY_PARAMS.radiation_shield_material} shielding."
            )
        ),
        Requirement(
            name="Severe Accident Mitigation",
            description=(
                f"Include features to mitigate beyond-design-basis accidents including core damage scenarios."
            )
        )
    ],
    parent=reactor_system
)

# Initialize children attribute
safety_systems.children = []

# Auxiliary Systems
auxiliary_systems = System(
    name="Auxiliary Systems",
    description=(
        f"Support systems including cooling water, HVAC, electrical distribution, "
        f"and waste management systems"
    ),
    requirements=[
        Requirement(
            name="Reliability",
            description=(
                f"Provide 99.9% availability for all support functions required for normal operation."
            )
        ),
        Requirement(
            name="Independence",
            description=(
                f"Maintain separation between safety and non-safety systems to prevent common cause failures."
            )
        )
    ],
    parent=reactor_system
)

# Initialize children attribute
auxiliary_systems.children = []

# Add all major subsystems to reactor_system.children
reactor_system.children = [reactor_core, primary_loop, secondary_loop, safety_systems, auxiliary_systems]

# Define a function to recursively count all components in the system hierarchy
def count_all_components(system):
    """Count all components in the system hierarchy recursively."""
    if not hasattr(system, 'children') or system.children is None:
        return 1
    
    # Count this system plus all its children
    return 1 + sum(count_all_components(child) for child in system.children)

# Print system hierarchy information
print(f"Systems hierarchy created with {len(reactor_system.children)} major subsystems")
print(f"Debug: reactor_system.children contains: {[child.name for child in reactor_system.children]}")
print(f"Total component count: {count_all_components(reactor_system)}")
