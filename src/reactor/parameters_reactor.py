"""
Aggregated parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
This module imports and combines parameters from all subsystems.
"""

from pyforge import Parameters, Quantity
from reactor import UREG
from reactor.parameters_core import CORE_PARAMS
from reactor.parameters_fuel import TRISO_PARAMS as FUEL_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS

def burnup_unit(value):
    """Convert a numeric value to a burnup quantity with proper units."""
    return Quantity(value, "GWd_per_tHM")

# Define the main reactor parameters class
class ReactorParameters(Parameters):
    """
    Main reactor parameters aggregating key values from all subsystems.
    
    This class serves as the central parameter repository for the entire
    reactor system, providing a single source of truth for critical values.
    """
    # Core parameters
    thermal_power: Quantity = CORE_PARAMS.thermal_power
    core_inlet_temp: Quantity = THERMAL_PARAMS.core_inlet_temperature
    core_outlet_temp: Quantity = THERMAL_PARAMS.core_outlet_temperature
    core_pressure: Quantity = THERMAL_PARAMS.core_pressure
    
    # Fuel parameters
    fuel_type: str = FUEL_PARAMS.kernel_material
    fuel_enrichment: float = FUEL_PARAMS.uranium_enrichment.magnitude
    fuel_burnup: Quantity = FUEL_PARAMS.max_burnup
    
    # Operational parameters
    design_life: int = THERMAL_PARAMS.design_life
    refueling_interval: Quantity = FUEL_PARAMS.refueling_interval
    availability_factor: float = 0.9  # Default value
    planned_outage_duration: Quantity = FUEL_PARAMS.refueling_duration
    planned_outage_frequency: Quantity = FUEL_PARAMS.refueling_interval
    
    # Secondary loop parameters
    secondary_fluid: str = THERMAL_PARAMS.secondary_coolant
    secondary_temp_max: Quantity = THERMAL_PARAMS.secondary_outlet_temperature
    secondary_pressure: Quantity = THERMAL_PARAMS.secondary_pressure
    
    # Safety parameters
    decay_heat_removal: str = "Passive"
    emergency_shutdown_time: Quantity = Quantity(30, "second")
    normal_fuel_temp: Quantity = FUEL_PARAMS.max_temperature
    normal_vessel_temp: Quantity = Quantity(350, "degC")
    helium_delta_T: Quantity = Quantity(250, "delta_degC")
    helium_density: Quantity = Quantity(3.71, "kg/m^3")
    helium_specific_heat: Quantity = Quantity(5193, "J/(kg*K)")
    fuel_mass: Quantity = Quantity(2500, "kg")
    
    # Physical dimensions
    reactor_height: Quantity = Quantity(10, "m")
    reactor_diameter: Quantity = Quantity(5, "m")
    containment_thickness: Quantity = Quantity(1, "m")
    core_height: Quantity = CORE_PARAMS.core_height
    
    # Component lifetimes
    vessel_design_life: Quantity = Quantity(60, "year")
    graphite_design_life: Quantity = Quantity(20, "year")
    control_system_design_life: Quantity = Quantity(20, "year")
    
    # Additional parameters for design.py
    core_geometry: str = "Cylindrical"
    active_core_height: Quantity = CORE_PARAMS.core_height
    core_diameter: Quantity = CORE_PARAMS.core_diameter
    num_fuel_elements: int = CORE_PARAMS.number_of_fuel_columns
    num_control_rods: int = CORE_PARAMS.number_of_control_rods
    power_density: Quantity = CORE_PARAMS.power_density
    reflector_thickness: Quantity = CORE_PARAMS.reflector_thickness

# Create the single source of truth instance
REACTOR_PARAMS = ReactorParameters()

# Print key parameters for verification
print(f"HTGR Thermal Power: {REACTOR_PARAMS.thermal_power}")
print(f"Core outlet temperature: {REACTOR_PARAMS.core_outlet_temp}")
print(f"Design lifetime: {REACTOR_PARAMS.design_life}")
print(f"Fuel burnup: {REACTOR_PARAMS.fuel_burnup}")
print("Reactor parameters loaded successfully with burnup_unit function")
