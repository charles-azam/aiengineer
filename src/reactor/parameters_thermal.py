from pyforge import Parameters, Quantity

class ThermalParameters(Parameters):
    """Define all the key parameters for the thermal systems."""
    # Primary loop parameters
    primary_pressure: Quantity = Quantity(15.5, "MPa")
    primary_temp_hot: Quantity = Quantity(320, "°C")
    primary_temp_cold: Quantity = Quantity(280, "°C")
    primary_flow_rate: Quantity = Quantity(1200, "kg/s")
    primary_coolant: str = "Light water"
    
    # Secondary loop parameters
    secondary_pressure: Quantity = Quantity(7.0, "MPa")
    secondary_temp_hot: Quantity = Quantity(285, "°C")
    secondary_temp_cold: Quantity = Quantity(230, "°C")
    secondary_flow_rate: Quantity = Quantity(100, "kg/s")
    secondary_coolant: str = "Light water"
    
    # Heat exchanger parameters
    heat_exchanger_type: str = "Shell and tube"
    heat_exchanger_material: str = "Inconel 690"
    heat_exchanger_capacity: Quantity = Quantity(65, "MW")
    
    # Turbine parameters
    turbine_type: str = "High-pressure steam turbine"
    turbine_efficiency: float = 0.87
    turbine_rpm: Quantity = Quantity(3600, "rpm")
    
    # Condenser parameters
    condenser_type: str = "Water-cooled surface condenser"
    condenser_cooling_method: str = "Forced draft cooling tower"
    condenser_capacity: Quantity = Quantity(40, "MW")

# single source of truth
THERMAL_PARAMS = ThermalParameters()

print(f"Thermal parameters loaded: Primary loop at {THERMAL_PARAMS.primary_pressure}, {THERMAL_PARAMS.primary_temp_hot}")
