"""
Efficiency calculation functions.
"""
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

def calculate_round_trip_efficiency() -> float:
    """
    Calculate round-trip efficiency of the thermal storage system.
    
    Returns:
        Round-trip efficiency as a fraction
    """
    # Simplified calculation based on charge and discharge efficiencies
    # and accounting for thermal losses
    charge_efficiency = THERMAL_STORAGE_PARAMS.charge_efficiency
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Estimate thermal losses for a typical cycle
    thermal_loss_factor = 0.98  # Assuming 2% thermal losses
    
    # Round-trip efficiency
    round_trip_efficiency = charge_efficiency * discharge_efficiency * thermal_loss_factor
    
    return round_trip_efficiency

def calculate_exergy_efficiency() -> float:
    """
    Calculate exergy efficiency of the thermal storage system.
    
    Returns:
        Exergy efficiency as a fraction
    """
    # Simplified calculation
    # Exergy efficiency is typically lower than energy efficiency due to
    # quality degradation of thermal energy
    round_trip = calculate_round_trip_efficiency()
    
    # Carnot factor approximation
    T_hot = THERMAL_STORAGE_PARAMS.max_temperature.magnitude + 273.15  # K
    T_cold = THERMAL_STORAGE_PARAMS.min_temperature.magnitude + 273.15  # K
    T_ambient = THERMAL_STORAGE_PARAMS.ambient_temperature.magnitude + 273.15  # K
    
    carnot_factor = (1 - T_ambient/T_hot) / (1 - T_ambient/T_cold)
    
    exergy_efficiency = round_trip * carnot_factor
    return exergy_efficiency

print("Efficiency simulation module loaded")
