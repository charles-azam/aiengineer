"""
Industrial heat applications and their requirements.

This module defines various industrial processes that require high-temperature
thermal energy, their temperature ranges, energy consumption profiles, and
other relevant parameters for thermal energy storage system design.
"""

from pyforge import Parameters
from epyr.tools_units import Quantity
from enum import Enum, auto
from typing import List, Dict
from dataclasses import dataclass


class HeatProfile(Enum):
    """Types of heat demand profiles in industrial applications."""
    CONSTANT = auto()      # Continuous, steady heat demand
    BATCH = auto()         # Intermittent heat demand for batch processes
    VARIABLE = auto()      # Fluctuating heat demand based on production
    SEASONAL = auto()      # Heat demand varies by season
    CYCLIC = auto()        # Regular pattern of high and low demand


@dataclass
class TemperatureRange:
    """Temperature range for an industrial process."""
    min: Quantity  # Minimum temperature
    max: Quantity  # Maximum temperature


class IndustrialApplication(Parameters):
    """Industrial process heat application parameters."""
    name: str                          # Process name
    industry: str                      # Industry sector
    temperature_range: TemperatureRange  # Temperature range required
    heat_profile: HeatProfile          # Heat demand profile type
    energy_intensity: Quantity         # Energy per unit of production
    current_heat_source: str           # Typically fossil fuel based
    emission_factor: Quantity          # CO2 emissions per unit of heat
    potential_energy_savings: float    # Potential savings with TES (fraction)


# Food Processing Industry Applications
FOOD_PASTEURIZATION = IndustrialApplication(
    name="Pasteurization",
    industry="Food Processing",
    temperature_range=TemperatureRange(
        min=Quantity(72, "°C"),
        max=Quantity(95, "°C")
    ),
    heat_profile=HeatProfile.BATCH,
    energy_intensity=Quantity(0.3, "kWh/kg"),
    current_heat_source="Natural Gas Boilers",
    emission_factor=Quantity(0.2, "kg_CO2_per_kWh"),
    potential_energy_savings=0.25
)

FOOD_DRYING = IndustrialApplication(
    name="Food Drying",
    industry="Food Processing",
    temperature_range=TemperatureRange(
        min=Quantity(70, "°C"),
        max=Quantity(150, "°C")
    ),
    heat_profile=HeatProfile.BATCH,
    energy_intensity=Quantity(0.8, "kWh/kg"),
    current_heat_source="Natural Gas / Electric",
    emission_factor=Quantity(0.22, "kg_CO2_per_kWh"),
    potential_energy_savings=0.30
)

FOOD_BAKING = IndustrialApplication(
    name="Baking",
    industry="Food Processing",
    temperature_range=TemperatureRange(
        min=Quantity(150, "°C"),
        max=Quantity(300, "°C")
    ),
    heat_profile=HeatProfile.BATCH,
    energy_intensity=Quantity(0.6, "kWh/kg"),
    current_heat_source="Natural Gas Ovens",
    emission_factor=Quantity(0.25, "kg_CO2_per_kWh"),
    potential_energy_savings=0.20
)

# Chemical Industry Applications
CHEMICAL_DISTILLATION = IndustrialApplication(
    name="Distillation",
    industry="Chemical",
    temperature_range=TemperatureRange(
        min=Quantity(100, "°C"),
        max=Quantity(200, "°C")
    ),
    heat_profile=HeatProfile.CONSTANT,
    energy_intensity=Quantity(1.2, "kWh/kg"),
    current_heat_source="Steam from Natural Gas",
    emission_factor=Quantity(0.3, "kg_CO2_per_kWh"),
    potential_energy_savings=0.35
)

CHEMICAL_REACTOR_HEATING = IndustrialApplication(
    name="Reactor Heating",
    industry="Chemical",
    temperature_range=TemperatureRange(
        min=Quantity(150, "°C"),
        max=Quantity(350, "°C")
    ),
    heat_profile=HeatProfile.VARIABLE,
    energy_intensity=Quantity(1.5, "kWh/kg"),
    current_heat_source="Natural Gas / Oil",
    emission_factor=Quantity(0.35, "kg_CO2_per_kWh"),
    potential_energy_savings=0.30
)

