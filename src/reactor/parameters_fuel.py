"""
Parameters for TRISO fuel particles used in High-Temperature Gas-cooled Reactor (HTGR).

TRISO (TRIstructural-ISOtropic) fuel consists of uranium kernels coated with 
multiple layers of carbon and silicon carbide, providing containment of fission products.
"""

from pyforge import Parameters, Quantity, UREG
from reactor import UREG

class TRISOFuelParameters(Parameters):
    """
    Parameters defining TRISO fuel particles for HTGR applications.
    
    TRISO particles consist of a uranium kernel surrounded by four coating layers:
    1. Buffer layer (porous carbon)
    2. Inner Pyrolytic Carbon (IPyC)
    3. Silicon Carbide (SiC)
    4. Outer Pyrolytic Carbon (OPyC)
    """
    # Kernel parameters
    kernel_diameter: Quantity = Quantity(500, "micrometer")
    kernel_density: Quantity = Quantity(10.8, "g/cm^3")
    kernel_material: str = "UO2"  # Uranium dioxide
    uranium_enrichment: Quantity = Quantity(0.155, "dimensionless")  # U-235 enrichment
    
    # Coating layer thicknesses
    buffer_thickness: Quantity = Quantity(95, "micrometer")
    ipyc_thickness: Quantity = Quantity(40, "micrometer")
    sic_thickness: Quantity = Quantity(35, "micrometer")
    opyc_thickness: Quantity = Quantity(40, "micrometer")
    
    # Coating layer densities
    buffer_density: Quantity = Quantity(1.05, "g/cm^3")
    ipyc_density: Quantity = Quantity(1.90, "g/cm^3")
    sic_density: Quantity = Quantity(3.20, "g/cm^3")
    opyc_density: Quantity = Quantity(1.90, "g/cm^3")
    
    # Fuel compact parameters
    compact_diameter: Quantity = Quantity(12.5, "mm")
    compact_height: Quantity = Quantity(50, "mm")
    packing_fraction: Quantity = Quantity(0.35, "dimensionless")  # Volume fraction of TRISO in compact
    matrix_material: str = "Graphite"
    matrix_density: Quantity = Quantity(1.75, "g/cm^3")
    
    # Fuel performance parameters
    max_burnup: Quantity = Quantity(150, "gigawatt*day/ton")
    max_temperature: Quantity = Quantity(1250, "degC")
    design_failure_fraction: Quantity = Quantity(1e-5, "dimensionless")  # Expected particle failure rate
    
    # Neutronic parameters
    heavy_metal_loading: Quantity = Quantity(7, "gram")  # Heavy metal per compact
    fissile_loading: Quantity = Quantity(1.085, "gram")  # U-235 content per compact
    
    # Thermal properties
    thermal_conductivity: Quantity = Quantity(3.5, "watt/(meter*kelvin)")  # For compact
    specific_heat_capacity: Quantity = Quantity(1.5, "kilojoule/(kilogram*kelvin)")  # For compact
    
    # Additional parameters needed for compatibility with other modules
    type: str = "TRISO"
    enrichment: float = 0.155
    target_burnup: float = 150  # GWd/tHM
    refueling_interval: Quantity = Quantity(5, "year")
    refueling_duration: Quantity = Quantity(14, "day")
    spent_fuel_storage: str = "On-site dry storage"
    burnup: Quantity = Quantity(150, "gigawatt*day/ton")

# Single source of truth
TRISO_PARAMS = TRISOFuelParameters()
FUEL_PARAMS = TRISO_PARAMS  # Alias for compatibility with other modules
print("DEBUG: Created FUEL_PARAMS alias for TRISO_PARAMS in parameters_fuel.py")

# Derived parameters (calculated from base parameters)
def calculate_derived_parameters():
    """Calculate and print derived TRISO fuel parameters."""
    # Total TRISO particle diameter
    total_diameter = (TRISO_PARAMS.kernel_diameter + 
                     2 * (TRISO_PARAMS.buffer_thickness + 
                          TRISO_PARAMS.ipyc_thickness + 
                          TRISO_PARAMS.sic_thickness + 
                          TRISO_PARAMS.opyc_thickness))
    
    # Volume of a single kernel
    kernel_radius = TRISO_PARAMS.kernel_diameter / 2
    kernel_volume = (4/3) * 3.14159 * (kernel_radius**3)
    
    # Uranium mass per particle
    uranium_fraction = 0.881  # Mass fraction of uranium in UO2
    uranium_per_particle = kernel_volume * TRISO_PARAMS.kernel_density * uranium_fraction
    
    # Particles per compact
    particles_per_compact = TRISO_PARAMS.heavy_metal_loading / uranium_per_particle
    
    print(f"Total TRISO particle diameter: {total_diameter}")
    print(f"Uranium per particle: {uranium_per_particle.to('mg'):.4f}")
    print(f"Particles per compact: {particles_per_compact.magnitude:.0f}")
    print(f"Total heavy metal in core (10 MWth): {TRISO_PARAMS.heavy_metal_loading * 1500:.2f}")  # Assuming 1500 compacts for 10 MWth

# Print key parameters for verification
print(f"TRISO fuel kernel diameter: {TRISO_PARAMS.kernel_diameter}")
print(f"Uranium enrichment: {TRISO_PARAMS.uranium_enrichment}")
print(f"Maximum fuel temperature: {TRISO_PARAMS.max_temperature}")
print(f"Heavy metal loading per compact: {TRISO_PARAMS.heavy_metal_loading}")

# Calculate derived parameters
calculate_derived_parameters()

print("DEBUG: TRISO fuel parameters loaded successfully with standard units")
"""
TRISO fuel parameters for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Parameters, Quantity, UREG

class FuelParameters(Parameters):
    """Define all key parameters for the TRISO fuel."""
    # Kernel parameters
    kernel_material: str = "UO2"
    kernel_diameter: Quantity = Quantity(500, "micrometer")
    enrichment: Quantity = Quantity(15.5, "wt_percent")
    
    # Coating layers
    buffer_thickness: Quantity = Quantity(95, "micrometer")
    ipyc_thickness: Quantity = Quantity(40, "micrometer")
    sic_thickness: Quantity = Quantity(35, "micrometer")
    opyc_thickness: Quantity = Quantity(40, "micrometer")
    
    # Derived parameters
    total_particle_diameter: Quantity = Quantity(920, "micrometer")
    failure_temperature: Quantity = Quantity(1600, "degC")
    
    # Fuel element parameters
    fuel_elements_medium: int = 1500  # For 15 MW configuration

# Single source of truth
FUEL_PARAMS = FuelParameters()
