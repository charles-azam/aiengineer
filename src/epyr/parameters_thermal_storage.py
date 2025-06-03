"""
Parameters for thermal energy storage systems.
"""
from pyforge import Parameters
from epyr.tools_units import Quantity

# Define material properties
class MaterialProperties(Parameters):
    """Material properties for thermal storage."""
    name: str = "Generic Material"
    density: Quantity = Quantity(1000, "kg/m^3")
    specific_heat: Quantity = Quantity(1.0, "kJ/(kg*K)")
    thermal_conductivity: Quantity = Quantity(1.0, "W/(m*K)")
    max_temperature: Quantity = Quantity(500, "°C")
    min_temperature: Quantity = Quantity(200, "°C")
    cost_per_kg: Quantity = Quantity(1.0, "USD_per_kg")
    
    @property
    def energy_density(self) -> Quantity:
        """Calculate energy density in kWh/m³."""
        temp_diff = self.max_temperature - self.min_temperature
        # Convert from kJ to kWh by dividing by 3600
        return self.density * self.specific_heat * temp_diff / Quantity(3600, "s/h")

# Define material options
MOLTEN_SALT = MaterialProperties(
    name="Molten Salt",
    density=Quantity(1850, "kg/m^3"),
    specific_heat=Quantity(1.5, "kJ/(kg*K)"),
    thermal_conductivity=Quantity(0.5, "W/(m*K)"),
    max_temperature=Quantity(550, "°C"),
    min_temperature=Quantity(250, "°C"),
    cost_per_kg=Quantity(0.5, "USD/kg")
)

CONCRETE = MaterialProperties(
    name="High-Temperature Concrete",
    density=Quantity(2200, "kg/m^3"),
    specific_heat=Quantity(0.85, "kJ/(kg*K)"),
    thermal_conductivity=Quantity(1.5, "W/(m*K)"),
    max_temperature=Quantity(500, "°C"),
    min_temperature=Quantity(100, "°C"),
    cost_per_kg=Quantity(0.1, "USD/kg")
)

CERAMIC = MaterialProperties(
    name="Ceramic Bricks",
    density=Quantity(3000, "kg/m^3"),
    specific_heat=Quantity(1.0, "kJ/(kg*K)"),
    thermal_conductivity=Quantity(2.0, "W/(m*K)"),
    max_temperature=Quantity(800, "°C"),
    min_temperature=Quantity(200, "°C"),
    cost_per_kg=Quantity(0.8, "USD/kg")
)

PHASE_CHANGE = MaterialProperties(
    name="Phase Change Material",
    density=Quantity(1600, "kg/m^3"),
    specific_heat=Quantity(2.0, "kJ/(kg*K)"),
    thermal_conductivity=Quantity(0.6, "W/(m*K)"),
    max_temperature=Quantity(350, "°C"),
    min_temperature=Quantity(300, "°C"),  # Narrow range due to phase change
    cost_per_kg=Quantity(3.0, "USD/kg")
)

# Define industrial applications
class IndustrialApplication(Parameters):
    """Industrial application parameters."""
    name: str = "Generic Process"
    temperature_range: dict = {"min": Quantity(100, "°C"), "max": Quantity(300, "°C")}
    energy_intensity: Quantity = Quantity(100, "kWh/tonne")
    potential_energy_savings: float = 0.15  # 15% potential savings
    
# Define specific industrial applications
CHEMICAL_APPLICATION = IndustrialApplication(
    name="Chemical Processing",
    temperature_range={"min": Quantity(200, "°C"), "max": Quantity(500, "°C")},
    energy_intensity=Quantity(250, "kWh/tonne"),
    potential_energy_savings=0.20
)

STEEL_APPLICATION = IndustrialApplication(
    name="Steel Manufacturing",
    temperature_range={"min": Quantity(400, "°C"), "max": Quantity(800, "°C")},
    energy_intensity=Quantity(350, "kWh/tonne"),
    potential_energy_savings=0.25
)

FOOD_APPLICATION = IndustrialApplication(
    name="Food Processing",
    temperature_range={"min": Quantity(80, "°C"), "max": Quantity(200, "°C")},
    energy_intensity=Quantity(120, "kWh/tonne"),
    potential_energy_savings=0.15
)

