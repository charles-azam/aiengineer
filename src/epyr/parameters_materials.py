"""
Thermal storage materials properties for different temperature ranges.

This module defines various thermal storage materials and their properties
for use in thermal energy storage system design and simulation.
"""

from pyforge import Parameters
from epyr.tools_units import Quantity

class MaterialProperties(Parameters):
    """
    Properties of thermal storage materials.
    
    Attributes:
        name: Material name
        density: Mass per unit volume
        specific_heat: Heat capacity per unit mass
        thermal_conductivity: Heat transfer coefficient
        max_temperature: Maximum safe operating temperature
        min_temperature: Minimum effective operating temperature
        cost_per_kg: Material cost per kilogram
        energy_density: Energy storage capacity per unit volume
        melting_point: Melting point temperature (if applicable)
        latent_heat: Latent heat of fusion (if applicable)
        specific_heat_solid: Specific heat in solid phase (if applicable)
        specific_heat_liquid: Specific heat in liquid phase (if applicable)
        composition: Material composition description
    """
    name: str                      # Material name
    density: Quantity              # kg/m³
    specific_heat: Quantity        # J/(kg·K)
    thermal_conductivity: Quantity # W/(m·K)
    max_temperature: Quantity      # °C
    min_temperature: Quantity      # °C
    cost_per_kg: Quantity          # USD/kg
    energy_density: Quantity       # J/m³
    melting_point: float = None    # °C
    latent_heat: Quantity = None   # J/kg
    specific_heat_solid: Quantity = None  # J/(kg·K)
    specific_heat_liquid: Quantity = None # J/(kg·K)
    composition: str = ""          # Material composition

# Solar salt (NaNO3-KNO3 mixture)
MOLTEN_SALT = MaterialProperties(
    name="Solar Salt (NaNO3-KNO3)",
    density=Quantity(1794, "kg/m^3"),              # at 400°C
    specific_heat=Quantity(1495, "J/(kg*K)"),      # average value
    thermal_conductivity=Quantity(0.53, "W/(m*K)"),
    max_temperature=Quantity(565, "°C"),
    min_temperature=Quantity(290, "°C"),           # melting point ~240°C with safety margin
    cost_per_kg=Quantity(0.5, "USD/kg"),
    energy_density=Quantity(0.8, "GJ/m^3"),        # calculated from density and specific heat
    melting_point=240,                             # °C
    composition="60% NaNO3, 40% KNO3"
)

# Concrete thermal storage
SOLID_CERAMIC = MaterialProperties(
    name="High-Density Concrete",
    density=Quantity(2200, "kg/m^3"),
    specific_heat=Quantity(850, "J/(kg*K)"),
    thermal_conductivity=Quantity(1.5, "W/(m*K)"),
    max_temperature=Quantity(500, "°C"),
    min_temperature=Quantity(20, "°C"),
    cost_per_kg=Quantity(0.1, "USD/kg"),
    energy_density=Quantity(0.4, "GJ/m^3")
)

# Alumina ceramic
HIGH_TEMP_CERAMIC = MaterialProperties(
    name="Alumina Ceramic",
    density=Quantity(3900, "kg/m^3"),
    specific_heat=Quantity(880, "J/(kg*K)"),
    thermal_conductivity=Quantity(30, "W/(m*K)"),
    max_temperature=Quantity(1600, "°C"),
    min_temperature=Quantity(20, "°C"),
    cost_per_kg=Quantity(1.5, "USD/kg"),
    energy_density=Quantity(0.9, "GJ/m^3")
)

# Molten aluminum
MOLTEN_METAL = MaterialProperties(
    name="Molten Aluminum",
    density=Quantity(2375, "kg/m^3"),              # at 700°C
    specific_heat=Quantity(1177, "J/(kg*K)"),
    thermal_conductivity=Quantity(94, "W/(m*K)"),
    max_temperature=Quantity(900, "°C"),
    min_temperature=Quantity(660, "°C"),           # melting point
    cost_per_kg=Quantity(2.0, "USD/kg"),
    energy_density=Quantity(1.2, "GJ/m^3"),
    melting_point=660                              # °C
)

# Industrial phase change material (salt based)
PHASE_CHANGE_MATERIAL = MaterialProperties(
    name="Salt-Based PCM",
    density=Quantity(2000, "kg/m^3"),
    specific_heat=Quantity(1500, "J/(kg*K)"),      # average value
    thermal_conductivity=Quantity(0.6, "W/(m*K)"),
    max_temperature=Quantity(450, "°C"),
    min_temperature=Quantity(300, "°C"),           # phase transition around 320-340°C
    cost_per_kg=Quantity(3.5, "USD/kg"),
    energy_density=Quantity(1.5, "GJ/m^3"),        # includes latent heat of fusion
    melting_point=330,                             # °C
    latent_heat=Quantity(150000, "J/kg"),          # approximate value
    specific_heat_solid=Quantity(1400, "J/(kg*K)"),
    specific_heat_liquid=Quantity(1600, "J/(kg*K)")
)

print("Thermal Storage Materials Properties loaded")
