"""
Parameters for High-Temperature Gas-cooled Reactor (HTGR) design.
"""
from pyforge import Parameters, Quantity, UREG

# Register custom units
UREG.define('USD = [currency]')

class HTGRParameters(Parameters):
    """Define all the key parameters for our HTGR reactor."""
    # Fuel parameters
    fuel_type: str = "TRISO"
    fuel_enrichment: str = "15% U-235"
    fuel_kernel_diameter: Quantity = Quantity(500, "μm")
    
    # Core parameters
    core_inlet_temp: Quantity = Quantity(350, "°C")
    core_outlet_temp: Quantity = Quantity(600, "°C")
    core_height: Quantity = Quantity(3.5, "m")
    core_diameter: Quantity = Quantity(3.0, "m")
    core_volume: Quantity = Quantity(24.7, "m^3")
    power_density: Quantity = Quantity(6.0, "MW/m^3")
    selected_power: Quantity = Quantity(15, "MW")  # Default power
    thermal_power_options: list = [
        Quantity(10, "MW"),  # Small
        Quantity(15, "MW"),  # Medium
        Quantity(20, "MW"),  # Large
    ]
    design_lifetime: Quantity = Quantity(20, "years")
    refueling_interval: Quantity = Quantity(5, "years")
    
    # Cooling parameters
    helium_pressure: Quantity = Quantity(7, "MPa")
    helium_flow_rate: Quantity = Quantity(8.5, "kg/s")
    secondary_fluid: str = "CO₂"
    secondary_pressure: Quantity = Quantity(20, "MPa")
    secondary_max_temp: Quantity = Quantity(550, "°C")
    secondary_flow_rate: Quantity = Quantity(85, "kg/s")
    secondary_inlet_temp: Quantity = Quantity(300, "°C")
    secondary_outlet_temp: Quantity = Quantity(500, "°C")
    
    # Heat exchanger parameters
    heat_exchanger_efficiency: float = 0.92
    heat_exchanger_area: Quantity = Quantity(500, "m^2")
    
    # Vessel dimensions
    vessel_height: Quantity = Quantity(12, "m")
    vessel_diameter: Quantity = Quantity(5, "m")
    vessel_height_small: Quantity = Quantity(8, "m")
    vessel_diameter_small: Quantity = Quantity(3.5, "m")
    vessel_height_medium: Quantity = Quantity(10, "m")
    vessel_diameter_medium: Quantity = Quantity(4, "m")
    vessel_height_large: Quantity = Quantity(12, "m")
    vessel_diameter_large: Quantity = Quantity(4.5, "m")
    
    # Safety parameters
    fuel_temp_limit: Quantity = Quantity(1600, "°C")
    emergency_shutdown_time: Quantity = Quantity(30, "seconds")
    radiation_exposure_limit: Quantity = Quantity(1, "mSv/year")
    temperature_tolerance: Quantity = Quantity(5, "°C")
    core_lifetime: Quantity = Quantity(5, "year")
    
    # Process parameters
    process_temperature: Quantity = Quantity("400 to 550", "°C")
    fuel_cycle_length: Quantity = Quantity(5, "years")

# Single source of truth
HTGR_PARAMS = HTGRParameters()
