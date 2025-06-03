"""
Parameters for modular design, manufacturing, and installation of HTGR systems.
Defines key parameters for modular High-Temperature Gas-cooled Reactor implementation.
"""

from pyforge import Parameters, Quantity, UREG
from reactor import UREG

class ModulePhysicalParameters(Parameters):
    """Physical dimensions and weights for standard reactor modules."""
    # Core module dimensions
    core_module_length: Quantity = Quantity(12, "m")
    core_module_width: Quantity = Quantity(4.5, "m")
    core_module_height: Quantity = Quantity(5, "m")
    core_module_weight: Quantity = Quantity(120, "tonne")
    
    # Heat exchanger module dimensions
    hx_module_length: Quantity = Quantity(8, "m")
    hx_module_width: Quantity = Quantity(4, "m")
    hx_module_height: Quantity = Quantity(4, "m")
    hx_module_weight: Quantity = Quantity(75, "tonne")
    
    # Control system module dimensions
    control_module_length: Quantity = Quantity(6, "m")
    control_module_width: Quantity = Quantity(3, "m")
    control_module_height: Quantity = Quantity(3, "m")
    control_module_weight: Quantity = Quantity(25, "tonne")
    
    # Transport limitations
    max_road_transport_weight: Quantity = Quantity(150, "tonne")
    max_road_transport_width: Quantity = Quantity(5, "m")
    max_road_transport_height: Quantity = Quantity(5.5, "m")
    max_road_transport_length: Quantity = Quantity(30, "m")


class FactoryAssemblyParameters(Parameters):
    """Parameters related to factory assembly of modules."""
    factory_floor_space_per_module: Quantity = Quantity(500, "m^2")
    assembly_time_core_module: Quantity = Quantity(6, "month")
    assembly_time_hx_module: Quantity = Quantity(3, "month")
    assembly_time_control_module: Quantity = Quantity(2, "month")
    quality_control_time: Quantity = Quantity(1, "month")
    factory_testing_time: Quantity = Quantity(2, "month")
    parallel_module_capacity: int = 4  # Number of modules that can be assembled in parallel
    skilled_labor_per_module: int = 25  # Workers needed per module


class SiteInstallationParameters(Parameters):
    """Parameters for on-site installation requirements."""
    site_area_requirement: Quantity = Quantity(10000, "m^2")  # Total site area
    concrete_foundation_thickness: Quantity = Quantity(2, "m")
    foundation_curing_time: Quantity = Quantity(28, "day")
    crane_capacity_required: Quantity = Quantity(200, "tonne")
    module_installation_time: Quantity = Quantity(2, "week")  # Per module
    system_integration_time: Quantity = Quantity(3, "month")
    commissioning_time: Quantity = Quantity(2, "month")
    site_preparation_time: Quantity = Quantity(6, "month")


class ModuleConnectionParameters(Parameters):
    """Specifications for connections between modules."""
    helium_pipe_diameter: Quantity = Quantity(0.5, "m")
    helium_connection_pressure: Quantity = Quantity(7, "MPa")
    co2_pipe_diameter: Quantity = Quantity(0.4, "m")
    co2_connection_pressure: Quantity = Quantity(5, "MPa")
    electrical_connection_voltage: Quantity = Quantity(480, "V")
    electrical_connection_phases: int = 3
    data_connection_bandwidth: Quantity = Quantity(10, "Gbit/s")
    connection_tolerance: Quantity = Quantity(5, "mm")
    seismic_isolation_rating: Quantity = Quantity(8, "dimensionless")  # Seismic rating (dimensionless)


class ConstructionTimelineParameters(Parameters):
    """Timeline parameters for construction and deployment."""
    site_assessment_time: Quantity = Quantity(3, "month")
    permitting_time: Quantity = Quantity(12, "month")
    site_preparation_time: Quantity = Quantity(6, "month")
    foundation_construction_time: Quantity = Quantity(4, "month")
    module_delivery_time: Quantity = Quantity(1, "month")  # Per module
    module_installation_time: Quantity = Quantity(2, "week")  # Per module
    system_integration_time: Quantity = Quantity(3, "month")
    testing_time: Quantity = Quantity(2, "month")
    commissioning_time: Quantity = Quantity(1, "month")
    total_project_timeline_10MW: Quantity = Quantity(30, "month")
    total_project_timeline_20MW: Quantity = Quantity(36, "month")


class PowerScalingParameters(Parameters):
    """Parameters for scaling between different power levels."""
    # 10 MW configuration
    modules_10MW: int = 3  # Core + HX + Control
    core_modules_10MW: int = 1
    hx_modules_10MW: int = 1
    control_modules_10MW: int = 1
    helium_flow_rate_10MW: Quantity = Quantity(15, "kilogram/second")
    co2_flow_rate_10MW: Quantity = Quantity(25, "kilogram/second")
    
    # 15 MW configuration
    modules_15MW: int = 4  # Core + 2 HX + Control
    core_modules_15MW: int = 1
    hx_modules_15MW: int = 2
    control_modules_15MW: int = 1
    helium_flow_rate_15MW: Quantity = Quantity(22.5, "kilogram/second")
    co2_flow_rate_15MW: Quantity = Quantity(37.5, "kilogram/second")
    
    # 20 MW configuration
    modules_20MW: int = 5  # Core + 3 HX + Control
    core_modules_20MW: int = 1
    hx_modules_20MW: int = 3
    control_modules_20MW: int = 1
    helium_flow_rate_20MW: Quantity = Quantity(30, "kilogram/second")
    co2_flow_rate_20MW: Quantity = Quantity(50, "kilogram/second")


