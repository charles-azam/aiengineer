"""
Utility functions for High-Temperature Gas-cooled Reactor (HTGR) design.

This module provides calculation tools for HTGR design parameters including
core geometry, power density, coolant properties, and heat transfer.
"""

import math
import numpy as np
from typing import Dict, Tuple, Any
from pyforge import UREG


def calculate_core_volume(height: float, diameter: float) -> float:
    """
    Calculate the cylindrical core volume.
    
    Args:
        height: Core height in meters
        diameter: Core diameter in meters
        
    Returns:
        Core volume in cubic meters
    """
    radius = diameter / 2
    return math.pi * radius**2 * height


def calculate_power_density(power: float, volume: float) -> float:
    """
    Calculate power density in the reactor core.
    
    Args:
        power: Thermal power in MW
        volume: Core volume in cubic meters
        
    Returns:
        Power density in MW/m³
    """
    return power / volume


def helium_properties(temperature: float, pressure: float) -> Dict[str, Any]:
    """
    Calculate helium properties at given temperature and pressure.
    
    Args:
        temperature: Temperature in °C
        pressure: Pressure in MPa
        
    Returns:
        Dictionary containing helium properties:
        - density (kg/m³)
        - specific_heat (J/kg·K)
        - thermal_conductivity (W/m·K)
        - dynamic_viscosity (Pa·s)
    """
    # Convert temperature to Kelvin for calculations
    T_K = temperature + 273.15
    
    # Helium properties based on engineering correlations
    density = pressure * 1e6 * 4.0026 / (8314.46 * T_K)  # Ideal gas law with He molar mass
    
    # Specific heat is nearly constant for helium
    specific_heat = 5193.0  # J/kg·K
    
    # Thermal conductivity correlation (W/m·K)
    thermal_conductivity = 2.682e-3 * (T_K**0.71) * (1 + 1.123e-8 * pressure * 1e6)
    
    # Dynamic viscosity correlation (Pa·s)
    dynamic_viscosity = 3.674e-7 * T_K**0.7
    
    return {
        "density": density,
        "specific_heat": specific_heat,
        "thermal_conductivity": thermal_conductivity,
        "dynamic_viscosity": dynamic_viscosity,
        "temperature": UREG.Quantity(temperature, "degC"),
        "pressure": UREG.Quantity(pressure, "MPa")
    }


def co2_properties(temperature: float, pressure: float) -> Dict[str, Any]:
    """
    Calculate CO2 properties at given temperature and pressure.
    
    Args:
        temperature: Temperature in °C
        pressure: Pressure in MPa
        
    Returns:
        Dictionary containing CO2 properties:
        - density (kg/m³)
        - specific_heat (J/kg·K)
        - thermal_conductivity (W/m·K)
        - dynamic_viscosity (Pa·s)
    """
    # Convert temperature to Kelvin for calculations
    T_K = temperature + 273.15
    
    # CO2 properties based on engineering correlations
    # Simplified model valid for gas phase CO2 in typical HTGR secondary loop conditions
    
    # Density approximation using ideal gas law with CO2 molar mass
    density = pressure * 1e6 * 44.01 / (8314.46 * T_K)
    
    # Specific heat correlation (J/kg·K)
    specific_heat = 840.0 + 0.5 * temperature
    
    # Thermal conductivity correlation (W/m·K)
    thermal_conductivity = 0.0146 + 8.4e-5 * temperature
    
    # Dynamic viscosity correlation (Pa·s)
    dynamic_viscosity = (1.47e-5) * (T_K/300.0)**0.8
    
    return {
        "density": density,
        "specific_heat": specific_heat,
        "thermal_conductivity": thermal_conductivity,
        "dynamic_viscosity": dynamic_viscosity,
        "temperature": UREG.Quantity(temperature, "degC"),
        "pressure": UREG.Quantity(pressure, "MPa")
    }


def triso_particles_per_pebble(pebble_diameter: float, packing_fraction: float) -> int:
    """
    Calculate the number of TRISO particles in a fuel pebble.
    
    Args:
        pebble_diameter: Diameter of the fuel pebble in cm
        packing_fraction: Volume fraction of TRISO particles in the fuel zone
        
    Returns:
        Number of TRISO particles per pebble (rounded to nearest integer)
    """
    # Typical TRISO particle diameter in cm
    triso_diameter = 0.092
    
    # Calculate fuel zone volume (typically 5cm diameter in a 6cm pebble)
    fuel_zone_diameter = 0.833 * pebble_diameter  # Typical ratio
    fuel_zone_volume = (4/3) * math.pi * (fuel_zone_diameter/2)**3
    
    # Calculate TRISO particle volume
    triso_volume = (4/3) * math.pi * (triso_diameter/2)**3
    
    # Calculate number of particles
    num_particles = (fuel_zone_volume * packing_fraction) / triso_volume
    
    return round(num_particles)


def heat_exchanger_effectiveness(ntu: float, cr: float = 1.0, flow_arrangement: str = "counter") -> float:
    """
    Calculate heat exchanger effectiveness using the NTU method.
    
    Args:
        ntu: Number of Transfer Units
        cr: Heat capacity rate ratio (Cmin/Cmax), default=1.0
        flow_arrangement: Type of flow arrangement ("counter", "parallel", or "cross")
        
    Returns:
        Heat exchanger effectiveness (0-1)
    """
    if flow_arrangement == "counter":
        if abs(cr - 1.0) < 0.001:  # cr ≈ 1
            effectiveness = ntu / (1 + ntu)
        else:
            effectiveness = (1 - np.exp(-ntu * (1 - cr))) / (1 - cr * np.exp(-ntu * (1 - cr)))
    
    elif flow_arrangement == "parallel":
        effectiveness = (1 - np.exp(-ntu * (1 + cr))) / (1 + cr)
    
    elif flow_arrangement == "cross":
        # Simplified correlation for cross-flow (both fluids unmixed)
        effectiveness = 1 - np.exp((np.exp(-ntu * cr**0.22) - 1) / cr**0.22)
    
    else:
        raise ValueError("Invalid flow arrangement. Choose 'counter', 'parallel', or 'cross'")
    
    return effectiveness


# Print statement for manager visibility
print("HTGR utility functions loaded successfully")
