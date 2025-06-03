"""
Unit registry with monetary units and custom units for thermal energy storage.

This module creates a unit registry with additional units needed for thermal
energy storage system design, including monetary units, energy density units,
and other compound units.
"""

from pint import UnitRegistry
from pyforge import Quantity as PyforgeQuantity

# Create a new unit registry
UNIT_REGISTRY = UnitRegistry()

# Create a Quantity class that uses our registry by default
class Quantity(PyforgeQuantity):
    """Quantity class that uses the EPYR unit registry by default."""
    pass

# Set the registry for our Quantity class
Quantity._REGISTRY = UNIT_REGISTRY

# Register base monetary units
UNIT_REGISTRY.define('USD = [currency] = dollar')
UNIT_REGISTRY.define('EUR = 1.09 * USD = euro')
UNIT_REGISTRY.define('GBP = 1.27 * USD = pound')

# Register energy density units
UNIT_REGISTRY.define('energy_density = joule / meter^3')
UNIT_REGISTRY.define('kWh_per_m3 = kilowatt_hour / meter^3 = energy_density')
UNIT_REGISTRY.define('MWh_per_m3 = megawatt_hour / meter^3 = energy_density')
UNIT_REGISTRY.define('GJ_per_m3 = gigajoule / meter^3 = energy_density')

# Register monetary derived units for energy
UNIT_REGISTRY.define('USD_per_kWh = USD / kilowatt_hour')
UNIT_REGISTRY.define('USD_per_MWh = USD / megawatt_hour')
UNIT_REGISTRY.define('USD_per_GJ = USD / gigajoule')

# Register power cost units
UNIT_REGISTRY.define('USD_per_kW = USD / kilowatt')
UNIT_REGISTRY.define('USD_per_MW = USD / megawatt')

# Register volume-specific cost units
UNIT_REGISTRY.define('USD_per_m3 = USD / meter^3')
UNIT_REGISTRY.define('EUR_per_m3 = EUR / meter^3')

# Register mass-specific cost units
UNIT_REGISTRY.define('USD_per_kg = USD / kilogram')
UNIT_REGISTRY.define('USD_per_tonne = USD / tonne')

# Register temperature gradient units
UNIT_REGISTRY.define('kelvin_per_meter = kelvin / meter = temperature_gradient')
UNIT_REGISTRY.define('celsius_per_meter = delta_degC / meter = temperature_gradient')

# Register thermal conductivity related units
UNIT_REGISTRY.define('W_per_mK = watt / (meter * kelvin)')

# Register carbon emission units
UNIT_REGISTRY.define('kg_CO2_per_kWh = kilogram / kilowatt_hour')
UNIT_REGISTRY.define('tonne_CO2_per_MWh = tonne / megawatt_hour')

# Export the Quantity class and UNIT_REGISTRY for use in other modules
__all__ = ['Quantity', 'UNIT_REGISTRY']

print("Unit registry loaded with monetary and custom units for thermal energy storage")
