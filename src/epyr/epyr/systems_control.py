"""
Control system definition.
"""
from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

# Define the control system
control_system = System(
    name="Control and Monitoring System",
    description="System for monitoring and controlling thermal storage operation",
    requirements=[
        Requirement(
            name="Temperature Control",
            description=(
                f"Maintain temperatures between {THERMAL_STORAGE_PARAMS.min_temperature.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.min_temperature.units} and "
                f"{THERMAL_STORAGE_PARAMS.max_temperature.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.max_temperature.units}"
            )
        ),
        Requirement(
            name="Safety Features",
            description="Provide automatic shutdown in case of temperature or pressure excursions"
        )
    ]
)

print("Control system defined")
