"""
Simulation module for HTGR core thermal-hydraulics.

This module provides simple analytical models for:
- Core power distribution
- Fuel temperature distribution
- Coolant temperature rise
- Core pressure drop
- Heat transfer from fuel to coolant
"""

import math
import numpy as np
from pyforge import UREG, Quantity

# Import necessary parameters
from reactor.parameters_core import CORE_PARAMS

print("DEBUG: Loaded simulation_core.py with proper imports")


def calculate_power_distribution(axial_positions, radial_positions):
    """
    Calculate the power distribution in the reactor core.
    
    Args:
        axial_positions: Array of normalized axial positions (0 to 1)
        radial_positions: Array of normalized radial positions (0 to 1)
        
    Returns:
        2D array of relative power densities
    """
    # Simple cosine axial distribution and J0 Bessel function radial distribution
    axial_shape = np.cos(np.pi * (axial_positions - 0.5))
    
    # Simplified J0 Bessel approximation using cosine
    radial_shape = np.cos(np.pi/2 * radial_positions)
    
    # Create 2D power distribution
    axial_2d = np.tile(axial_shape[:, np.newaxis], (1, len(radial_positions)))
    radial_2d = np.tile(radial_shape, (len(axial_positions), 1))
    
    power_distribution = axial_2d * radial_2d
    
    # Normalize to maintain total power
    power_distribution = power_distribution / np.mean(power_distribution) * CORE_PARAMS.thermal_power.magnitude
    
    print(f"Power distribution calculated with peak-to-average ratio: {np.max(power_distribution)/np.mean(power_distribution):.2f}")
    return power_distribution


def calculate_fuel_temperature(power_distribution, coolant_temperature):
    """
    Calculate the fuel temperature distribution based on power distribution.
    
    Args:
        power_distribution: 2D array of power densities (W/m³)
        coolant_temperature: Temperature of coolant at each position (K or °C)
        
    Returns:
        2D array of fuel temperatures
    """
    # Get fuel thermal conductivity
    k_fuel = CORE_PARAMS.fuel_thermal_conductivity.to('W/(m*K)').magnitude
    
    # Get fuel particle radius
    r_fuel = CORE_PARAMS.fuel_particle_radius.to('m').magnitude
    
    # Calculate temperature difference between fuel center and surface
    # Using conduction equation for spherical geometry: ΔT = q'''*r²/(6*k)
    # where q''' is volumetric heat generation
    
    # Convert power distribution to volumetric heat generation
    fuel_volume = CORE_PARAMS.core_volume.to('m^3').magnitude * CORE_PARAMS.fuel_volume_fraction
    q_vol = power_distribution / fuel_volume
    
    # Temperature difference between fuel center and surface
    delta_T = q_vol * (r_fuel**2) / (6 * k_fuel)
    
    # Add to coolant temperature to get fuel temperature
    fuel_temperature = coolant_temperature + delta_T
    
    print(f"Fuel temperature calculated with maximum: {np.max(fuel_temperature):.1f} K")
    return fuel_temperature


def calculate_coolant_temperature_rise(power_distribution, inlet_temperature):
    """
    Calculate the coolant temperature rise across the core.
    
    Args:
        power_distribution: 2D array of power densities
        inlet_temperature: Coolant inlet temperature (K or °C)
        
    Returns:
        2D array of coolant temperatures
    """
    # Get coolant properties
    cp_coolant = CORE_PARAMS.coolant_specific_heat.to('J/(kg*K)').magnitude
    mass_flow = CORE_PARAMS.coolant_mass_flow.to('kg/s').magnitude
    
    # Calculate axial power distribution (sum over radial)
    axial_power = np.sum(power_distribution, axis=1)
    
    # Calculate cumulative power along axial direction
    cumulative_power = np.cumsum(axial_power)
    
    # Calculate temperature rise
    temperature_rise = cumulative_power / (mass_flow * cp_coolant)
    
    # Add inlet temperature
    axial_temperature = inlet_temperature + temperature_rise
    
    # Expand to 2D (assuming uniform temperature radially at each axial position)
    coolant_temperature = np.tile(axial_temperature[:, np.newaxis], 
                                 (1, power_distribution.shape[1]))
    
    outlet_temp = axial_temperature[-1]
    print(f"Coolant temperature rise: {outlet_temp - inlet_temperature:.1f} K")
    print(f"Outlet temperature: {outlet_temp:.1f} K")
    
    return coolant_temperature


