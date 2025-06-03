from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

# Print debug information
print("Loading thermal storage system definitions")

# Root "Thermal Energy Storage" system
thermal_storage_system = System(
    name="Thermal Energy Storage System",
    description=(
        f"{THERMAL_STORAGE_PARAMS.storage_capacity} thermal energy storage system "
        f"operating between {THERMAL_STORAGE_PARAMS.min_temperature} and "
        f"{THERMAL_STORAGE_PARAMS.max_temperature}"
    ),
    requirements=[
        # Performance Requirements
        Requirement(
            name="Storage Capacity",
            description=(
                f"Store at least {THERMAL_STORAGE_PARAMS.storage_capacity} of thermal energy"
            )
        ),
        Requirement(
            name="Power Output",
            description=(
                f"Deliver up to {THERMAL_STORAGE_PARAMS.max_power_output} of power"
            )
        ),
        Requirement(
            name="Design Life",
            description=(
                f"Operate for at least {THERMAL_STORAGE_PARAMS.design_life} years with "
                f"{THERMAL_STORAGE_PARAMS.cycles_per_year} cycles per year"
            )
        ),
        Requirement(
            name="Efficiency",
            description=(
                f"Maintain charge efficiency of {THERMAL_STORAGE_PARAMS.charge_efficiency} and "
                f"discharge efficiency of {THERMAL_STORAGE_PARAMS.discharge_efficiency}"
            )
        ),
    ]
)

# Subsystems
# 1. Thermal Storage Medium
thermal_storage_medium = System(
    name="Storage Medium",
    description="High-temperature thermal mass for energy storage",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Energy Density",
            description=f"Minimum energy density of {THERMAL_STORAGE_PARAMS.min_energy_density}"
        ),
        Requirement(
            name="Temperature Range",
            description=(
                f"Operate effectively between {THERMAL_STORAGE_PARAMS.min_temperature} and "
                f"{THERMAL_STORAGE_PARAMS.max_temperature}"
            )
        ),
    ]
)

# Storage Container
storage_container = System(
    name="Storage Container",
    description=f"Vessel containing the storage medium with {THERMAL_STORAGE_PARAMS.container_thickness} walls",
    parent=thermal_storage_medium,
    requirements=[
        Requirement(
            name="Thermal Stability",
            description=f"Maintain properties for {THERMAL_STORAGE_PARAMS.design_life} years"
        ),
    ]
)

# 2. Insulation System
insulation_system = System(
    name="Insulation System",
    description=f"Thermal insulation with {THERMAL_STORAGE_PARAMS.insulation_thickness} thickness",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Thermal Conductivity",
            description=f"Maximum thermal conductivity of {THERMAL_STORAGE_PARAMS.max_insulation_conductivity}"
        ),
        Requirement(
            name="Heat Loss",
            description=f"Limit heat loss to {THERMAL_STORAGE_PARAMS.max_heat_loss} per day"
        )
    ]
)

# 3. Heat Exchanger
heat_exchanger = System(
    name="Heat Exchanger",
    description="System for charging and discharging thermal energy",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Heat Transfer Rate",
            description=f"Transfer heat at {THERMAL_STORAGE_PARAMS.max_power_output} during discharge"
        ),
        Requirement(
            name="Pressure Drop",
            description=f"Maximum pressure drop of {THERMAL_STORAGE_PARAMS.max_pressure_drop}"
        ),
        Requirement(
            name="Efficiency",
            description=f"Heat transfer efficiency of at least {THERMAL_STORAGE_PARAMS.heat_exchanger_efficiency}"
        )
    ]
)

# Heat Transfer Fluid System
heat_transfer_fluid_system = System(
    name="Heat Transfer Fluid System",
    description="Fluid circulation system for heat transport",
    parent=heat_exchanger,
    requirements=[
        Requirement(
            name="Flow Rate",
            description=f"Maintain flow rate of {THERMAL_STORAGE_PARAMS.nominal_flow_rate}"
        ),
        Requirement(
            name="Temperature Rating",
            description=f"Operate with fluid temperatures up to {THERMAL_STORAGE_PARAMS.max_fluid_temperature}"
        )
    ]
)

# 4. Control System
control_system = System(
    name="Control System",
    description="Monitoring and control of thermal storage operation",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Response Time",
            description=f"Control system response time under {THERMAL_STORAGE_PARAMS.max_control_response_time}"
        ),
        Requirement(
            name="Data Logging",
            description=f"Log data at {THERMAL_STORAGE_PARAMS.data_logging_frequency} frequency"
        )
    ]
)

# Monitoring System
monitoring_system = System(
    name="Monitoring System",
    description="Sensors and data acquisition for system state monitoring",
    parent=control_system,
    requirements=[
        Requirement(
            name="Temperature Sensors",
            description=f"Temperature measurement accuracy of ±{THERMAL_STORAGE_PARAMS.temperature_accuracy}"
        ),
        Requirement(
            name="Pressure Sensors",
            description=f"Pressure measurement accuracy of ±{THERMAL_STORAGE_PARAMS.pressure_accuracy}"
        ),
        Requirement(
            name="Flow Sensors",
            description=f"Flow measurement accuracy of ±{THERMAL_STORAGE_PARAMS.flow_accuracy}"
        )
    ]
)

# 5. Power Conversion System
power_conversion_system = System(
    name="Power Conversion System",
    description="System for converting thermal energy to electricity",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Conversion Efficiency",
            description=f"Achieve thermal-to-electric conversion efficiency of {THERMAL_STORAGE_PARAMS.power_conversion_efficiency}"
        ),
        Requirement(
            name="Power Quality",
            description=f"Meet grid standards for frequency stability (±{THERMAL_STORAGE_PARAMS.frequency_tolerance}) and voltage regulation"
        ),
        Requirement(
            name="Ramp Rate",
            description=f"Ramp power output at {THERMAL_STORAGE_PARAMS.ramp_rate} of rated capacity per minute"
        )
    ]
)

# 6. Heat Distribution System
heat_distribution_system = System(
    name="Heat Distribution System",
    description="System for delivering heat to industrial processes",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Temperature Control",
            description=f"Maintain output temperature within ±{THERMAL_STORAGE_PARAMS.temperature_control_tolerance} of setpoint"
        ),
        Requirement(
            name="Distribution Losses",
            description=f"Limit heat losses to {THERMAL_STORAGE_PARAMS.max_distribution_losses} during transport"
        )
    ]
)

# Print system hierarchy for verification
print("Thermal Energy Storage System Architecture:")
print(thermal_storage_system.display())
print("DESIGN_COMPLETE")