CEMENT_APPLICATION = IndustrialApplication(
    name="Cement Production",
    temperature_range={"min": Quantity(500, "°C"), "max": Quantity(700, "°C")},
    energy_intensity=Quantity(400, "kWh/tonne"),
    potential_energy_savings=0.18
)

# Group applications for easy access
INDUSTRIAL_APPLICATIONS = [CHEMICAL_APPLICATION, STEEL_APPLICATION, FOOD_APPLICATION, CEMENT_APPLICATION]

class ThermalStorageParameters(Parameters):
    """Define all key parameters for the thermal energy storage system."""
    # Material and application selection
    storage_medium: MaterialProperties = MOLTEN_SALT    # Selected storage medium material
    industrial_application: IndustrialApplication = CHEMICAL_APPLICATION  # Target application
    
    # Storage capacity parameters
    storage_capacity: Quantity = Quantity(1000, "kWh")  # Total energy storage capacity
    max_power_output: Quantity = Quantity(100, "kW")    # Maximum power output
    max_power_input: Quantity = Quantity(120, "kW")     # Maximum charging power
    
    # Temperature parameters
    max_temperature: Quantity = Quantity(550, "°C")     # Maximum operating temperature
    min_temperature: Quantity = Quantity(250, "°C")     # Minimum operating temperature
    ambient_temperature: Quantity = Quantity(25, "°C")  # Ambient temperature
    
    # Physical parameters
    storage_volume: Quantity = Quantity(20, "m^3")      # Volume of storage medium
    insulation_thickness: Quantity = Quantity(0.5, "m") # Insulation thickness
    surface_area: Quantity = Quantity(50, "m^2")        # Surface area of storage tank
    surface_emissivity: float = 0.8                     # Surface emissivity for radiation
    insulation_conductivity: Quantity = Quantity(0.05, "W/(m*K)") # Insulation thermal conductivity
    
    # Material properties
    storage_medium_density: Quantity = Quantity(1850, "kg/m^3")       # Density of storage medium
    storage_medium_specific_heat: Quantity = Quantity(1.5, "kJ/(kg*K)")  # Specific heat capacity
    
    # Operational parameters
    charge_efficiency: float = 0.95                     # Charging efficiency
    discharge_efficiency: float = 0.92                  # Discharging efficiency
    self_discharge_rate: float = 0.02                   # Daily self-discharge rate (fraction)
    design_life: int = 25                               # Design life in years
    cycles_per_year: int = 300                          # Expected cycles per year
    
    # Economic parameters
    capital_cost: Quantity = Quantity(200000, "USD")    # Initial capital cost
    operational_cost_per_year: Quantity = Quantity(5000, "USD/year")  # Annual operational cost
    energy_cost_savings: Quantity = Quantity(0.1, "USD_per_kWh")  # Cost savings per kWh

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
    def annual_energy_savings(self) -> Quantity:
        """Calculate annual energy savings in kWh."""
        return self.storage_capacity * self.cycles_per_year * self.discharge_efficiency
    
    @property
    def annual_cost_savings(self) -> Quantity:
        """Calculate annual cost savings in USD."""
        return self.annual_energy_savings * self.energy_cost_savings
    
    @property
    def simple_payback_period(self) -> float:
        """Calculate simple payback period in years."""
        annual_savings = self.annual_cost_savings.magnitude - self.operational_cost_per_year.magnitude
        return self.capital_cost.magnitude / annual_savings if annual_savings > 0 else float('inf')
    
    @property
    def levelized_cost_of_storage(self) -> Quantity:
        """Calculate levelized cost of storage in USD/kWh."""
        lifetime_energy = self.annual_energy_savings * self.design_life
        lifetime_cost = self.capital_cost + (self.operational_cost_per_year * self.design_life)
        return lifetime_cost / lifetime_energy if lifetime_energy.magnitude > 0 else Quantity(float('inf'), "USD_per_kWh")

# Single source of truth for default configuration
THERMAL_STORAGE_PARAMS = ThermalStorageParameters()

print("Thermal storage parameters loaded")
print(f"Available storage media: Molten Salt, Concrete, Ceramic, Phase Change Material")
print(f"Available applications: Chemical Processing, Steel Manufacturing, Food Processing, Cement Production")
