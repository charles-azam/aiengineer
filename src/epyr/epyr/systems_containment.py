"""
Containment system definition.
"""
from pyforge import System, Requirement
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

# Define the containment system
containment_system = System(
    name="Thermal Storage Containment",
    description="Storage vessel for thermal storage medium",
    requirements=[
        Requirement(
            name="Volume Capacity",
            description=(
                f"Contain {THERMAL_STORAGE_PARAMS.storage_volume.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.storage_volume.units} of storage medium"
            )
        ),
        Requirement(
            name="Insulation Performance",
            description=(
                f"Limit heat loss to less than {THERMAL_STORAGE_PARAMS.self_discharge_rate * 100:.1f}% "
                f"of capacity per day with {THERMAL_STORAGE_PARAMS.insulation_thickness.magnitude}"
                f"{THERMAL_STORAGE_PARAMS.insulation_thickness.units} insulation"
            )
        )
    ]
)

print("Containment system defined")
