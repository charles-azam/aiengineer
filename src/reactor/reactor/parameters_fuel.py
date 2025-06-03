"""
Fuel parameters for the High-Temperature Gas-cooled Reactor (HTGR).
Defines all key parameters for the TRISO fuel design.
"""

from pyforge import Parameters, Quantity
from reactor import UREG

class FuelParameters(Parameters):
    """Define all the key parameters for the HTGR TRISO fuel."""
    
    # TRISO fuel specifications
    fuel_type: str = "TRISO"
    kernel_material: str = "UCO"
    kernel_diameter: Quantity = Quantity(500, "micrometer")
    buffer_thickness: Quantity = Quantity(100, "micrometer")
    ipyc_thickness: Quantity = Quantity(40, "micrometer")
    sic_thickness: Quantity = Quantity(35, "micrometer")
    opyc_thickness: Quantity = Quantity(40, "micrometer")
    enrichment: Quantity = Quantity(0.155, "dimensionless")  # 15.5%
    packing_fraction: Quantity = Quantity(0.35, "dimensionless")  # 35%
    
    # Fuel performance parameters
    burnup: Quantity = Quantity(150, "gigawatt*day/ton")
    refueling_interval: Quantity = Quantity(5, "year")
    refueling_duration: Quantity = Quantity(14, "day")
    spent_fuel_storage: str = "On-site dry storage"

# Single source of truth
FUEL_PARAMS = FuelParameters()

# Print key parameters for verification
print(f"TRISO fuel kernel diameter: {FUEL_PARAMS.kernel_diameter}")
print(f"TRISO fuel enrichment: {FUEL_PARAMS.enrichment}")
print(f"Target burnup: {FUEL_PARAMS.burnup}")
print("Fuel parameters loaded successfully")