class StandardizationParameters(Parameters):
    """Parameters for component standardization across modules."""
    standard_bolt_sizes: list = [8, 10, 12, 16, 20]  # mm
    standard_pipe_diameters: list = [100, 200, 300, 400, 500]  # mm
    standard_electrical_connectors: list = ["Type A", "Type B", "Type C"]
    standard_sensor_interfaces: list = ["4-20mA", "0-10V", "HART", "Modbus"]
    standard_control_protocols: list = ["Modbus TCP", "OPC UA", "Profinet"]
    standard_insulation_thickness: Quantity = Quantity(200, "mm")
    standard_valve_types: list = ["Gate", "Globe", "Check", "Ball", "Butterfly"]
    standard_gasket_materials: list = ["Graphite", "PTFE", "Metal", "Spiral Wound"]
    standard_weld_procedures: list = ["GTAW", "SMAW", "FCAW"]


class IndustrialInterfaceParameters(Parameters):
    """Parameters for interfaces with existing industrial systems."""
    # Steam interface
    steam_output_temperature: Quantity = Quantity(550, "degC")
    steam_output_pressure: Quantity = Quantity(10, "MPa")
    steam_flow_rate_10MW: Quantity = Quantity(4, "kilogram/second")
    steam_flow_rate_20MW: Quantity = Quantity(8, "kilogram/second")
    
    # Hot air interface
    hot_air_output_temperature: Quantity = Quantity(500, "degC")
    hot_air_pressure: Quantity = Quantity(0.5, "MPa")
    hot_air_flow_rate_10MW: Quantity = Quantity(12, "kilogram/second")
    hot_air_flow_rate_20MW: Quantity = Quantity(24, "kilogram/second")
    
    # Thermal oil interface
    thermal_oil_output_temperature: Quantity = Quantity(400, "degC")
    thermal_oil_return_temperature: Quantity = Quantity(250, "degC")
    thermal_oil_flow_rate_10MW: Quantity = Quantity(50, "kilogram/second")
    thermal_oil_flow_rate_20MW: Quantity = Quantity(100, "kilogram/second")
    
    # Standard connection types
    steam_connection_type: str = "ASME B16.5 Class 600 Flange"
    air_connection_type: str = "ASME B16.5 Class 300 Flange"
    oil_connection_type: str = "ASME B16.5 Class 400 Flange"


class SitePreparationParameters(Parameters):
    """Parameters for site preparation requirements."""
    minimum_soil_bearing_capacity: Quantity = Quantity(200, "kPa")
    minimum_distance_to_population: Quantity = Quantity(800, "m")
    minimum_distance_to_water_source: Quantity = Quantity(100, "m")
    maximum_groundwater_level: Quantity = Quantity(10, "m")  # Below surface
    minimum_access_road_width: Quantity = Quantity(8, "m")
    minimum_electrical_supply: Quantity = Quantity(2, "MVA")
    backup_power_requirement: Quantity = Quantity(500, "kW")
    cooling_water_requirement_10MW: Quantity = Quantity(50, "meter^3/second")
    cooling_water_requirement_20MW: Quantity = Quantity(100, "meter^3/second")
    security_perimeter_requirement: Quantity = Quantity(100, "m")


class RegulatoryComplianceParameters(Parameters):
    """Parameters related to regulatory compliance."""
    radiation_exclusion_zone: Quantity = Quantity(300, "m")
    max_worker_annual_dose: Quantity = Quantity(20, "mSv")
    max_public_annual_dose: Quantity = Quantity(1, "mSv")
    containment_leak_rate_limit: Quantity = Quantity(0.1, "percent/day")
    emergency_planning_zone: Quantity = Quantity(400, "m")
    seismic_design_basis: Quantity = Quantity(0.3, "g")  # Peak ground acceleration in g units
    aircraft_impact_protection: bool = True
    cyber_security_level: str = "Level 4"  # Based on IEC 62443
    quality_assurance_standard: str = "10 CFR 50 Appendix B"
    design_life: Quantity = Quantity(20, "year")


# Single source of truth instances
MODULE_PHYSICAL_PARAMS = ModulePhysicalParameters()
FACTORY_ASSEMBLY_PARAMS = FactoryAssemblyParameters()
SITE_INSTALLATION_PARAMS = SiteInstallationParameters()
MODULE_CONNECTION_PARAMS = ModuleConnectionParameters()
CONSTRUCTION_TIMELINE_PARAMS = ConstructionTimelineParameters()
POWER_SCALING_PARAMS = PowerScalingParameters()
STANDARDIZATION_PARAMS = StandardizationParameters()
INDUSTRIAL_INTERFACE_PARAMS = IndustrialInterfaceParameters()
SITE_PREPARATION_PARAMS = SitePreparationParameters()
REGULATORY_COMPLIANCE_PARAMS = RegulatoryComplianceParameters()

# Print key parameters for verification
print(f"Core module dimensions: {MODULE_PHYSICAL_PARAMS.core_module_length} x {MODULE_PHYSICAL_PARAMS.core_module_width} x {MODULE_PHYSICAL_PARAMS.core_module_height}")
print(f"10 MW configuration: {POWER_SCALING_PARAMS.modules_10MW} modules total")
print(f"20 MW configuration: {POWER_SCALING_PARAMS.modules_20MW} modules total")
print(f"Steam output temperature: {INDUSTRIAL_INTERFACE_PARAMS.steam_output_temperature}")
print(f"Total project timeline (10 MW): {CONSTRUCTION_TIMELINE_PARAMS.total_project_timeline_10MW}")
print(f"Reactor design life: {REGULATORY_COMPLIANCE_PARAMS.design_life}")
