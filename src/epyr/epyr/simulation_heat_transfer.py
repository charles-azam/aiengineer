"""
Heat transfer simulation functions.
"""
import math
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

def calculate_heat_transfer_rate(hot_temp: float, cold_temp: float) -> float:
    """
    Calculate heat transfer rate between hot and cold sides.
    
    Args:
        hot_temp: Hot side temperature in °C
        cold_temp: Cold side temperature in °C
        
    Returns:
        Heat transfer rate in kW
    """
    # Simple heat transfer calculation using parameters
    delta_T = hot_temp - cold_temp
    area = 50  # m²
    heat_transfer_coeff = 500  # W/(m²·K)
    
    # Q = U * A * ΔT
    heat_transfer = heat_transfer_coeff * area * delta_T / 1000  # kW
    
    return heat_transfer

def calculate_temperature_profile(initial_temp: float, ambient_temp: float, time_hours: float) -> list:
    """
    Calculate temperature profile over time during cooling.
    
    Args:
        initial_temp: Initial temperature in °C
        ambient_temp: Ambient temperature in °C
        time_hours: Time period in hours
        
    Returns:
        List of temperatures at hourly intervals
    """
    # Parameters
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    surface_area = THERMAL_STORAGE_PARAMS.surface_area.magnitude
    insulation_thickness = THERMAL_STORAGE_PARAMS.insulation_thickness.magnitude
    insulation_conductivity = THERMAL_STORAGE_PARAMS.insulation_conductivity.magnitude
    
    # Overall heat transfer coefficient (simplified)
    U = insulation_conductivity / insulation_thickness  # W/(m²·K)
    
    # Time constant
    tau = mass * specific_heat / (U * surface_area * 3600)  # hours
    
    # Temperature profile (Newton's law of cooling)
    temps = []
    hours = range(int(time_hours) + 1)
    
    for t in hours:
        temp = ambient_temp + (initial_temp - ambient_temp) * math.exp(-t / tau)
        temps.append(temp)
    
    return temps

print("Heat transfer simulation module loaded")
