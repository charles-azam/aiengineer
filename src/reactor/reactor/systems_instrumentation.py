"""
Instrumentation and Control Systems for the Small Modular Reactor.
Defines the I&C architecture, safety systems, and human-machine interface.
"""

from pyforge import System, Requirement
from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS

# Main I&C System
instrumentation_control_system = System(
    name="Instrumentation and Control System",
    description=(
        "Digital and analog instrumentation and control systems for monitoring and "
        "controlling all aspects of reactor operation."
    ),
    requirements=[
        Requirement(
            name="Safety Classification",
            description=(
                "The I&C system shall be classified into safety-critical, safety-related, "
                "and non-safety categories in accordance with IEC 61513."
            )
        ),
        Requirement(
            name="Defense in Depth",
            description=(
                "The I&C architecture shall implement defense-in-depth with multiple "
                "independent layers of protection."
            )
        ),
        Requirement(
            name="Cyber Security",
            description=(
                "The digital I&C systems shall be protected against cyber threats in "
                "accordance with IEC 62645 and regulatory requirements."
            )
        ),
    ]
)

# Reactor Protection System
reactor_protection_system = System(
    name="Reactor Protection System",
    description=(
        "Safety-critical system that monitors key parameters and automatically initiates "
        "reactor trip when safety limits are approached."
    ),
    requirements=[
        Requirement(
            name="Independence",
            description=(
                "The RPS shall be physically and functionally independent from control systems "
                "to prevent common cause failures."
            )
        ),
        Requirement(
            name="Redundancy",
            description=(
                "The RPS shall implement quadruple redundancy (4 divisions) with 2-out-of-4 "
                "voting logic for trip actuation."
            )
        ),
        Requirement(
            name="Response Time",
            description=(
                "The RPS shall detect unsafe conditions and initiate protective actions "
                "within 100 milliseconds."
            )
        ),
        Requirement(
            name="Equipment Qualification",
            description=(
                "All RPS components shall be qualified for the environmental conditions "
                "they will experience during normal operation and accident conditions."
            )
        ),
    ]
)

# Engineered Safety Features Actuation System
esfas_system = System(
    name="Engineered Safety Features Actuation System",
    description=(
        "System that actuates engineered safety features such as emergency core cooling "
        "and containment isolation in response to accident conditions."
    ),
    requirements=[
        Requirement(
            name="Automatic Actuation",
            description=(
                "The ESFAS shall automatically actuate engineered safety features when "
                "monitored parameters exceed safety limits."
            )
        ),
        Requirement(
            name="Manual Actuation",
            description=(
                "The ESFAS shall provide means for operators to manually actuate "
                "engineered safety features from the main control room."
            )
        ),
        Requirement(
            name="Testability",
            description=(
                "The ESFAS shall be designed to allow periodic testing of all functions "
                "without compromising plant safety."
            )
        ),
    ]
)

# Plant Control System
plant_control_system = System(
    name="Plant Control System",
    description=(
        "Non-safety system that controls normal plant operations including reactor power, "
        "primary loop temperature, and steam generator level."
    ),
    requirements=[
        Requirement(
            name="Power Control",
            description=(
                "The system shall control reactor power between 5% and 100% of rated power "
                "with a stability of ±0.5%."
            )
        ),
        Requirement(
            name="Temperature Control",
            description=(
                f"The system shall maintain primary coolant average temperature within "
                f"±2°C of the setpoint across the power range."
            )
        ),
        Requirement(
            name="Load Following",
            description=(
                "The system shall support load following operation with power change rates "
                "of up to 5% per minute between 20% and 100% power."
            )
        ),
    ]
)

# Human-Machine Interface
hmi_system = System(
    name="Human-Machine Interface",
    description=(
        "Control room interfaces, displays, and operator workstations for monitoring "
        "and controlling the plant."
    ),
    requirements=[
        Requirement(
            name="Main Control Room",
            description=(
                "The main control room shall provide all necessary controls and displays "
                "for normal operation, abnormal operation, and accident management."
            )
        ),
        Requirement(
            name="Remote Shutdown Station",
            description=(
                "A remote shutdown station shall be provided to achieve and maintain safe "
                "shutdown if the main control room becomes uninhabitable."
            )
        ),
        Requirement(
            name="Human Factors",
            description=(
                "The HMI shall be designed in accordance with human factors engineering "
                "principles to minimize operator error."
            )
        ),
    ]
)

# Monitoring Systems
monitoring_systems = System(
    name="Monitoring Systems",
    description=(
        "Systems for monitoring reactor parameters, radiation levels, and equipment status."
    ),
    requirements=[
        Requirement(
            name="Neutron Monitoring",
            description=(
                "The system shall monitor neutron flux across the full range from shutdown "
                "to 125% of rated power with an accuracy of ±2%."
            )
        ),
        Requirement(
            name="Radiation Monitoring",
            description=(
                "The system shall monitor radiation levels in all plant areas and effluent "
                "paths with detection ranges covering normal and accident conditions."
            )
        ),
        Requirement(
            name="Equipment Condition Monitoring",
            description=(
                "The system shall monitor the condition of critical equipment including "
                "vibration, temperature, and electrical parameters."
            )
        ),
    ]
)

# Add children to I&C system
instrumentation_control_system.add_child(reactor_protection_system)
instrumentation_control_system.add_child(esfas_system)
instrumentation_control_system.add_child(plant_control_system)
instrumentation_control_system.add_child(hmi_system)
instrumentation_control_system.add_child(monitoring_systems)

# Print system structure for verification
print("\n=== INSTRUMENTATION AND CONTROL SYSTEM STRUCTURE ===")
print(f"- {instrumentation_control_system.name}")
for system in instrumentation_control_system.children:
    print(f"  - {system.name}")

# Provide implementation details
print("\n=== I&C IMPLEMENTATION DETAILS ===")
print("Reactor Protection System:")
print("  - Platform: Rolls-Royce Spinline 3 (Class 1E qualified)")
print("  - Architecture: 4 independent divisions with 2-out-of-4 voting")
print("  - Manufacturing: Factory assembled and tested cabinets with field connections")
print("  - Key Suppliers: Rolls-Royce, Lockheed Martin")

print("\nPlant Control System:")
print("  - Platform: Emerson Ovation DCS")
print("  - Architecture: Redundant controllers and networks")
print("  - Manufacturing: Factory assembled control cabinets with on-site integration")
print("  - Key Suppliers: Emerson, Westinghouse")

print("\nHuman-Machine Interface:")
print("  - Main Control Room: Digital displays with soft controls and minimal hardwired backups")
print("  - Technology: Large overview displays with operator workstations")
print("  - Manufacturing: Factory assembled operator consoles with on-site integration")
print("  - Key Suppliers: Westinghouse, General Electric")
