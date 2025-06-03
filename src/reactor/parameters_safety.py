"""
Safety parameters for High-Temperature Gas-cooled Reactor (HTGR) systems.

This module defines all key safety parameters for the HTGR design, including
passive safety systems, emergency systems, and containment specifications.
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
    temp_coefficient: Quantity = Quantity(-5e-5, "dimensionless/delta_degC")  # -5 pcm/°C
    shutdown_margin: Quantity = Quantity(5.0, "dimensionless")  # Value in "dollars" of reactivity
    
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
    temperature_reactivity_coeff: Quantity = Quantity(-5e-5, "dimensionless/delta_degC")  # -5 pcm/°C
    
    # Emergency parameters
    emergency_response_time: Quantity = Quantity(30, "minute")
    cooling_safety_margin: float = 0.2
    minimum_shutdown_cooling: Quantity = Quantity(0.5, "megawatt")
    
    # Additional parameters needed for simulation_safety.py
    delayed_neutron_fraction: float = 0.0065
    prompt_neutron_lifetime: Quantity = Quantity(1e-3, "second")
    temperature_coefficient: Quantity = Quantity(-5e-5, "dimensionless/kelvin")  # Reactivity temperature coefficient
    control_rod_worth: Quantity = Quantity(0.15, "dimensionless")  # Reactivity worth
    core_activity: Quantity = Quantity(1e18, "becquerel")
    max_fuel_temp_limit: Quantity = Quantity(1600, "degC")
    containment_leak_rate: Quantity = Quantity(0.1, "percent/day")
    max_worker_dose: Quantity = Quantity(20, "mSv")
    max_public_dose: Quantity = Quantity(1, "mSv")
    emergency_shutdown_time: Quantity = Quantity(3, "second")

# Single source of truth
SAFETY_PARAMS = SafetyParameters()

# Print key safety parameters for verification
print(f"Maximum TRISO fuel temperature (normal): {SAFETY_PARAMS.max_normal_fuel_temp}")
print(f"Maximum TRISO fuel temperature (accident): {SAFETY_PARAMS.max_accident_fuel_temp}")
print(f"Passive cooling duration: {SAFETY_PARAMS.passive_cooling_duration}")
print(f"Temperature coefficient: {SAFETY_PARAMS.temperature_coefficient}")
print("Safety parameters loaded successfully with custom reactor units")
"""
Safety parameters for High-Temperature Gas-cooled Reactor (HTGR) systems.

This module defines all key safety parameters for the HTGR design, including
passive safety systems, emergency systems, and containment specifications.
"""

from pyforge import Parameters, Quantity
from reactor import UREG

class SafetyParameters(Parameters):
    """Combined safety parameters for the HTGR design."""
    
    # Core design parameters
    thermal_power: Quantity = Quantity(20, "megawatt")  # Base design, can be scaled to 10 or 15 MW
    core_height: Quantity = Quantity(3.5, "m")
    core_diameter: Quantity = Quantity(3.0, "m")
    core_power_density: Quantity = Quantity(3.0, "MW/m^3")
    helium_pressure: Quantity = Quantity(7, "MPa")
    helium_inlet_temp: Quantity = Quantity(350, "degC")
    helium_outlet_temp: Quantity = Quantity(600, "degC")  # Target for industrial heat
    helium_mass_flow: Quantity = Quantity(12, "kg/s")
    
    # TRISO fuel parameters
    triso_kernel_diameter: Quantity = Quantity(500, "micrometer")
    triso_coating_thickness: Quantity = Quantity(200, "micrometer")
    triso_packing_fraction: float = 0.35  # Volume fraction in fuel compact
    max_normal_fuel_temp: Quantity = Quantity(1250, "degC")
    max_accident_fuel_temp: Quantity = Quantity(1600, "degC")
    triso_failure_temp: Quantity = Quantity(1800, "degC")
    triso_burnup_limit: Quantity = Quantity(0.20, "dimensionless")  # 20% FIMA
    triso_fluence_limit: Quantity = Quantity(5e25, "1/m^2")
    
    # Passive safety parameters
    passive_cooling_capacity: Quantity = Quantity(3, "megawatt")
    passive_cooling_duration: Quantity = Quantity(7, "day")
    vessel_surface_area: Quantity = Quantity(150, "m^2")
    vessel_emissivity: float = 0.8
    natural_convection_coefficient: Quantity = Quantity(10, "watt/(meter^2*kelvin)")
    decay_heat_removal_capacity: Quantity = Quantity(3, "megawatt")
    
    # Vessel parameters
    vessel_inner_diameter: Quantity = Quantity(4.5, "m")
    vessel_height: Quantity = Quantity(12, "m")
    vessel_thickness: Quantity = Quantity(20, "cm")
    max_vessel_temp_limit: Quantity = Quantity(550, "degC")
    
    # Radiation and shielding parameters
    bio_shield_thickness: Quantity = Quantity(150, "cm")
    containment_thickness: Quantity = Quantity(100, "cm")
    annual_dose_limit: Quantity = Quantity(1, "mSv")
    dose_rate_limit: Quantity = Quantity(0.1, "mSv/hour")
    max_worker_dose: Quantity = Quantity(20, "mSv")
    max_public_dose: Quantity = Quantity(1, "mSv")
    containment_leak_rate: Quantity = Quantity(0.1, "percent/day")
    
    # Reactivity parameters
    temperature_coefficient: Quantity = Quantity(-5e-5, "delta_k/kelvin")
    shutdown_margin: Quantity = Quantity(5.0, "dimensionless")  # Value in "dollars"
    delayed_neutron_fraction: float = 0.0065
    prompt_neutron_lifetime: Quantity = Quantity(1e-3, "second")
    control_rod_worth: Quantity = Quantity(0.15, "delta_k")
    
    # Secondary CO2 loop parameters
    co2_pressure: Quantity = Quantity(20, "MPa")
    co2_inlet_temp: Quantity = Quantity(300, "degC")
    co2_outlet_temp: Quantity = Quantity(550, "degC")
    co2_mass_flow: Quantity = Quantity(15, "kg/s")
    
    # Operational parameters
    design_lifetime: Quantity = Quantity(20, "year")
    refueling_interval: Quantity = Quantity(5, "year")
    availability_factor: float = 0.95
    
    # Emergency parameters
    emergency_response_time: Quantity = Quantity(30, "minute")
    emergency_shutdown_time: Quantity = Quantity(3, "second")
    cooling_safety_margin: float = 0.2
    minimum_shutdown_cooling: Quantity = Quantity(0.5, "megawatt")

# Single source of truth
SAFETY_PARAMS = SafetyParameters()

# Print key design parameters for verification
print(f"HTGR Thermal Power: {SAFETY_PARAMS.thermal_power}")
print(f"Helium Outlet Temperature: {SAFETY_PARAMS.helium_outlet_temp}")
print(f"Maximum TRISO fuel temperature (normal): {SAFETY_PARAMS.max_normal_fuel_temp}")
print(f"Maximum TRISO fuel temperature (accident): {SAFETY_PARAMS.max_accident_fuel_temp}")
print(f"Passive cooling duration: {SAFETY_PARAMS.passive_cooling_duration}")
print(f"Temperature coefficient: {SAFETY_PARAMS.temperature_coefficient}")
print(f"Design lifetime: {SAFETY_PARAMS.design_lifetime}")
print("Safety parameters loaded successfully with custom reactor units")
"""
Safety parameters for the HTGR reactor design.

