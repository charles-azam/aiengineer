"""
Instrumentation and Control systems for the small modular reactor.
"""
from pyforge import System, Requirement
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
from reactor.systems_reactor import safety_systems

# Main I&C System
instrumentation_control = System(
    name="Instrumentation and Control Systems",
    description=(
        f"Digital and analog control systems with triple redundancy, "
        f"supplied by Framatome using TELEPERM XS platform with diverse backup systems"
    ),
    requirements=[
        Requirement(
            name="Control Reliability",
            description=(
                f"99.999% availability with no single point of failure."
            )
        ),
        Requirement(
            name="Cybersecurity",
            description=(
                f"Meet NEI 08-09 Rev. 6 cybersecurity requirements with air-gapped safety systems."
            )
        )
    ],
    parent=safety_systems
)

# Reactor Protection System
reactor_protection = System(
    name="Reactor Protection System",
    description=(
        f"Triple redundant safety-grade protection system by Framatome, "
        f"using FPGA-based logic with 2-out-of-3 voting logic, "
        f"manufactured with IEC 61508 SIL-4 certification process"
    ),
    requirements=[
        Requirement(
            name="Response Time",
            description=(
                f"Detect and initiate SCRAM within 100 ms of trip condition."
            )
        ),
        Requirement(
            name="Failure Rate",
            description=(
                f"Less than 1×10⁻⁷ failures per demand with diagnostic coverage >95%."
            )
        )
    ],
    parent=instrumentation_control
)

# Neutron Monitoring System
neutron_monitoring = System(
    name="Neutron Monitoring System",
    description=(
        f"Wide-range neutron flux monitoring by Mirion Technologies, "
        f"using fission chambers with 10B coating, "
        f"covering 10⁻⁸ to 150% rated power"
    ),
    requirements=[
        Requirement(
            name="Measurement Range",
            description=(
                f"Monitor neutron flux from shutdown to 150% of rated power with ±2% accuracy."
            )
        ),
        Requirement(
            name="Response Time",
            description=(
                f"<500 ms response time for rapid transient detection."
            )
        )
    ],
    parent=instrumentation_control
)

# Process Monitoring System
process_monitoring = System(
    name="Process Monitoring System",
    description=(
        f"Comprehensive monitoring of temperatures, pressures, flows, and levels "
        f"by Emerson Process Management using Rosemount sensors and transmitters, "
        f"with HART protocol communication"
    ),
    requirements=[
        Requirement(
            name="Temperature Monitoring",
            description=(
                f"Monitor primary coolant temperatures with ±0.5°C accuracy from 0-400°C."
            )
        ),
        Requirement(
            name="Pressure Monitoring",
            description=(
                f"Monitor primary system pressure with ±0.1% accuracy from 0-20 MPa."
            )
        )
    ],
    parent=instrumentation_control
)

# Control Room
control_room = System(
    name="Main Control Room",
    description=(
        f"Digital control room by Westinghouse, using Advanced Logic System platform, "
        f"with large display panels and operator workstations, "
        f"manufactured with human factors engineering principles per NUREG-0711"
    ),
    requirements=[
        Requirement(
            name="Habitability",
            description=(
                f"Maintain habitability during all design basis accidents with independent HVAC."
            )
        ),
        Requirement(
            name="Human Factors",
            description=(
                f"Comply with NUREG-0700 Rev. 3 human-system interface guidelines."
            )
        )
    ],
    parent=instrumentation_control
)

# Remote Shutdown Panel
remote_shutdown = System(
    name="Remote Shutdown Panel",
    description=(
        f"Backup control capability by Westinghouse, using hardwired controls and indicators, "
        f"located in separate fire area from main control room"
    ),
    requirements=[
        Requirement(
            name="Functionality",
            description=(
                f"Provide capability to achieve and maintain safe shutdown independent of main control room."
            )
        ),
        Requirement(
            name="Accessibility",
            description=(
                f"Accessible within 10 minutes from main control room under emergency conditions."
            )
        )
    ],
    parent=instrumentation_control
)

print(f"Instrumentation and Control systems defined with {len(instrumentation_control.children)} subsystems")
