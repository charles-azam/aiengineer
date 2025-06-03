"""
Parameters for thermal energy storage systems.
"""
from pyforge import Parameters, Quantity
from epyr.parameters_materials import MOLTEN_SALT, SOLID_CERAMIC, HIGH_TEMP_CERAMIC, MOLTEN_METAL, PHASE_CHANGE_MATERIAL
from epyr.parameters_industrial_applications import IndustrialApplication, CHEMICAL_APPLICATIONS

class ThermalStorageParameters(Parameters):
    """Define all key parameters for the thermal energy storage system."""
    # Material and application selection
    storage_medium: dict = MOLTEN_SALT                  # Selected storage medium material
    industrial_application: IndustrialApplication = CHEMICAL_APPLICATIONS[0]  # Target application
    
    # Storage capacity parameters
    storage_capacity: Quantity = Quantity(1000, "kWh")  # Total energy storage capacity
    max_power_output: Quantity = Quantity(100, "kW")    # Maximum power output
    max_power_input: Quantity = Quantity(120, "kW")     # Maximum charging power
    
    # Temperature parameters
    max_temperature: Quantity = Quantity(550, "°C")     # Maximum operating temperature
    min_temperature: Quantity = Quantity(250, "°C")     # Minimum operating temperature
    ambient_temperature: Quantity = Quantity(25, "°C")  # Ambient temperature
    max_temp_gradient: Quantity = Quantity(50, "K/m")   # Maximum temperature gradient
    
    # Physical parameters
    storage_volume: Quantity = Quantity(20, "m^3")      # Volume of storage medium
    insulation_thickness: Quantity = Quantity(0.5, "m") # Insulation thickness
    tank_height: Quantity = Quantity(4, "m")            # Height of storage tank
    tank_diameter: Quantity = Quantity(2.5, "m")        # Diameter of storage tank
    aspect_ratio: float = 1.6                           # Height to diameter ratio
    
    # Heat exchanger parameters
    hx_surface_area: Quantity = Quantity(50, "m^2")     # Heat exchanger surface area
    hx_heat_transfer_coeff: Quantity = Quantity(500, "W/(m^2*K)")  # Heat transfer coefficient
    hx_flow_rate_hot: Quantity = Quantity(2.5, "kg/s")  # Hot side flow rate
    hx_flow_rate_cold: Quantity = Quantity(3.0, "kg/s") # Cold side flow rate
    hx_effectiveness: float = 0.85                      # Heat exchanger effectiveness
    
    # Material properties
    storage_medium_density: Quantity = Quantity(1850, "kg/m^3")       # Density of storage medium
    storage_medium_specific_heat: Quantity = Quantity(1.5, "kJ/(kg*K)")  # Specific heat capacity
    thermal_conductivity: Quantity = Quantity(0.8, "W/(m*K)")         # Thermal conductivity
    
    # Operational parameters
    charge_efficiency: float = 0.95                     # Charging efficiency
    discharge_efficiency: float = 0.92                  # Discharging efficiency
    self_discharge_rate: float = 0.02                   # Daily self-discharge rate (fraction)
    design_life: int = 25                               # Design life in years
    cycles_per_year: int = 300                          # Expected cycles per year
    max_ramp_rate: Quantity = Quantity(20, "kW/min")    # Maximum power ramp rate
    min_state_of_charge: float = 0.1                    # Minimum allowable state of charge
    
    # Economic parameters
    capital_cost: Quantity = Quantity(250, "USD/kWh")   # Capital cost per unit energy
    electricity_cost: Quantity = Quantity(0.12, "USD/kWh") # Cost of electricity
    carbon_price: Quantity = Quantity(50, "USD/tCO2")   # Carbon price
    maintenance_cost_annual: float = 0.02               # Annual maintenance cost (fraction of capital)
    
    # Grid integration parameters
    grid_connection_capacity: Quantity = Quantity(150, "kW")  # Grid connection capacity
    response_time: Quantity = Quantity(5, "min")        # Response time to power request
    frequency_regulation_capability: bool = True        # Capability for frequency regulation
    voltage_support_capability: bool = False            # Capability for voltage support

    @property
    def thermal_energy_capacity(self) -> Quantity:
        """Calculate thermal energy capacity based on physical properties."""
        mass = self.storage_volume * self.storage_medium_density
        delta_T = self.max_temperature - self.min_temperature
        return mass * self.storage_medium_specific_heat * delta_T
    
    @property
    def energy_density(self) -> Quantity:
        """Calculate energy density of the storage system."""
        return self.thermal_energy_capacity / self.storage_volume
    
    @property
    def levelized_cost_of_storage(self) -> Quantity:
        """Simplified LCOS calculation."""
        annual_cycles = self.cycles_per_year
        lifetime_cycles = annual_cycles * self.design_life
        lifetime_energy = self.storage_capacity * lifetime_cycles * self.discharge_efficiency
        
        capital = self.capital_cost * self.storage_capacity
        lifetime_maintenance = self.maintenance_cost_annual * capital * self.design_life
        total_cost = capital + lifetime_maintenance
        
        return Quantity(total_cost.magnitude / lifetime_energy.magnitude, "USD/kWh")

