"""
Coolant parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Parameters, Quantity, UREG

class CoolantParameters(Parameters):
    """Define all key parameters for the primary and secondary coolant systems."""
    # Primary coolant (Helium)
    primary_coolant: str = "Helium"
    helium_flow_rate_large: Quantity = Quantity(27, "kg/s")  # For 20 MW configuration
    
    # Secondary coolant (CO2)
    secondary_coolant: str = "CO2"
    secondary_max_temp: Quantity = Quantity(570, "degC")
    secondary_pressure: Quantity = Quantity(10, "MPa")
    co2_inlet_temp: Quantity = Quantity(300, "degC")
    co2_outlet_temp: Quantity = Quantity(570, "degC")
    co2_flow_rate_large: Quantity = Quantity(96, "kg/s")  # For 20 MW configuration

# Single source of truth
COOLANT_PARAMS = CoolantParameters()
