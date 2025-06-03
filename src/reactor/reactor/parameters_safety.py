"""
Safety parameters for High-Temperature Gas-cooled Reactor (HTGR) systems.

This module defines all key safety parameters for the HTGR design, including
passive safety features, emergency systems, and containment specifications.
"""

from pyforge import Parameters, Quantity
from reactor import UREG

class SafetyParameters(Parameters):
    """Combined safety parameters for the HTGR design."""
    # Passive heat removal parameters
    passive_cooling_capacity: Quantity = Quantity(3, "megawatt")
    passive_cooling_duration: Quantity = Quantity(7, "day")
    vessel_surface_area: Quantity = Quantity(150, "m^2")
    vessel_emissivity: float = 0.8
    natural_convection_coefficient: Quantity = Quantity(10, "watt/(meter^2*kelvin)")
    
    # TRISO fuel parameters
    max_normal_fuel_temp: Quantity = Quantity(1250, "degC")
    max_accident_fuel_temp: Quantity = Quantity(1600, "degC")
    triso_failure_temp: Quantity = Quantity(1800, "degC")
    triso_temp_limit: Quantity = Quantity(1600, "degC")
    triso_burnup_limit: Quantity = Quantity(0.20, "dimensionless")  # 20%
    triso_fluence_limit: Quantity = Quantity(5e25, "1/m^2")
    triso_free_volume: Quantity = Quantity(1e-14, "m^3")
    triso_pressure_limit: Quantity = Quantity(100, "MPa")
    
    # Vessel parameters
    max_vessel_temp_limit: Quantity = Quantity(550, "degC")
    vessel_thickness: Quantity = Quantity(20, "cm")
    
    # Radiation parameters
    bio_shield_thickness: Quantity = Quantity(150, "cm")
    containment_thickness: Quantity = Quantity(100, "cm")
    annual_dose_limit: Quantity = Quantity(1, "mSv")
    dose_rate_limit: Quantity = Quantity(0.1, "mSv/hour")
    
    # Reactivity parameters
    temp_coefficient: Quantity = Quantity(-5, "dimensionless")  # Temperature coefficient
    shutdown_margin: Quantity = Quantity(5.0, "dimensionless")  # Shutdown margin
    
    # Decay heat parameters
    decay_heat_removal_capacity: Quantity = Quantity(3, "megawatt")
    
    # Thermal parameters
    effective_emissivity: float = 0.8
    natural_convection_coeff: Quantity = Quantity(10, "watt/(meter^2*kelvin)")
    effective_conductivity: Quantity = Quantity(20, "watt/(meter*kelvin)")
    conduction_path_length: Quantity = Quantity(0.5, "m")
    thermal_expansion_coeff: float = 0.003  # per K
    flow_resistance: float = 100.0  # Pa/(kg/s)^2
    fuel_specific_heat: Quantity = Quantity(1000, "joule/(kilogram*kelvin)")
    
    # Control parameters
    control_redundancy: int = 3
    monitored_parameters: int = 150
    sensor_redundancy: int = 2
    control_response_time: Quantity = Quantity(0.5, "second")
    temperature_reactivity_coeff: Quantity = Quantity(-5, "dimensionless/delta_degC")
    
    # Emergency parameters
    emergency_response_time: Quantity = Quantity(30, "minute")
    cooling_safety_margin: float = 0.2
    minimum_shutdown_cooling: Quantity = Quantity(0.5, "megawatt")
    
    # Additional parameters needed for simulation_safety.py
    delayed_neutron_fraction: float = 0.0065
    prompt_neutron_lifetime: Quantity = Quantity(1e-3, "second")
    temperature_coefficient: Quantity = Quantity(-5e-5, "dimensionless/kelvin")
    core_activity: Quantity = Quantity(1e18, "becquerel")
    max_fuel_temp_limit: Quantity = Quantity(1600, "degC")
    containment_leak_rate: Quantity = Quantity(0.1, "percent/day")
    max_worker_dose: Quantity = Quantity(20, "mSv")
    max_public_dose: Quantity = Quantity(1, "mSv")

# Single source of truth
SAFETY_PARAMS = SafetyParameters()

# Print key safety parameters for verification
print(f"Maximum TRISO fuel temperature (normal): {SAFETY_PARAMS.max_normal_fuel_temp}")
print(f"Maximum TRISO fuel temperature (accident): {SAFETY_PARAMS.max_accident_fuel_temp}")
print(f"Passive cooling duration: {SAFETY_PARAMS.passive_cooling_duration}")
print(f"Temperature coefficient: {SAFETY_PARAMS.temperature_coefficient}")
print("Safety parameters loaded successfully with custom reactor units")