# Single source of truth for default configuration
THERMAL_STORAGE_PARAMS = ThermalStorageParameters()

# Alternative configurations for different applications
HIGH_TEMP_INDUSTRIAL_CONFIG = ThermalStorageParameters(
    storage_medium=HIGH_TEMP_CERAMIC,
    max_temperature=Quantity(800, "°C"),
    min_temperature=Quantity(400, "°C"),
    storage_capacity=Quantity(2000, "kWh"),
    max_power_output=Quantity(250, "kW"),
)

GRID_SCALE_CONFIG = ThermalStorageParameters(
    storage_medium=MOLTEN_SALT,
    storage_capacity=Quantity(10000, "kWh"),
    max_power_output=Quantity(1000, "kW"),
    storage_volume=Quantity(200, "m^3"),
    tank_height=Quantity(8, "m"),
    tank_diameter=Quantity(5.6, "m"),
    grid_connection_capacity=Quantity(1200, "kW"),
)

PHASE_CHANGE_CONFIG = ThermalStorageParameters(
    storage_medium=PHASE_CHANGE_MATERIAL,
    max_temperature=Quantity(350, "°C"),
    min_temperature=Quantity(300, "°C"),
    storage_capacity=Quantity(500, "kWh"),
    thermal_conductivity=Quantity(2.5, "W/(m*K)"),
)

# Operational mode configurations
FAST_RESPONSE_MODE = {
    "max_ramp_rate": Quantity(50, "kW/min"),
    "response_time": Quantity(1, "min"),
    "min_state_of_charge": 0.3,
}

ENERGY_SAVING_MODE = {
    "max_power_output": Quantity(80, "kW"),
    "self_discharge_rate": 0.015,
}

PEAK_POWER_MODE = {
    "max_power_output": Quantity(150, "kW"),
    "discharge_efficiency": 0.88,
    "min_state_of_charge": 0.2,
}

# Print debug information
print("Thermal storage parameters loaded successfully")
from pyforge import Parameters, Quantity

class ThermalStorageParameters(Parameters):
    """Define all the key parameters for thermal energy storage system."""
    storage_capacity: Quantity = Quantity(100, "MWh")
    max_power_output: Quantity = Quantity(10, "MW")
    design_life: int = 25  # years
    cycles_per_year: int = 365
    charge_efficiency: float = 0.95
    discharge_efficiency: float = 0.90
    min_temperature: Quantity = Quantity(300, "°C")
    max_temperature: Quantity = Quantity(800, "°C")
    grid_frequency: Quantity = Quantity(50, "Hz")
    grid_voltage: Quantity = Quantity(11, "kV")
    target_lcoe: Quantity = Quantity(0.10, "USD/kWh")
    max_capital_cost: Quantity = Quantity(50, "USD/kWh")
    min_availability: float = 98.0
    mtbf: Quantity = Quantity(8760, "hour")
    min_energy_density: Quantity = Quantity(0.5, "MWh/m^3")
    container_thickness: Quantity = Quantity(50, "mm")
    insulation_thickness: Quantity = Quantity(300, "mm")
    max_insulation_conductivity: Quantity = Quantity(0.05, "W/(m*K)")
    max_heat_loss: Quantity = Quantity(1, "%/day")
    max_pressure_drop: Quantity = Quantity(0.5, "bar")
    heat_exchanger_efficiency: float = 0.90
    max_input_temperature: Quantity = Quantity(850, "°C")
    min_output_temperature: Quantity = Quantity(250, "°C")
    nominal_flow_rate: Quantity = Quantity(50, "kg/s")
    max_fluid_temperature: Quantity = Quantity(820, "°C")
    max_control_response_time: Quantity = Quantity(1, "s")
    data_logging_frequency: Quantity = Quantity(1, "Hz")
    temperature_accuracy: Quantity = Quantity(1, "°C")
    pressure_accuracy: Quantity = Quantity(0.1, "bar")
    flow_accuracy: Quantity = Quantity(1, "%")
    optimization_improvement: Quantity = Quantity(5, "%")
    power_conversion_efficiency: float = 0.40
    frequency_tolerance: Quantity = Quantity(0.1, "Hz")
    ramp_rate: Quantity = Quantity(5, "%/min")
    turbine_efficiency: float = 0.85
    min_turbine_load: Quantity = Quantity(20, "%")
    generator_efficiency: float = 0.98
    min_power_factor: float = 0.95
    temperature_control_tolerance: Quantity = Quantity(2, "°C")
    max_distribution_losses: Quantity = Quantity(2, "%")
    max_pipe_heat_loss: Quantity = Quantity(50, "W/m")
    distribution_pressure: Quantity = Quantity(10, "bar")
    min_process_temperature: Quantity = Quantity(100, "°C")
    max_process_temperature: Quantity = Quantity(750, "°C")
    max_temp_change_rate: Quantity = Quantity(5, "°C/min")

# Single source of truth
THERMAL_STORAGE_PARAMS = ThermalStorageParameters()
