"""
Heat exchanger system definition.
"""
from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

# Define the heat exchanger system
heat_exchanger_system = System(
    name="Heat Exchanger Network",
    description="Heat transfer interface for charging and discharging thermal storage",
    requirements=[
        Requirement(
            name="Power Rating",
            description=(
                f"Support charging and discharging at "
                f"{THERMAL_STORAGE_PARAMS.max_power_output.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.max_power_output.units}"
            )
        ),
        Requirement(
            name="Temperature Compatibility",
            description=(
                f"Handle fluid temperatures from {THERMAL_STORAGE_PARAMS.min_temperature.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.min_temperature.units} to "
                f"{THERMAL_STORAGE_PARAMS.max_temperature.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.max_temperature.units}"
            )
        )
    ]
)

print("Heat exchanger system defined")
