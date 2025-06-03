"""
Thermal-hydraulic parameters for the High-Temperature Gas-cooled Reactor (HTGR).
Defines all key parameters for the primary helium loop, secondary CO2 loop,
heat exchangers, and thermal characteristics.
"""

from pyforge import Parameters, Quantity, UREG
from dataclasses import field
from typing import Dict

class ThermalPowerParameters(Parameters):
    """Define the core thermal power parameters for our HTGR."""
    
    # Core thermal parameters
    core_thermal_power_options: Dict[str, Quantity] = field(default_factory=lambda: {
        "small": Quantity(10e6, "W"),
        "medium": Quantity(15e6, "W"),
        "large": Quantity(20e6, "W")
    })
    core_inlet_temperature: Quantity = Quantity(350, "°C")
    core_outlet_temperature: Quantity = Quantity(600, "°C")
    core_pressure: Quantity = Quantity(7, "MPa")
    thermal_efficiency: float = 0.42  # Overall thermal efficiency
    
    # Pressure drops
    core_pressure_drop: Quantity = Quantity(150, "kPa")
    
    # Thermal insulation properties
    insulation_thermal_conductivity: Quantity = Quantity(0.05, "W/(m*K)")
    insulation_thickness: Quantity = Quantity(300, "mm")
    max_outer_surface_temperature: Quantity = Quantity(50, "°C")
    
    # Industrial interface parameters
    industrial_steam_temperature: Quantity = Quantity(450, "°C")
    industrial_steam_pressure: Quantity = Quantity(4, "MPa")
    industrial_hot_air_temperature: Quantity = Quantity(500, "°C")
    industrial_thermal_oil_max_temperature: Quantity = Quantity(350, "°C")
    
    # System lifespan
    design_life: int = 20  # years
    refueling_interval: int = 5  # years
    
    # Additional parameters for simulation_thermal.py
    primary_coolant: str = "Helium"
    secondary_coolant: str = "CO2"
    primary_mass_flow_rate: Quantity = Quantity(20.3, "kg/s")
    secondary_mass_flow_rate: Quantity = Quantity(72.0, "kg/s")
    secondary_inlet_temperature: Quantity = Quantity(300, "°C")
    secondary_outlet_temperature: Quantity = Quantity(550, "°C")
    secondary_pressure: Quantity = Quantity(8, "MPa")
    primary_pressure: Quantity = Quantity(7, "MPa")
    primary_pressure_drop: Quantity = Quantity(350, "kPa")
    ihx_type: str = "Printed Circuit Heat Exchanger"
    ihx_capacity: Quantity = Quantity(15, "MW")
    ihx_effectiveness: float = 0.92
    process_hx_types: str = "Steam, Hot Air, Thermal Oil"
    process_heat_output: Quantity = Quantity(14, "MW")
    process_heat_min_temp: Quantity = Quantity(350, "°C")
    process_heat_max_temp: Quantity = Quantity(550, "°C")
    helium_flow_rate: Quantity = Quantity(20.3, "kg/s")
    primary_delta_t: Quantity = Quantity(250, "delta_degC")
    containment_leak_rate: Quantity = Quantity(0.1, "percent/day")

class PrimaryLoopParameters(Parameters):
    """Define the primary helium loop parameters for our HTGR."""
    
    # Primary helium loop parameters
    helium_specific_heat: Quantity = Quantity(5193, "J/(kg*K)")
    helium_thermal_conductivity: Quantity = Quantity(0.29, "W/(m*K)")
    helium_dynamic_viscosity: Quantity = Quantity(3.975e-5, "Pa*s")
    helium_density: Quantity = Quantity(3.71, "kg/m^3")  # at 7 MPa, 450°C average
    
    # Flow rates for different power levels
    helium_flow_rate_small: Quantity = Quantity(13.5, "kg/s")    # For 10 MW
    helium_flow_rate_medium: Quantity = Quantity(20.3, "kg/s")   # For 15 MW
    helium_flow_rate_large: Quantity = Quantity(27.0, "kg/s")    # For 20 MW
    
    # Pressure drops
    primary_loop_total_pressure_drop: Quantity = Quantity(350, "kPa")
    
    # Additional parameters needed for simulation_thermal.py
    mass_flow_rate: Quantity = Quantity(20.3, "kg/s")  # Default to medium size
    operating_pressure: Quantity = Quantity(7, "MPa")
    design_pressure_drop: Quantity = Quantity(350, "kPa")
    gas_constant: Quantity = Quantity(2077, "J/(kg*K)")  # Helium gas constant
    circulator_efficiency: float = 0.85

