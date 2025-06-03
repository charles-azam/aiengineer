"""
Parameters for the High-Temperature Gas-cooled Reactor (HTGR) core design.
"""

from pyforge import Parameters, Quantity
from reactor import UREG

class CoreParameters(Parameters):
    """Define all the key parameters for the HTGR core design."""
    
    # Core thermal power options
    thermal_power_small: Quantity = Quantity(10, UREG.MWth)
    thermal_power_medium: Quantity = Quantity(15, UREG.MWth)
    thermal_power_large: Quantity = Quantity(20, UREG.MWth)
    thermal_power: Quantity = Quantity(15, UREG.MWth)  # Default to medium size
    
    # Core dimensions and geometry
    core_height: Quantity = Quantity(3.5, UREG.m)
    core_diameter: Quantity = Quantity(3.0, UREG.m)
    reflector_thickness: Quantity = Quantity(0.6, UREG.m)
    number_of_fuel_columns: int = 54
    number_of_blocks_per_column: int = 10
    core_volume: Quantity = Quantity(24.7, UREG.m**3)
    fuel_volume_fraction: float = 0.3
    
    # TRISO fuel specifications
    triso_kernel_diameter: Quantity = Quantity(500, UREG.micrometer)
    triso_coating_thickness: Quantity = Quantity(200, UREG.micrometer)
    triso_particles_per_compact: int = 10000
    fuel_enrichment: Quantity = Quantity(15.5, UREG.wt_percent)  # percent U-235
    fuel_loading: Quantity = Quantity(6.5, UREG.g / UREG.cm**3)  # Uranium loading
    fuel_particle_radius: Quantity = Quantity(250, UREG.micrometer)
    fuel_thermal_conductivity: Quantity = Quantity(30, UREG.W_per_mK)
    
    # Helium coolant properties
    helium_pressure: Quantity = Quantity(7, UREG.MPa)
    helium_mass_flow_rate: Quantity = Quantity(4.3, UREG.kg_per_s)  # For 10 MW design
    helium_specific_heat: Quantity = Quantity(5193, UREG.joule / (UREG.kg * UREG.kelvin))
    helium_thermal_conductivity: Quantity = Quantity(0.152, UREG.W_per_mK)
    coolant_mass_flow: Quantity = Quantity(20.3, UREG.kg_per_s)  # Default to medium size
    coolant_specific_heat: Quantity = Quantity(5193, UREG.joule / (UREG.kg * UREG.kelvin))
    coolant_channel_diameter: Quantity = Quantity(16, UREG.mm)
    coolant_velocity: Quantity = Quantity(40, UREG.m / UREG.s)
    coolant_density: Quantity = Quantity(3.71, UREG.kg / UREG.m**3)
    friction_factor: float = 0.02
    heat_transfer_coefficient: Quantity = Quantity(1000, UREG.W_per_m2K)
    heat_transfer_area: Quantity = Quantity(500, UREG.m**2)
    
    # Operating temperatures
    inlet_temperature: Quantity = Quantity(350, UREG.degC)
    outlet_temperature: Quantity = Quantity(600, UREG.degC)
    max_fuel_temperature: Quantity = Quantity(1200, UREG.degC)
    core_inlet_temp: Quantity = Quantity(350, UREG.degC)
    core_outlet_temp: Quantity = Quantity(600, UREG.degC)
    min_operating_temp: Quantity = Quantity(250, UREG.degC)
    max_operating_temp: Quantity = Quantity(650, UREG.degC)
    max_graphite_temp: Quantity = Quantity(1200, UREG.degC)
    max_reflector_temp: Quantity = Quantity(1000, UREG.degC)
    temp_measurement_accuracy: Quantity = Quantity(5, UREG.delta_degC)
    
    # Pressure parameters
    pressure_drop_core: Quantity = Quantity(0.1, UREG.MPa)
    
    # Control rod specifications
    number_of_control_rods: int = 12
    control_rod_count: int = 12
    control_rod_material: str = "B4C"
    control_rod_worth: Quantity = Quantity(15, UREG.pcm / UREG.cm)
    shutdown_margin: Quantity = Quantity(1, UREG.delta_k)
    total_rod_worth: Quantity = Quantity(12, "dimensionless")  # Total rod worth in dollars
    rod_insertion_time: Quantity = Quantity(30, UREG.second)
    
    # Core lifetime and refueling
    design_lifetime: int = 20  # years
    core_lifetime: Quantity = Quantity(20, UREG.year)
    refueling_interval: Quantity = Quantity(3, UREG.year)
    refueling_duration: Quantity = Quantity(14, UREG.day)
    burnup_target: Quantity = Quantity(150, UREG.GWd_per_tHM)
    
    # Neutronics parameters
    power_density: Quantity = Quantity(5, UREG.MWth / UREG.m**3)
    max_neutron_fluence: Quantity = Quantity(5e25, 1 / UREG.m**2)
    
    # Materials
    support_structure_material: str = "Alloy 800H"
    reflector_material: str = "Nuclear Grade Graphite"
    
    # Instrumentation
    instrument_lifetime: Quantity = Quantity(10, UREG.year)

# Single source of truth
CORE_PARAMS = CoreParameters()

# Print parameters for verification
print("HTGR Core Parameters:")
print(f"Thermal Power Options: {CORE_PARAMS.thermal_power_small}, {CORE_PARAMS.thermal_power_medium}, {CORE_PARAMS.thermal_power_large}")
print(f"Core Dimensions: {CORE_PARAMS.core_height} height, {CORE_PARAMS.core_diameter} diameter")
print(f"Operating Temperatures: {CORE_PARAMS.inlet_temperature} inlet, {CORE_PARAMS.outlet_temperature} outlet")
print(f"Design Lifetime: {CORE_PARAMS.design_lifetime} years with {CORE_PARAMS.refueling_interval} refueling interval")
print("DEBUG: Core parameters loaded successfully with custom nuclear units")
"""
Core parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Parameters, Quantity, UREG

class CoreParameters(Parameters):
    """Define all key parameters for the HTGR core."""
    # Power options
    thermal_power_small: Quantity = Quantity(10, "MWth")
    thermal_power_medium: Quantity = Quantity(15, "MWth")
    thermal_power_large: Quantity = Quantity(20, "MWth")
    
    # Temperature parameters
    core_outlet_temp: Quantity = Quantity(600, "degC")
    core_inlet_temp: Quantity = Quantity(350, "degC")
    temp_differential: Quantity = Quantity(250, "delta_degC")
    
    # Physical dimensions
    core_height: Quantity = Quantity(3.5, "m")
    core_diameter: Quantity = Quantity(3.0, "m")
    reflector_thickness: Quantity = Quantity(60, "cm")
    power_density: Quantity = Quantity(3.5, "MW/m^3")
    
    # Operational parameters
    primary_pressure: Quantity = Quantity(7, "MPa")
    core_pressure_drop: Quantity = Quantity(150, "kPa")
    
    # Lifecycle parameters
    design_life: Quantity = Quantity(20, "year")
    refueling_interval: Quantity = Quantity(5, "year")

# Single source of truth
CORE_PARAMS = CoreParameters()
