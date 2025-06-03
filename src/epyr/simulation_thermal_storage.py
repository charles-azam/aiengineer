"""
Simulation module for thermal energy storage system performance.
"""
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS
import numpy as np
import math

# Print debug information
print("Loading thermal storage simulation module")

def calculate_energy_content(current_temperature: float) -> float:
    """
    Calculate the energy content of the storage system at a given temperature.
    
    Args:
        current_temperature: Current temperature of the storage medium in °C
        
    Returns:
        Energy content in kWh
    """
    # Basic calculation of energy content based on temperature difference
    min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    
    # Energy = mass * specific heat * temperature difference
    # Convert from kJ to kWh by dividing by 3600
    energy_content = mass * specific_heat * (current_temperature - min_temp) / 3600
    
    return energy_content

def calculate_heat_loss(duration_hours: float) -> float:
    """
    Calculate heat loss over a specified time period using simplified model.
    
    Args:
        duration_hours: Time period in hours
        
    Returns:
        Heat loss in kWh
    """
    # Simplified heat loss calculation
    ambient_temp = THERMAL_STORAGE_PARAMS.ambient_temperature.magnitude
    daily_loss_rate = THERMAL_STORAGE_PARAMS.self_discharge_rate
    
    # Convert daily rate to hourly and calculate energy loss
    hourly_loss_rate = daily_loss_rate / 24
    max_energy = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude
    
    # Energy loss is proportional to time
    energy_loss = max_energy * hourly_loss_rate * duration_hours
    
    return energy_loss

def simulate_charging(hours: float) -> dict:
    """
    Simulate charging of the thermal storage system.
    
    Args:
        hours: Duration of charging in hours
        
    Returns:
        Dictionary with simulation results
    """
    # Get parameters
    min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
    max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
    charge_rate = THERMAL_STORAGE_PARAMS.max_power_output.magnitude  # kW
    efficiency = THERMAL_STORAGE_PARAMS.charge_efficiency
    
    # Calculate energy input
    energy_input = charge_rate * hours  # kWh
    energy_stored = energy_input * efficiency  # kWh
    
    # Calculate final temperature (simplified)
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    
    # Temperature increase = energy / (mass * specific heat)
    # Convert kWh to kJ by multiplying by 3600
    temp_increase = energy_stored * 3600 / (mass * specific_heat)
    
    # Account for heat loss
    heat_loss = calculate_heat_loss(hours)
    temp_decrease = heat_loss * 3600 / (mass * specific_heat)
    
    # Net temperature change
    final_temp = min_temp + temp_increase - temp_decrease
    
    # Ensure temperature doesn't exceed maximum
    final_temp = min(final_temp, max_temp)
    
    return {
        "final_temp": final_temp,
        "energy_stored": energy_stored - heat_loss,
        "avg_power": charge_rate
    }

def simulate_discharging(hours: float) -> dict:
    """
    Simulate discharging of the thermal storage system.
    
    Args:
        hours: Duration of discharging in hours
        
    Returns:
        Dictionary with simulation results
    """
    # Get parameters
    min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
    max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
    discharge_rate = THERMAL_STORAGE_PARAMS.max_power_output.magnitude  # kW
    efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Calculate energy output
    max_energy_output = discharge_rate * hours  # kWh
    
    # Calculate temperature decrease (simplified)
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    
    # Maximum temperature decrease possible
    max_temp_decrease = max_energy_output * 3600 / (mass * specific_heat * efficiency)
    
    # Actual temperature decrease (limited by min temperature)
    actual_temp_decrease = min(max_temp_decrease, max_temp - min_temp)
    
    # Energy delivered (accounting for efficiency)
    energy_delivered = actual_temp_decrease * mass * specific_heat / 3600 * efficiency
    
    # Account for heat loss
    heat_loss = calculate_heat_loss(hours)
    
    # Final temperature
    final_temp = max_temp - actual_temp_decrease
    
    return {
        "final_temp": final_temp,
        "energy_delivered": energy_delivered - heat_loss,
        "avg_power": energy_delivered / hours
    }

def calculate_round_trip_efficiency() -> float:
    """
    Calculate round-trip efficiency of the thermal storage system.
    
    Returns:
        Round-trip efficiency as a fraction
    """
    # Simplified calculation based on charge and discharge efficiencies
    return THERMAL_STORAGE_PARAMS.charge_efficiency * THERMAL_STORAGE_PARAMS.discharge_efficiency

def calculate_exergy_efficiency() -> float:
    """
    Calculate exergy efficiency of the thermal storage system.
    
    Returns:
        Exergy efficiency as a fraction
    """
    # Simplified calculation
    # Exergy efficiency is typically lower than energy efficiency
    return calculate_round_trip_efficiency() * 0.9

# Print some basic simulation results
print(f"Maximum energy storage: {THERMAL_STORAGE_PARAMS.storage_capacity}")
print(f"Operating temperature range: {THERMAL_STORAGE_PARAMS.min_temperature} to {THERMAL_STORAGE_PARAMS.max_temperature}")

# Run a sample simulation
charge_hours = 8
discharge_hours = 10

print("\nRunning simulations...")
charge_results = simulate_charging(charge_hours)
discharge_results = simulate_discharging(discharge_hours)
round_trip = calculate_round_trip_efficiency()

print(f"Charging: {charge_results['energy_stored']:.2f} kWh stored, final temp: {charge_results['final_temp']:.1f}°C")
print(f"Discharging: {discharge_results['energy_delivered']:.2f} kWh delivered, final temp: {discharge_results['final_temp']:.1f}°C")
print(f"Round-trip efficiency: {round_trip*100:.1f}%")