# Metal Processing Applications
METAL_HEAT_TREATMENT = IndustrialApplication(
    name="Heat Treatment",
    industry="Metal Processing",
    temperature_range=TemperatureRange(
        min=Quantity(600, "°C"),
        max=Quantity(900, "°C")
    ),
    heat_profile=HeatProfile.BATCH,
    energy_intensity=Quantity(0.9, "kWh/kg"),
    current_heat_source="Natural Gas Furnaces",
    emission_factor=Quantity(0.4, "kg_CO2_per_kWh"),
    potential_energy_savings=0.25
)

ALUMINUM_MELTING = IndustrialApplication(
    name="Aluminum Melting",
    industry="Metal Processing",
    temperature_range=TemperatureRange(
        min=Quantity(650, "°C"),
        max=Quantity(750, "°C")
    ),
    heat_profile=HeatProfile.BATCH,
    energy_intensity=Quantity(1.1, "kWh/kg"),
    current_heat_source="Natural Gas / Electric",
    emission_factor=Quantity(0.38, "kg_CO2_per_kWh"),
    potential_energy_savings=0.28
)

# Paper Industry Applications
PAPER_DRYING = IndustrialApplication(
    name="Paper Drying",
    industry="Paper",
    temperature_range=TemperatureRange(
        min=Quantity(100, "°C"),
        max=Quantity(180, "°C")
    ),
    heat_profile=HeatProfile.CONSTANT,
    energy_intensity=Quantity(1.3, "kWh/kg"),
    current_heat_source="Steam from Natural Gas",
    emission_factor=Quantity(0.28, "kg_CO2_per_kWh"),
    potential_energy_savings=0.32
)

# Cement Industry Applications
CEMENT_KILN = IndustrialApplication(
    name="Cement Kiln",
    industry="Cement Manufacturing",
    temperature_range=TemperatureRange(
        min=Quantity(1300, "°C"),
        max=Quantity(1450, "°C")
    ),
    heat_profile=HeatProfile.CONSTANT,
    energy_intensity=Quantity(1.6, "kWh/kg"),
    current_heat_source="Coal / Petroleum Coke",
    emission_factor=Quantity(0.8, "kg_CO2_per_kWh"),
    potential_energy_savings=0.15
)

# Textile Industry Applications
TEXTILE_DYEING = IndustrialApplication(
    name="Textile Dyeing",
    industry="Textile",
    temperature_range=TemperatureRange(
        min=Quantity(80, "°C"),
        max=Quantity(140, "°C")
    ),
    heat_profile=HeatProfile.BATCH,
    energy_intensity=Quantity(0.7, "kWh/kg"),
    current_heat_source="Steam from Natural Gas",
    emission_factor=Quantity(0.27, "kg_CO2_per_kWh"),
    potential_energy_savings=0.28
)

# Group applications by industry for easier access
FOOD_APPLICATIONS = [FOOD_PASTEURIZATION, FOOD_DRYING, FOOD_BAKING]
CHEMICAL_APPLICATIONS = [CHEMICAL_DISTILLATION, CHEMICAL_REACTOR_HEATING]
METAL_APPLICATIONS = [METAL_HEAT_TREATMENT, ALUMINUM_MELTING]
PAPER_APPLICATIONS = [PAPER_DRYING]
CEMENT_APPLICATIONS = [CEMENT_KILN]
TEXTILE_APPLICATIONS = [TEXTILE_DYEING]

# All industrial applications
ALL_INDUSTRIAL_APPLICATIONS = (
    FOOD_APPLICATIONS + 
    CHEMICAL_APPLICATIONS + 
    METAL_APPLICATIONS + 
    PAPER_APPLICATIONS + 
    CEMENT_APPLICATIONS + 
    TEXTILE_APPLICATIONS
)

print("Industrial applications parameters loaded")
