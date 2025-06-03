"""
Parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Parameters, Quantity
from reactor import UREG

class ReactorParameters(Parameters):
    """
    Main reactor system parameters for the modular HTGR design.
    
    Consolidates parameters from various subsystems into a single
    source of truth for the overall reactor system.
    """
    # Core parameters - available in three standard sizes
    thermal_power_options: list = [10, 15, 20]  # MWth
    thermal_power: Quantity = Quantity(15, "MWth")
    core_height: Quantity = Quantity(3.5, "m")
    core_diameter: Quantity = Quantity(2.8, "m")
    
    # Thermal parameters
    core_inlet_temp: Quantity = Quantity(350, "degC")
    core_outlet_temp: Quantity = Quantity(600, "degC")
    helium_pressure: Quantity = Quantity(7, "MPa")
    helium_flow_rate: Quantity = Quantity(8.2, "kg/s")
    
    # Fuel parameters
    fuel_type: str = "TRISO particles"
    enrichment: Quantity = Quantity(15.5, "wt_percent")
    fuel_loading: Quantity = Quantity(5, "kgU/m^3")
    kernel_diameter: Quantity = Quantity(500, "micrometer")
    packing_fraction: Quantity = Quantity(0.35, "dimensionless")
    
    # Physical parameters
    module_height: Quantity = Quantity(12, "m")
    module_diameter: Quantity = Quantity(4.5, "m")
    module_weight: Quantity = Quantity(250, "tonne")
    
    # Secondary loop parameters
    secondary_fluid: str = "CO2"
    secondary_temp: Quantity = Quantity(550, "degC")
    secondary_pressure: Quantity = Quantity(5, "MPa")
    heat_exchanger_type: str = "Printed circuit heat exchanger"
    
    # Operational parameters
    design_lifetime: Quantity = Quantity(20, "year")
    refueling_interval: Quantity = Quantity(5, "year")
    capacity_factor: float = 0.95
    availability: float = 0.98
    
    # Safety parameters
    decay_heat_removal: str = "Passive air cooling"
    containment_type: str = "Steel pressure vessel"
    emergency_shutdown: str = "Control rod insertion and reserve shutdown system"
    fission_product_barrier: str = "TRISO coating layers (PyC, SiC)"

# Single source of truth for reactor parameters
REACTOR_PARAMS = ReactorParameters()

# Print key reactor parameters for verification
print(f"HTGR Reactor: {REACTOR_PARAMS.thermal_power} thermal, "
      f"{REACTOR_PARAMS.core_outlet_temp} outlet temperature")
print(f"Module dimensions: {REACTOR_PARAMS.module_diameter} diameter × "
      f"{REACTOR_PARAMS.module_height} height")
print(f"Design lifetime: {REACTOR_PARAMS.design_lifetime} with "
      f"{REACTOR_PARAMS.refueling_interval} refueling interval")
print(f"Available power options: {REACTOR_PARAMS.thermal_power_options} MWth")
print("Reactor parameters initialized successfully")