class SecondaryLoopParameters(Parameters):
    """Define the secondary CO2 loop parameters for our HTGR."""
    
    # Secondary CO2 loop parameters
    co2_pressure: Quantity = Quantity(8, "MPa")
    co2_inlet_temperature: Quantity = Quantity(300, "°C")
    co2_outlet_temperature: Quantity = Quantity(550, "°C")
    co2_specific_heat: Quantity = Quantity(1250, "J/(kg*K)")
    co2_thermal_conductivity: Quantity = Quantity(0.085, "W/(m*K)")
    co2_dynamic_viscosity: Quantity = Quantity(3.5e-5, "Pa*s")
    co2_density: Quantity = Quantity(42.5, "kg/m^3")  # at 8 MPa, 425°C average
    
    # CO2 flow rates for different power levels
    co2_flow_rate_small: Quantity = Quantity(48.0, "kg/s")    # For 10 MW
    co2_flow_rate_medium: Quantity = Quantity(72.0, "kg/s")   # For 15 MW
    co2_flow_rate_large: Quantity = Quantity(96.0, "kg/s")    # For 20 MW
    
    # Additional parameters needed for simulation_thermal.py
    mass_flow_rate: Quantity = Quantity(72.0, "kg/s")  # Default to medium size
    operating_pressure: Quantity = Quantity(8, "MPa")
    inlet_temperature: Quantity = Quantity(300, "°C")
    pressure_ratio: float = 1.2
    specific_heat: Quantity = Quantity(1250, "J/(kg*K)")
    specific_heat_ratio: float = 1.3
    compressor_efficiency: float = 0.8
    pressure_drop_coefficient: Quantity = Quantity(0.5, "kPa/(kg/s)^2")

class HeatExchangerParameters(Parameters):
    """Define the heat exchanger parameters for our HTGR."""
    
    # Heat exchanger parameters
    hx_effectiveness: float = 0.92
    hx_primary_side_pressure_drop: Quantity = Quantity(100, "kPa")
    hx_secondary_side_pressure_drop: Quantity = Quantity(120, "kPa")
    hx_heat_transfer_coefficient: Quantity = Quantity(1200, "W/(m^2*K)")
    hx_surface_area_small: Quantity = Quantity(500, "m^2")       # For 10 MW
    hx_surface_area_medium: Quantity = Quantity(750, "m^2")      # For 15 MW
    hx_surface_area_large: Quantity = Quantity(1000, "m^2")      # For 20 MW
    
    # Additional parameters needed for simulation_thermal.py
    efficiency: float = 0.92
    primary_pressure_drop: Quantity = Quantity(100, "kPa")
    secondary_pressure_drop: Quantity = Quantity(120, "kPa")

# Additional parameters needed for simulation_thermal.py
class IHXParameters(Parameters):
    """Define the intermediate heat exchanger parameters."""
    efficiency: float = 0.92
    heat_transfer_capacity: Quantity = Quantity(15, "MW")
    type: str = "Printed Circuit Heat Exchanger"
    effectiveness: float = 0.92
    primary_pressure_drop: Quantity = Quantity(100, "kPa")
    secondary_pressure_drop: Quantity = Quantity(120, "kPa")
    design_life: Quantity = Quantity(20, "year")

# Single source of truth - instances of each parameter class
THERMAL_PARAMS = ThermalPowerParameters()
PRIMARY_LOOP_PARAMS = PrimaryLoopParameters()
SECONDARY_LOOP_PARAMS = SecondaryLoopParameters()
HEAT_EXCHANGER_PARAMS = HeatExchangerParameters()
IHX_PARAMS = IHXParameters()

# Export all parameter objects for use in other modules
__all__ = [
    "THERMAL_PARAMS",
    "PRIMARY_LOOP_PARAMS", 
    "SECONDARY_LOOP_PARAMS",
    "HEAT_EXCHANGER_PARAMS",
    "IHX_PARAMS"
]

# Print key parameters for verification
print(f"HTGR Thermal Parameters:")
print(f"Core thermal power options: {THERMAL_PARAMS.core_thermal_power_options}")
print(f"Core outlet temperature: {THERMAL_PARAMS.core_outlet_temperature}")
print(f"Helium flow rate (20MW): {PRIMARY_LOOP_PARAMS.helium_flow_rate_large}")
print(f"CO2 flow rate (20MW): {SECONDARY_LOOP_PARAMS.co2_flow_rate_large}")
print(f"Heat exchanger effectiveness: {HEAT_EXCHANGER_PARAMS.hx_effectiveness}")
print("Thermal parameters loaded successfully")