This module defines safety-related parameters for the high-temperature
gas-cooled reactor, including reactivity coefficients, control rod worth,
and other safety-critical values.
"""

from pyforge import Parameters, Quantity

class SafetyParameters(Parameters):
    """Safety parameters for the HTGR reactor design."""
    
    # Reactivity coefficients
    temperature_coefficient: Quantity = Quantity(-5e-5, "dimensionless/kelvin")
    void_coefficient: Quantity = Quantity(-2e-4, "dimensionless/percent")
    
    # Control and shutdown systems
    control_rod_worth: Quantity = Quantity(0.15, "dimensionless")
    shutdown_margin: Quantity = Quantity(0.02, "dimensionless")
    
    # Safety limits
    max_fuel_temperature: Quantity = Quantity(1600, "degC")
    max_pressure: Quantity = Quantity(7, "MPa")
    
    # Emergency systems
    decay_heat_removal_capacity: Quantity = Quantity(2, "MWth")
    emergency_cooling_time: Quantity = Quantity(72, "hour")

# Single source of truth
SAFETY_PARAMS = SafetyParameters()
"""
Safety parameters for High-Temperature Gas-cooled Reactor (HTGR) designs.

This module defines safety-related parameters and limits for HTGR systems,
including temperature limits, pressure boundaries, and radiation thresholds.
"""

from pyforge import Parameters, Quantity, UREG

class SafetyParameters(Parameters):
    """Safety parameters for HTGR designs."""
    
    # Temperature limits
    max_fuel_temp: Quantity = Quantity(1600, "degC")  # Maximum TRISO fuel temperature
    max_core_outlet_temp: Quantity = Quantity(850, "degC")  # Maximum core outlet temperature
    max_vessel_temp: Quantity = Quantity(450, "degC")  # Maximum reactor vessel temperature
    
    # Pressure limits
    max_primary_pressure: Quantity = Quantity(7, "MPa")  # Maximum primary loop pressure
    max_secondary_pressure: Quantity = Quantity(5, "MPa")  # Maximum secondary loop pressure
    
    # Radiation limits
    max_worker_dose: Quantity = Quantity(20, "mSv/year")  # Maximum worker radiation dose
    max_public_dose: Quantity = Quantity(1, "mSv/year")  # Maximum public radiation dose
    
    # Reactivity limits
    max_reactivity_insertion: Quantity = Quantity(0.006, "delta_k")  # Maximum reactivity insertion
    shutdown_margin: Quantity = Quantity(0.01, "delta_k")  # Minimum shutdown margin
    
    # Cooling requirements
    min_decay_heat_removal: Quantity = Quantity(1, "percent")  # Minimum decay heat removal capability
    
    # Emergency response times
    scram_response_time: Quantity = Quantity(2, "second")  # Control rod insertion time
    
    # Power limits
    max_power_density: Quantity = Quantity(4.5, "MW/m^3")  # Maximum power density
    max_thermal_power: Quantity = Quantity(20, "megawatt")  # Maximum thermal power output

# Single source of truth for safety parameters
SAFETY_PARAMS = SafetyParameters()

print("Safety parameters loaded with maximum thermal power:", SAFETY_PARAMS.max_thermal_power)