def calculate_core_pressure_drop():
    """
    Calculate the pressure drop across the reactor core.
    
    Returns:
        Pressure drop in Pa
    """
    # Get core geometry and flow parameters
    core_length = CORE_PARAMS.core_height.to('m').magnitude
    hydraulic_diameter = CORE_PARAMS.coolant_channel_diameter.to('m').magnitude
    coolant_velocity = CORE_PARAMS.coolant_velocity.to('m/s').magnitude
    coolant_density = CORE_PARAMS.coolant_density.to('kg/m^3').magnitude
    friction_factor = CORE_PARAMS.friction_factor
    
    # Calculate pressure drop using Darcy-Weisbach equation
    # ΔP = f * (L/D) * (ρ*v²/2)
    pressure_drop = (friction_factor * (core_length / hydraulic_diameter) * 
                    (coolant_density * coolant_velocity**2 / 2))
    
    pressure_drop_quantity = Quantity(pressure_drop, 'Pa')
    
    print(f"Core pressure drop: {pressure_drop_quantity}")
    return pressure_drop_quantity


def calculate_heat_transfer(fuel_temperature, coolant_temperature):
    """
    Calculate heat transfer from fuel to coolant.
    
    Args:
        fuel_temperature: 2D array of fuel temperatures
        coolant_temperature: 2D array of coolant temperatures
        
    Returns:
        2D array of heat transfer rates (W/m²)
    """
    # Get heat transfer coefficient
    h_transfer = CORE_PARAMS.heat_transfer_coefficient.to('W/(m^2*K)').magnitude
    
    # Calculate temperature difference
    delta_T = fuel_temperature - coolant_temperature
    
    # Calculate heat flux using Newton's law of cooling
    heat_flux = h_transfer * delta_T
    
    # Calculate total heat transfer area
    heat_transfer_area = CORE_PARAMS.heat_transfer_area.to('m^2').magnitude
    
    # Calculate total heat transfer
    total_heat_transfer = np.sum(heat_flux) * heat_transfer_area / heat_flux.size
    
    print(f"Average heat flux: {np.mean(heat_flux):.1f} W/m²")
    print(f"Total heat transfer: {total_heat_transfer:.2e} W")
    
    return heat_flux


# Execute simulation when run directly
if __name__ == "__main__":
    print("Running HTGR core thermal-hydraulics simulation...")
    
    # Create mesh grid for core
    n_axial = 20
    n_radial = 10
    axial_positions = np.linspace(0, 1, n_axial)
    radial_positions = np.linspace(0, 1, n_radial)
    
    # Run simulation steps
    power_dist = calculate_power_distribution(axial_positions, radial_positions)
    
    inlet_temp = CORE_PARAMS.inlet_temperature.to('K').magnitude
    coolant_temp = calculate_coolant_temperature_rise(power_dist, inlet_temp)
    
    fuel_temp = calculate_fuel_temperature(power_dist, coolant_temp)
    
    pressure_drop = calculate_core_pressure_drop()
    
    heat_flux = calculate_heat_transfer(fuel_temp, coolant_temp)
    
    print("\nCore simulation complete!")
    print(f"Maximum fuel temperature: {np.max(fuel_temp):.1f} K")
    print(f"Core outlet temperature: {np.max(coolant_temp):.1f} K")
    print(f"Core pressure drop: {pressure_drop}")
