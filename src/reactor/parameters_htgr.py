"""
Parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
Defines all key design parameters with appropriate units.
"""

from pyforge import Parameters, Quantity, UREG

class CoreParameters(Parameters):
    """Core design parameters for the HTGR system."""
    thermal_power_small: Quantity = Quantity(10, "MW")  # Small configuration
    thermal_power_medium: Quantity = Quantity(15, "MW")  # Medium configuration
    thermal_power_large: Quantity = Quantity(20, "MW")  # Large configuration
    core_height: Quantity = Quantity(3.5, "m")  # Active core height
    core_diameter: Quantity = Quantity(3.0, "m")  # Core diameter including reflector
    power_density: Quantity = Quantity(3.5, "MW/m^3")  # Conservative for HTGR
    reflector_thickness: Quantity = Quantity(60, "cm")  # Graphite reflector
    control_rods: int = 24  # Number of control rod assemblies
    fuel_elements_medium: int = 1500  # Number of fuel compacts for 15 MW

class ThermalHydraulicParameters(Parameters):
    """Thermal-hydraulic parameters for the HTGR system."""
    core_inlet_temp: Quantity = Quantity(350, "degC")  # Helium inlet temperature
    core_outlet_temp: Quantity = Quantity(600, "degC")  # Helium outlet temperature
    primary_pressure: Quantity = Quantity(7, "MPa")  # Helium system pressure
    helium_flow_rate_large: Quantity = Quantity(27, "kg/s")  # For 20 MW configuration
    core_pressure_drop: Quantity = Quantity(150, "kPa")  # Across active core
    secondary_max_temp: Quantity = Quantity(570, "degC")  # CO2 maximum temperature
    secondary_pressure: Quantity = Quantity(10, "MPa")  # CO2 system pressure
    co2_flow_rate_large: Quantity = Quantity(96, "kg/s")  # For 20 MW configuration
    co2_inlet_temp: Quantity = Quantity(300, "degC")  # CO2 inlet to heat exchanger

class FuelParameters(Parameters):
    """TRISO fuel parameters for the HTGR system."""
    kernel_material: str = "UO2"  # Uranium dioxide
    kernel_diameter: Quantity = Quantity(500, "micrometer")  # Fuel kernel diameter
    enrichment: Quantity = Quantity(15.5, "wt_percent")  # U-235 enrichment
    buffer_thickness: Quantity = Quantity(95, "micrometer")  # Porous carbon buffer
    ipyc_thickness: Quantity = Quantity(40, "micrometer")  # Inner PyC layer
    sic_thickness: Quantity = Quantity(35, "micrometer")  # Silicon carbide layer
    opyc_thickness: Quantity = Quantity(40, "micrometer")  # Outer PyC layer
    total_diameter: Quantity = Quantity(920, "micrometer")  # Total particle diameter
    failure_temp: Quantity = Quantity(1600, "degC")  # Minimum failure temperature

class HeatExchangerParameters(Parameters):
    """Heat exchanger parameters for the HTGR system."""
    type: str = "Compact Printed Circuit"  # Heat exchanger type
    effectiveness: float = 0.92  # Thermal efficiency
    capacity: Quantity = Quantity(20, "MW")  # Maximum heat transfer capacity
    material: str = "Inconel 617"  # High-temperature alloy
    primary_pressure_drop: Quantity = Quantity(50, "kPa")  # Helium side
    secondary_pressure_drop: Quantity = Quantity(100, "kPa")  # CO2 side
    design_life: Quantity = Quantity(20, "year")  # Expected operational life

class OperationalParameters(Parameters):
    """Operational parameters for the HTGR system."""
    design_life: Quantity = Quantity(20, "year")  # Base design life
    refueling_interval: Quantity = Quantity(5, "year")  # Time between refueling
    refueling_duration: Quantity = Quantity(30, "day")  # Outage duration
    availability: float = 0.90  # Annual availability excluding planned outages
    thermal_efficiency: float = 0.92  # Primary-to-secondary heat transfer efficiency
    parasitic_power_large: Quantity = Quantity(4.3, "MW")  # For 20 MW configuration
    circulator_power_large: Quantity = Quantity(1.5, "MW")  # For 20 MW configuration
    compressor_power_large: Quantity = Quantity(2.8, "MW")  # For 20 MW configuration

class SafetyParameters(Parameters):
    """Safety parameters for the HTGR system."""
    max_accident_temp: Quantity = Quantity(1350, "degC")  # Maximum during accidents
    passive_cooling_duration: Quantity = Quantity(168, "hour")  # Without active systems
    fission_product_retention: float = 0.9999  # Fraction retained in fuel
    grace_period: Quantity = Quantity(72, "hour")  # Time before operator action needed

class EconomicParameters(Parameters):
    """Economic parameters for the HTGR system."""
    lcoh: Quantity = Quantity(45.75, "USD/MWh")  # Levelized cost of heat
    capital_cost: Quantity = Quantity(4500, "USD/kW")  # Per kW thermal
    operational_cost: Quantity = Quantity(12, "USD/MWh")  # Per MWh thermal
    carbon_emissions: Quantity = Quantity(5, "kg/MWh")  # CO2 per MWh thermal
    conventional_emissions: Quantity = Quantity(275, "kg/MWh")  # Average for fossil fuels
    payback_period: Quantity = Quantity(13.5, "year")  # With carbon pricing

class ModularParameters(Parameters):
    """Modular design parameters for the HTGR system."""
    module_length: Quantity = Quantity(12, "m")  # Maximum module length
    module_width: Quantity = Quantity(4.5, "m")  # Maximum module width
    module_height: Quantity = Quantity(5, "m")  # Maximum module height
    factory_assembly: float = 0.85  # Fraction completed in factory
    onsite_assembly: float = 0.15  # Fraction completed on-site
    construction_time: Quantity = Quantity(36, "month")  # From site prep to operation
    site_area: Quantity = Quantity(10000, "m^2")  # Required site area

# Single source of truth for all parameters
CORE_PARAMS = CoreParameters()
THERMAL_PARAMS = ThermalHydraulicParameters()
FUEL_PARAMS = FuelParameters()
HX_PARAMS = HeatExchangerParameters()
OPERATIONAL_PARAMS = OperationalParameters()
SAFETY_PARAMS = SafetyParameters()
ECONOMIC_PARAMS = EconomicParameters()
MODULAR_PARAMS = ModularParameters()

print("HTGR parameters initialized with appropriate units")
