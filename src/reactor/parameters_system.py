"""
System-level parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Parameters, Quantity, UREG

class SystemParameters(Parameters):
    """Define all key system-level parameters for the HTGR."""
    # Performance parameters
    thermal_efficiency: float = 0.92  # 92% heat transfer efficiency
    parasitic_power_large: Quantity = Quantity(4.3, "MW")  # For 20 MW configuration
    
    # Availability parameters
    annual_availability: float = 0.90  # 90% excluding planned outages
    planned_outage_duration: Quantity = Quantity(30, "day")
    unplanned_outage_allowance: Quantity = Quantity(7, "day/year")
    
    # Economic parameters
    lcoh: Quantity = Quantity(45.75, "$/MWh")  # Levelized Cost of Heat
    capital_cost: Quantity = Quantity(4500, "$/kW")
    operational_cost: Quantity = Quantity(12, "$/MWh")
    carbon_emissions: Quantity = Quantity(5, "kg/MWh")
    payback_period: Quantity = Quantity(13.5, "year")

# Single source of truth
SYSTEM_PARAMS = SystemParameters()
