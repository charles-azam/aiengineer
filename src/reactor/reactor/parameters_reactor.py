"""
Parameters for the Small Modular Reactor (SMR) design.
"""
from pyforge import Parameters, Quantity

class ReactorParameters(Parameters):
    """Define all key parameters for the SMR reactor."""
    # Core parameters
    thermal_power: Quantity = Quantity(60, "MW")  # Thermal output
    electrical_power: Quantity = Quantity(20, "MW")  # Electrical output
    thermal_efficiency: float = 0.33  # Conversion efficiency
    core_height: Quantity = Quantity(2.5, "m")
    core_diameter: Quantity = Quantity(1.8, "m")
    fuel_type: str = "UO2"  # Uranium dioxide
    enrichment: float = 4.95  # % U-235
    fuel_assemblies: int = 37  # Number of fuel assemblies
    
    # Primary loop parameters
    primary_pressure: Quantity = Quantity(15.5, "MPa")
    primary_temp_inlet: Quantity = Quantity(290, "°C")
    primary_temp_outlet: Quantity = Quantity(325, "°C")
    primary_flow_rate: Quantity = Quantity(320, "kg/s")
    
    # Secondary loop parameters
    secondary_pressure: Quantity = Quantity(7.0, "MPa")
    secondary_temp_inlet: Quantity = Quantity(230, "°C")
    secondary_temp_outlet: Quantity = Quantity(290, "°C")
    secondary_flow_rate: Quantity = Quantity(110, "kg/s")
    
    # Operational parameters
    design_life: int = 60  # years
    refueling_interval: int = 24  # months
    availability_factor: float = 0.95  # % uptime
    
    # Physical dimensions
    containment_height: Quantity = Quantity(25, "m")
    containment_diameter: Quantity = Quantity(15, "m")
    total_weight: Quantity = Quantity(350, "ton")

# Single source of truth
REACTOR_PARAMS = ReactorParameters()
