"""
Seismic protection systems for the Small Modular Reactor.
Defines the seismic isolation and qualification systems.
"""

from pyforge import System, Requirement
from reactor.parameters_reactor import CONTAINMENT_PARAMS
from pyforge import Quantity  # Add missing import for Quantity

# Seismic Protection System
seismic_protection_system = System(
    name="Seismic Protection System",
    description=(
        "Seismic protection system to ensure structural integrity and equipment functionality "
        "during and after seismic events."
    ),
    requirements=[
        Requirement(
            name="Design Basis Earthquake",
            description=(
                "The reactor shall withstand a design basis earthquake with peak ground "
                "acceleration of 0.3g without loss of safety functions."
            )
        ),
        Requirement(
            name="Seismic Margin",
            description=(
                "The seismic design shall provide a margin of at least 1.5 times the design "
                "basis earthquake for all safety-critical systems."
            )
        ),
        Requirement(
            name="Equipment Qualification",
            description=(
                "All safety-related equipment shall be seismically qualified to withstand "
                "the applicable floor response spectra with a margin of at least 1.5."
            )
        ),
    ]
)

# Foundation System
foundation_system = System(
    name="Foundation System",
    description=(
        f"A {getattr(CONTAINMENT_PARAMS, 'foundation_width', Quantity(22, 'm')).magnitude}m x {getattr(CONTAINMENT_PARAMS, 'foundation_width', Quantity(22, 'm')).magnitude}m "
        f"reinforced concrete foundation with {getattr(CONTAINMENT_PARAMS, 'foundation_depth', Quantity(3, 'm')).magnitude}m depth."
    ),
    requirements=[
        Requirement(
            name="Soil Bearing Capacity",
            description=(
                "The foundation shall distribute structural loads to maintain soil bearing "
                "pressure below allowable limits with a safety factor of at least 3.0."
            )
        ),
        Requirement(
            name="Settlement Control",
            description=(
                "The foundation shall limit differential settlement to less than 1/750 of the "
                "span between any two points."
            )
        ),
    ]
)

# Seismic Isolation System
seismic_isolation_system = System(
    name="Seismic Isolation System",
    description=(
        "Advanced triple-pendulum bearing isolation system for critical equipment to reduce seismic accelerations."
    ),
    requirements=[
        Requirement(
            name="Acceleration Reduction",
            description=(
                "The isolation system shall reduce peak accelerations by at least 60% for "
                "frequencies above 5 Hz."
            )
        ),
        Requirement(
            name="Equipment Protection",
            description=(
                "The isolation system shall be installed for the reactor pressure vessel, "
                "control rod drive mechanisms, and main coolant pumps."
            )
        ),
        Requirement(
            name="Supplier Qualification",
            description=(
                "The isolation system shall be supplied by Earthquake Protection Systems, Inc. "
                "or equivalent qualified manufacturer with nuclear-grade certification."
            )
        ),
    ]
)

# Add children to seismic protection system
seismic_protection_system.add_child(foundation_system)
seismic_protection_system.add_child(seismic_isolation_system)

# Print system structure for verification
print("\n=== SEISMIC PROTECTION SYSTEM STRUCTURE ===")
print(f"- {seismic_protection_system.name}")
for system in seismic_protection_system.children:
    print(f"  - {system.name}")
