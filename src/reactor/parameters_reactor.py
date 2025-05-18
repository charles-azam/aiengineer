from pyforge import Parameters, Quantity

class ReactorParameters(Parameters):
    """Define all the key parameters for our small modular reactor."""
    thermal_power: Quantity = Quantity(60, "MW")  # thermal output
    electrical_power: Quantity = Quantity(20, "MW")  # electrical output
    efficiency: float = 0.33  # thermal to electrical conversion efficiency
    core_height: Quantity = Quantity(2.5, "m")
    core_diameter: Quantity = Quantity(1.8, "m")
    fuel_type: str = "UO2"  # Uranium dioxide
    enrichment: float = 4.95  # % U-235
    fuel_assemblies: int = 37  # number of fuel assemblies
    fuel_rods_per_assembly: int = 264  # number of fuel rods per assembly
    control_rods: int = 16  # number of control rod assemblies
    design_life: int = 60  # years
    refueling_interval: int = 2  # years

# single source of truth
REACTOR_PARAMS = ReactorParameters()

print(f"Reactor parameters loaded: {REACTOR_PARAMS.thermal_power} thermal, {REACTOR_PARAMS.electrical_power} electrical")
