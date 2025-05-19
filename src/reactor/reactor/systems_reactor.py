"""
System definitions for the Small Modular Reactor (SMR).
"""
from pyforge import System, Requirement
from .parameters_reactor import REACTOR_PARAMS
print("Loaded systems_reactor module")

# Root "SMR" system
smr_system = System(
    name="Small Modular Reactor System",
    description=(
        f"{REACTOR_PARAMS.electrical_power} electrical output SMR with "
        f"{REACTOR_PARAMS.thermal_efficiency*100:.1f}% thermal efficiency and "
        f"{REACTOR_PARAMS.design_life} year design life"
    ),
    requirements=[
        Requirement(
            name="Power Output",
            description=(
                f"Deliver {REACTOR_PARAMS.electrical_power} electrical power "
                f"with {REACTOR_PARAMS.availability_factor*100:.1f}% availability."
            )
        ),
        Requirement(
            name="Safety",
            description=(
                "Meet all regulatory requirements for nuclear safety with passive "
                "safety systems capable of maintaining safe shutdown without external power."
            )
        ),
        Requirement(
            name="Operational Lifetime",
            description=(
                f"Minimum operational lifetime of {REACTOR_PARAMS.design_life} years "
                f"with refueling every {REACTOR_PARAMS.refueling_interval} months."
            )
        ),
        Requirement(
            name="Manufacturability",
            description=(
                "Design must be modular for factory fabrication and transportable "
                "by standard shipping methods to reduce on-site construction time."
            )
        )
    ]
)

# Reactor Core subsystem
reactor_core = System(
    name="Reactor Core",
    description=(
        f"{REACTOR_PARAMS.thermal_power} thermal output core using "
        f"{REACTOR_PARAMS.fuel_type} fuel enriched to {REACTOR_PARAMS.enrichment}% U-235"
    ),
    requirements=[
        Requirement(
            name="Thermal Output",
            description=(
                f"Generate {REACTOR_PARAMS.thermal_power} thermal power under "
                f"normal operating conditions."
            )
        ),
        Requirement(
            name="Core Geometry",
            description=(
                f"Core dimensions: {REACTOR_PARAMS.core_height} height, "
                f"{REACTOR_PARAMS.core_diameter} diameter with "
                f"{REACTOR_PARAMS.fuel_assemblies} fuel assemblies."
            )
        ),
        Requirement(
            name="Fuel Specification",
            description=(
                f"{REACTOR_PARAMS.fuel_type} fuel with {REACTOR_PARAMS.enrichment}% "
                f"U-235 enrichment, designed for {REACTOR_PARAMS.refueling_interval} "
                f"month cycle length."
            )
        )
    ],
    parent=smr_system
)

# Primary Loop subsystem
primary_loop = System(
    name="Primary Coolant Loop",
    description=(
        f"Pressurized water primary loop operating at {REACTOR_PARAMS.primary_pressure} "
        f"with temperatures from {REACTOR_PARAMS.primary_temp_inlet} to "
        f"{REACTOR_PARAMS.primary_temp_outlet}"
    ),
    requirements=[
        Requirement(
            name="Heat Transfer",
            description=(
                f"Transfer {REACTOR_PARAMS.thermal_power} from the reactor core "
                f"to the steam generators."
            )
        ),
        Requirement(
            name="Operating Conditions",
            description=(
                f"Maintain pressure of {REACTOR_PARAMS.primary_pressure} and flow rate "
                f"of {REACTOR_PARAMS.primary_flow_rate}."
            )
        ),
        Requirement(
            name="Safety Systems",
            description=(
                "Include passive safety systems for decay heat removal and "
                "emergency core cooling without external power."
            )
        )
    ],
    parent=smr_system
)

# Secondary Loop subsystem
secondary_loop = System(
    name="Secondary Loop",
    description=(
        f"Power conversion system generating {REACTOR_PARAMS.electrical_power} "
        f"with {REACTOR_PARAMS.thermal_efficiency*100:.1f}% efficiency"
    ),
    requirements=[
        Requirement(
            name="Power Generation",
            description=(
                f"Convert thermal energy to {REACTOR_PARAMS.electrical_power} "
                f"electrical output."
            )
        ),
        Requirement(
            name="Steam Conditions",
            description=(
                f"Operate with steam at {REACTOR_PARAMS.secondary_pressure} and "
                f"temperatures from {REACTOR_PARAMS.secondary_temp_inlet} to "
                f"{REACTOR_PARAMS.secondary_temp_outlet}."
            )
        ),
        Requirement(
            name="Efficiency",
            description=(
                f"Achieve minimum {REACTOR_PARAMS.thermal_efficiency*100:.1f}% "
                f"thermal-to-electrical conversion efficiency."
            )
        )
    ],
    parent=smr_system
)

# Containment subsystem
containment = System(
    name="Containment Structure",
    description=(
        f"Compact containment structure {REACTOR_PARAMS.containment_height} high "
        f"and {REACTOR_PARAMS.containment_diameter} in diameter"
    ),
    requirements=[
        Requirement(
            name="Protection",
            description=(
                "Provide protection against internal pressurization events and "
                "external hazards including aircraft impact and natural disasters."
            )
        ),
        Requirement(
            name="Dimensions",
            description=(
                f"Maximum dimensions: {REACTOR_PARAMS.containment_height} height, "
                f"{REACTOR_PARAMS.containment_diameter} diameter for transportability."
            )
        ),
        Requirement(
            name="Modular Construction",
            description=(
                "Design for factory fabrication with minimal on-site assembly."
            )
        )
    ],
    parent=smr_system
)
