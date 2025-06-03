"""
System definitions for thermal energy storage systems.
"""
from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS
from epyr.parameters_materials import (
    MOLTEN_SALT,
    SOLID_CERAMIC,
    HIGH_TEMP_CERAMIC,
    MOLTEN_METAL,
    PHASE_CHANGE_MATERIAL
)

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
            name="Temperature Range",
            description=(
                f"Operate between {THERMAL_STORAGE_PARAMS.min_temperature} and "
                f"{THERMAL_STORAGE_PARAMS.max_temperature}"
            )
        ),
        Requirement(
            name="Efficiency",
            description=(
                f"Maintain round-trip efficiency of at least "
                f"{THERMAL_STORAGE_PARAMS.charge_efficiency * THERMAL_STORAGE_PARAMS.discharge_efficiency * 100:.1f}%"
            )
        ),
        
        # Safety Requirements
        Requirement(
            name="Maximum Temperature",
            description=(
                f"Never exceed {THERMAL_STORAGE_PARAMS.max_safe_temperature} under any operating condition"
            )
        ),
        Requirement(
            name="Pressure Safety",
            description=(
                f"Maintain pressure below {THERMAL_STORAGE_PARAMS.max_pressure}"
            )
        ),
        
        # Economic Requirements
        Requirement(
            name="Capital Cost",
            description=(
                f"Capital cost below {THERMAL_STORAGE_PARAMS.max_capital_cost} per kWh of storage"
            )
        ),
        
        # Lifetime Requirements
        Requirement(
            name="Design Life",
            description=(
                f"Operate for at least {THERMAL_STORAGE_PARAMS.design_life} years"
            )
        )
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
            description=f"Provide energy density of at least {THERMAL_STORAGE_PARAMS.energy_density}"
        ),
        Requirement(
            name="Thermal Stability",
            description=f"Maintain properties for {THERMAL_STORAGE_PARAMS.design_life} years"
        )
    ]
)

# 2. Containment System
containment_system = System(
    name="Containment System",
    description="Vessel and insulation for the storage medium",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Thermal Insulation",
            description=f"Limit heat loss to less than {THERMAL_STORAGE_PARAMS.self_discharge_rate * 100:.1f}% per day"
        ),
        Requirement(
            name="Structural Integrity",
            description=f"Withstand thermal cycling for {THERMAL_STORAGE_PARAMS.design_life} years"
        )
    ]
)

# 3. Heat Exchanger System
heat_exchanger_system = System(
    name="Heat Exchanger System",
    description="System for charging and discharging thermal energy",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Heat Transfer Rate",
            description=f"Transfer heat at {THERMAL_STORAGE_PARAMS.max_power_output} during discharge"
        ),
        Requirement(
            name="Efficiency",
            description=f"Heat transfer efficiency of at least {THERMAL_STORAGE_PARAMS.heat_exchanger_efficiency * 100:.1f}%"
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
            name="Temperature Control",
            description=f"Maintain temperature within ±{THERMAL_STORAGE_PARAMS.temperature_control_tolerance}"
        ),
        Requirement(
            name="Safety Monitoring",
            description="Monitor all critical parameters and implement safety protocols"
        )
    ]
)

# 5. Integration System
integration_system = System(
    name="Integration System",
    description="Interface with industrial processes and energy sources",
    parent=thermal_storage_system,
    requirements=[
        Requirement(
            name="Process Compatibility",
            description="Compatible with target industrial processes"
        ),
        Requirement(
            name="Energy Source Flexibility",
            description="Accept energy from multiple sources including renewable electricity"
        )
    ]
)

print("Thermal storage system definitions loaded")
"""
Thermal storage system definition.
"""
from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

# Define the thermal storage system
thermal_storage_system = System(
    name="Thermal Energy Storage System",
    description=(
        f"{THERMAL_STORAGE_PARAMS.storage_capacity.magnitude}{THERMAL_STORAGE_PARAMS.storage_capacity.units} "
        f"thermal storage using {THERMAL_STORAGE_PARAMS.storage_medium.name}"
    ),
    requirements=[
        Requirement(
            name="Storage Capacity",
            description=(
                f"Store {THERMAL_STORAGE_PARAMS.storage_capacity.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.storage_capacity.units} of thermal energy"
            )
        ),
        Requirement(
            name="Temperature Range",
            description=(
                f"Operate between {THERMAL_STORAGE_PARAMS.min_temperature.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.min_temperature.units} and "
                f"{THERMAL_STORAGE_PARAMS.max_temperature.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.max_temperature.units}"
            )
        ),
        Requirement(
            name="Efficiency",
            description=(
                f"Achieve round-trip efficiency of at least "
                f"{THERMAL_STORAGE_PARAMS.charge_efficiency * THERMAL_STORAGE_PARAMS.discharge_efficiency * 100:.1f}%"
            )
        )
    ]
)

print("Thermal storage system defined")
