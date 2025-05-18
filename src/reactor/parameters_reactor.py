"""
Parameters for the Small Modular Reactor design.
Contains engineering parameters with appropriate units.
"""

from pyforge import Parameters, Quantity

class ReactorParameters(Parameters):
    """Core reactor parameters for a 20 MW small modular reactor."""
    # Power specifications
    thermal_power: Quantity = Quantity(60, "MW")  # Thermal power (assuming ~33% efficiency)
    electrical_power: Quantity = Quantity(20, "MW")  # Target electrical output
    
    # Helper method to access magnitude
    def get_value(self, param_name):
        """Get the magnitude value of a parameter"""
        param = getattr(self, param_name)
        return param.magnitude
    
    # Core dimensions
    core_height: Quantity = Quantity(2.0, "m")
    core_diameter: Quantity = Quantity(1.4, "m")  # Optimized dimensions for better power density
    
    # Fuel specifications
    fuel_type: str = "HALEU"  # High-Assay Low-Enriched Uranium
    fuel_enrichment: Quantity = Quantity(19.75, "%")  # Below 20% for non-proliferation
    fuel_assembly_count: int = 69  # Increased for longer cycle length
    fuel_rods_per_assembly: int = 264
    
    # Operational parameters
    design_lifetime: Quantity = Quantity(40, "years")
    refueling_interval: Quantity = Quantity(4, "years")
    capacity_factor: Quantity = Quantity(90, "%")  # Realistic availability
    uranium_loading: Quantity = Quantity(4800, "kg")  # Increased uranium loading for longer cycle
    
    # Safety parameters
    max_fuel_temperature: Quantity = Quantity(1200, "°C")
    normal_operating_temperature: Quantity = Quantity(320, "°C")
    design_pressure: Quantity = Quantity(15, "MPa")

REACTOR_PARAMS = ReactorParameters()

class PrimaryLoopParameters(Parameters):
    """Parameters for the primary cooling loop."""
    coolant_type: str = "Pressurized Water"
    coolant_flow_rate: Quantity = Quantity(364, "kg/s")  # Exactly matches thermal power requirements
    inlet_temperature: Quantity = Quantity(290, "°C")
    outlet_temperature: Quantity = Quantity(320, "°C")
    operating_pressure: Quantity = Quantity(15, "MPa")
    primary_pump_power: Quantity = Quantity(600, "kW")  # Sized for the flow rate
    primary_pump_count: int = 2  # Redundancy for safety
    
    # Heat exchanger specifications
    heat_exchanger_type: str = "Helical Coil"  # Changed to more compact design
    heat_exchanger_material: str = "Inconel 690"
    heat_transfer_capacity: Quantity = Quantity(60, "MW")
    
    # Reactor vessel specifications
    vessel_material: str = "SA-508 Grade 3 Class 1"
    vessel_cladding: str = "308L/309L Stainless Steel"
    vessel_diameter: Quantity = Quantity(3.0, "m")
    vessel_height: Quantity = Quantity(7.5, "m")
    vessel_wall_thickness: Quantity = Quantity(200, "mm")

PRIMARY_LOOP_PARAMS = PrimaryLoopParameters()

class SecondaryLoopParameters(Parameters):
    """Parameters for the secondary steam loop."""
    working_fluid: str = "Water/Steam"
    steam_flow_rate: Quantity = Quantity(8.83, "kg/s")  # Exactly matches electrical power output
    steam_temperature: Quantity = Quantity(280, "°C")
    steam_pressure: Quantity = Quantity(7, "MPa")
    condenser_cooling_method: str = "Water-cooled"
    condenser_cooling_capacity: Quantity = Quantity(40, "MW")
    
    # Turbine specifications
    turbine_type: str = "Multi-stage Steam Turbine"
    turbine_efficiency: Quantity = Quantity(87, "%")
    generator_capacity: Quantity = Quantity(22, "MW")  # Slightly oversized
    generator_efficiency: Quantity = Quantity(98, "%")

SECONDARY_LOOP_PARAMS = SecondaryLoopParameters()

class ContainmentParameters(Parameters):
    """Parameters for the reactor containment structure."""
    containment_type: str = "Steel-Reinforced Concrete"
    wall_thickness: Quantity = Quantity(1.2, "m")
    height: Quantity = Quantity(25, "m")
    diameter: Quantity = Quantity(15, "m")
    design_pressure: Quantity = Quantity(0.4, "MPa")
    leak_rate: Quantity = Quantity(0.1, "%/day")
    foundation_width: Quantity = Quantity(22, "m")  # Increased foundation size for better soil bearing capacity
    foundation_depth: Quantity = Quantity(3, "m")   # Deep foundation for improved stability
    
    # Safety systems
    passive_cooling_capacity: Quantity = Quantity(3, "MW")
    emergency_water_supply: Quantity = Quantity(500, "m³")

CONTAINMENT_PARAMS = ContainmentParameters()
