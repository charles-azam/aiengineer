"""
Integration system definition.
"""
from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

# Define the integration system
integration_system = System(
    name="Process Integration Interface",
    description="Interface to connect thermal storage with industrial processes",
    requirements=[
        Requirement(
            name="Process Compatibility",
            description=(
                f"Deliver heat at temperatures compatible with "
                f"{THERMAL_STORAGE_PARAMS.industrial_application.name} processes "
                f"({THERMAL_STORAGE_PARAMS.industrial_application.temperature_range['min']} to "
                f"{THERMAL_STORAGE_PARAMS.industrial_application.temperature_range['max']})"
            )
        ),
        Requirement(
            name="Energy Savings",
            description=(
                f"Enable energy cost savings of at least "
                f"{THERMAL_STORAGE_PARAMS.industrial_application.potential_energy_savings * 100:.1f}%"
            )
        )
    ]
)

print("Integration system defined")
