"""
Simulation module for thermal energy storage system performance.
"""
from epyr.tools_units import Quantity
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS
from epyr.parameters_materials import (
    MOLTEN_SALT,
    SOLID_CERAMIC,
    HIGH_TEMP_CERAMIC,
    MOLTEN_METAL,
    PHASE_CHANGE_MATERIAL
)
import numpy as np
import math

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
    Calculate heat loss over a specified time period.
    
    Args:
        duration_hours: Time period in hours
        
    Returns:
        Heat loss in kWh
    """
    # Get parameters
    ambient_temp = THERMAL_STORAGE_PARAMS.ambient_temperature.magnitude
    max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
    insulation_thickness = THERMAL_STORAGE_PARAMS.insulation_thickness.magnitude  # m
    insulation_conductivity = THERMAL_STORAGE_PARAMS.insulation_conductivity.magnitude  # W/(m·K)
    surface_area = THERMAL_STORAGE_PARAMS.surface_area.magnitude  # m²
    
    # Calculate heat loss using simplified model
    # Q = k * A * (T_hot - T_cold) / thickness * time
    temp_diff = max_temp - ambient_temp
    heat_loss_rate = insulation_conductivity * surface_area * temp_diff / insulation_thickness  # W
    heat_loss = heat_loss_rate * duration_hours / 1000  # kWh
    
    return heat_loss

def simulate_charging(charge_hours: float) -> dict:
    """
    Simulate charging of the thermal storage system.
    
    Args:
        charge_hours: Duration of charging in hours
        
    Returns:
        Dictionary with simulation results
    """
    # Get parameters
    max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
    min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
    charge_rate = THERMAL_STORAGE_PARAMS.max_power_output.magnitude  # kW
    efficiency = THERMAL_STORAGE_PARAMS.charge_efficiency
    
    # Calculate energy input
    energy_input = charge_rate * charge_hours  # kWh
    energy_stored = energy_input * efficiency  # kWh
    
    # Calculate final temperature (simplified)
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    
    # Temperature increase = energy / (mass * specific heat)
    # Convert kWh to kJ by multiplying by 3600
    temp_increase = energy_stored * 3600 / (mass * specific_heat)
    final_temp = min(min_temp + temp_increase, max_temp)
    
    # Account for heat loss during charging (simplified)
    heat_loss = calculate_heat_loss(charge_hours)
    energy_stored -= heat_loss
    
    return {
        "initial_temp": min_temp,
        "final_temp": final_temp,
        "energy_input": energy_input,
        "energy_stored": energy_stored,
        "heat_loss": heat_loss,
        "avg_power": charge_rate
    }

def simulate_discharging(discharge_hours: float) -> dict:
    """
    Simulate discharging of the thermal storage system.
    
    Args:
        discharge_hours: Duration of discharging in hours
        
    Returns:
        Dictionary with simulation results
    """
    # Get parameters
    max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
    min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
    discharge_rate = THERMAL_STORAGE_PARAMS.max_power_output.magnitude  # kW
    efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Calculate energy output
    max_energy_output = discharge_rate * discharge_hours  # kWh
    
    # Calculate available energy in storage (simplified)
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    
    # Available energy = mass * specific heat * (max_temp - min_temp) / 3600 (to convert from kJ to kWh)
    available_energy = mass * specific_heat * (max_temp - min_temp) / 3600
    
    # Actual energy delivered (limited by available energy and efficiency)
    energy_delivered = min(max_energy_output, available_energy * efficiency)
    
    # Calculate final temperature
    # Energy extracted = mass * specific heat * (initial_temp - final_temp)
    # Therefore: final_temp = initial_temp - (energy_extracted / (mass * specific_heat))
    energy_extracted = energy_delivered / efficiency  # Energy extracted from storage
    temp_decrease = energy_extracted * 3600 / (mass * specific_heat)
    final_temp = max(max_temp - temp_decrease, min_temp)
    
    # Account for heat loss during discharging (simplified)
    heat_loss = calculate_heat_loss(discharge_hours)
    
    return {
        "initial_temp": max_temp,
        "final_temp": final_temp,
        "energy_delivered": energy_delivered,
        "heat_loss": heat_loss,
        "avg_power": energy_delivered / discharge_hours
    }

def calculate_round_trip_efficiency() -> float:
    """
    Calculate round-trip efficiency of the thermal storage system.
    
    Returns:
        Round-trip efficiency as a fraction
    """
    # Basic calculation using charge and discharge efficiencies
    # and accounting for thermal losses
    charge_efficiency = THERMAL_STORAGE_PARAMS.charge_efficiency
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Estimate thermal losses for a typical cycle (e.g., 24 hours)
    storage_duration = 24  # hours
    heat_loss = calculate_heat_loss(storage_duration)
    
    # Calculate total energy capacity
    max_temp = THERMAL_STORAGE_PARAMS.max_temperature.magnitude
    min_temp = THERMAL_STORAGE_PARAMS.min_temperature.magnitude
    mass = THERMAL_STORAGE_PARAMS.storage_volume.magnitude * THERMAL_STORAGE_PARAMS.storage_medium_density.magnitude
    specific_heat = THERMAL_STORAGE_PARAMS.storage_medium_specific_heat.magnitude
    energy_capacity = mass * specific_heat * (max_temp - min_temp) / 3600  # kWh
    
    # Calculate thermal loss factor
    thermal_loss_factor = 1 - (heat_loss / energy_capacity)
    
    # Round-trip efficiency
    round_trip_efficiency = charge_efficiency * discharge_efficiency * thermal_loss_factor
    
    return round_trip_efficiency

def calculate_exergy_efficiency() -> float:
    """
    Calculate exergy efficiency of the thermal storage system.
    
    Returns:
        Exergy efficiency as a fraction
    """
    # Exergy efficiency calculation (simplified)
    # Accounts for the quality of energy (temperature)
    
    # Get temperatures in Kelvin
    T_max = THERMAL_STORAGE_PARAMS.max_temperature.to("kelvin").magnitude
    T_min = THERMAL_STORAGE_PARAMS.min_temperature.to("kelvin").magnitude
    T_ambient = THERMAL_STORAGE_PARAMS.ambient_temperature.to("kelvin").magnitude
    
    # Calculate Carnot factors
    carnot_max = 1 - (T_ambient / T_max)
    carnot_min = 1 - (T_ambient / T_min)
    
    # Calculate average Carnot factor for the storage
    carnot_avg = (carnot_max + carnot_min) / 2
    
    # Exergy efficiency is the product of round-trip efficiency and Carnot factor
    round_trip = calculate_round_trip_efficiency()
    exergy_efficiency = round_trip * carnot_avg
    
    return exergy_efficiency

def simulate_full_cycle() -> dict:
    """
    Simulate a full charge-discharge cycle.
    
    Returns:
        Dictionary with simulation results
    """
    # Define cycle parameters
    charge_hours = 8
    storage_hours = 10
    discharge_hours = 6
    
    # Simulate charging
    charging_results = simulate_charging(charge_hours)
    
    # Calculate heat loss during storage
    storage_heat_loss = calculate_heat_loss(storage_hours)
    
    # Simulate discharging
    discharging_results = simulate_discharging(discharge_hours)
    
    # Calculate overall metrics
    energy_input = charging_results["energy_input"]
    energy_output = discharging_results["energy_delivered"]
    total_heat_loss = charging_results["heat_loss"] + storage_heat_loss + discharging_results["heat_loss"]
    cycle_efficiency = energy_output / energy_input
    
    return {
        "charge_hours": charge_hours,
        "storage_hours": storage_hours,
        "discharge_hours": discharge_hours,
        "energy_input": energy_input,
        "energy_output": energy_output,
        "total_heat_loss": total_heat_loss,
        "cycle_efficiency": cycle_efficiency
    }

def compare_materials() -> dict:
    """
    Compare performance of different storage materials.
    
    Returns:
        Dictionary with comparison results
    """
    materials = {
        "Molten Salt": MOLTEN_SALT,
        "Solid Ceramic": SOLID_CERAMIC,
        "High-Temp Ceramic": HIGH_TEMP_CERAMIC,
        "Molten Metal": MOLTEN_METAL,
        "Phase Change Material": PHASE_CHANGE_MATERIAL
    }
    
    results = {}
    
    for name, material in materials.items():
        # Calculate energy density
        density = material.density.magnitude
        specific_heat = material.specific_heat.magnitude
        temp_range = material.max_temperature.magnitude - material.min_temperature.magnitude
        
        # Energy density in kWh/m³
        energy_density = density * specific_heat * temp_range / 3600
        
        # Estimate charging time (hours) for a standard energy input
        standard_energy = 1000  # kWh
        charging_time = standard_energy / THERMAL_STORAGE_PARAMS.max_power_input.magnitude
        
        # Estimate heat loss based on thermal conductivity
        thermal_conductivity_ratio = material.thermal_conductivity.magnitude / 1.0  # Normalized to a reference value
        relative_heat_loss = 1.0 * thermal_conductivity_ratio  # Simplified model
        
        results[name] = {
            "energy_density": energy_density,
            "temp_range": temp_range,
            "charging_time": charging_time,
            "relative_heat_loss": relative_heat_loss,
            "cost_per_kwh": material.cost_per_kg.magnitude * density / energy_density
        }
    
    return results

# Print some basic simulation results
print(f"Maximum energy storage: {THERMAL_STORAGE_PARAMS.storage_capacity}")
print(f"Operating temperature range: {THERMAL_STORAGE_PARAMS.min_temperature} to {THERMAL_STORAGE_PARAMS.max_temperature}")

# Run a sample simulation
cycle_results = simulate_full_cycle()
print(f"Cycle efficiency: {cycle_results['cycle_efficiency']*100:.1f}%")
print(f"Energy input: {cycle_results['energy_input']:.1f} kWh")
print(f"Energy output: {cycle_results['energy_output']:.1f} kWh")
