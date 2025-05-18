"""
Fuel cycle calculations for the small modular reactor.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
import math
import numpy as np

def calculate_burnup(power_density, enrichment, time_days):
    """
    Calculate fuel burnup based on power density, enrichment and time.
    
    Args:
        power_density: Power density in MW/tU
        enrichment: Fuel enrichment in % U-235
        time_days: Operating time in days
        
    Returns:
        Burnup in MWd/tU
    """
    # Simple linear burnup model
    burnup = power_density * time_days
    
    # Apply correction factor based on enrichment
    # Higher enrichment allows higher burnup
    correction = 0.8 + 0.05 * enrichment
    
    return burnup * correction

def calculate_fuel_cycle_length():
    """
    Calculate the fuel cycle length based on reactor parameters.
    
    Returns:
        Cycle length in effective full power days (EFPD)
    """
    # Calculate core uranium mass
    fuel_assemblies = REACTOR_PARAMS.fuel_assemblies
    rods_per_assembly = REACTOR_PARAMS.fuel_rods_per_assembly
    
    # Assuming UO2 fuel with 10.5 g/cm³ density and 95% theoretical density
    rod_diameter = 0.0095  # m
    rod_height = REACTOR_PARAMS.core_height.magnitude  # m
    rod_volume = math.pi * (rod_diameter/2)**2 * rod_height  # m³
    
    # UO2 density (95% of theoretical)
    uo2_density = 10500 * 0.95  # kg/m³
    
    # Mass of UO2 per rod
    uo2_mass_per_rod = rod_volume * uo2_density  # kg
    
    # Mass of uranium per rod (UO2 is about 88% uranium by mass)
    u_mass_per_rod = uo2_mass_per_rod * 0.88  # kg
    
    # Total uranium mass in core
    total_u_mass = u_mass_per_rod * rods_per_assembly * fuel_assemblies  # kg
    
    # Convert to metric tons
    total_u_mass_tons = total_u_mass / 1000  # tU
    
    # Calculate average power density
    power_mw = REACTOR_PARAMS.thermal_power.magnitude  # MW
    power_density = power_mw / total_u_mass_tons  # MW/tU
    
    # Calculate discharge burnup based on enrichment
    # Rule of thumb: ~10 GWd/tU per % enrichment
    max_burnup = REACTOR_PARAMS.enrichment * 10000  # MWd/tU
    
    # Calculate cycle length
    # Using a more realistic 4-batch fuel management with 90% capacity factor
    # This gives more realistic cycle lengths for SMRs
    batch_fraction = 1/4  # 4-batch fuel management
    capacity_factor = 0.9
    
    cycle_length_days = max_burnup * batch_fraction / power_density / capacity_factor
    
    # Calculate refueling interval in years
    refueling_interval_years = cycle_length_days / 365
    
    # Check if calculated refueling interval matches the parameter
    if abs(refueling_interval_years - REACTOR_PARAMS.refueling_interval) > 0.5:
        print(f"Warning: Calculated refueling interval ({refueling_interval_years:.2f} years) " +
              f"differs from parameter value ({REACTOR_PARAMS.refueling_interval} years)")
    
    return {
        "total_uranium_mass": total_u_mass,
        "power_density_per_uranium": power_density,
        "max_burnup": max_burnup,
        "cycle_length_efpd": cycle_length_days,
        "cycle_length_months": cycle_length_days / 30.4,
        "refueling_interval_years": refueling_interval_years
    }

def calculate_reactivity_coefficients():
    """
    Estimate key reactivity coefficients for the reactor.
    
    Returns:
        Dictionary of reactivity coefficients
    """
    # These values are typical for a PWR with similar parameters
    # In a real design, these would be calculated with neutronics codes
    
    # Fuel temperature coefficient (Doppler)
    # Typical range: -1.0 to -4.0 pcm/°C
    doppler = -2.5  # pcm/°C
    
    # Moderator temperature coefficient
    # Typical range: -10 to -50 pcm/°C
    moderator_temp = -30.0  # pcm/°C
    
    # Void coefficient
    # Typical range: -50 to -200 pcm/% void
    void = -100.0  # pcm/% void
    
    # Boron worth
    # Typical range: -7 to -10 pcm/ppm
    boron = -8.5  # pcm/ppm
    
    return {
        "doppler": doppler,
        "moderator_temperature": moderator_temp,
        "void": void,
        "boron": boron
    }

def calculate_shutdown_margin():
    """
    Calculate the shutdown margin with the highest worth rod stuck out.
    
    Returns:
        Shutdown margin in % dk/k
    """
    # Assuming total control rod worth of 8% dk/k
    total_rod_worth = 0.08
    
    # Highest worth rod is typically 20-25% of total worth
    highest_rod_worth = 0.25 * total_rod_worth
    
    # Available rod worth with highest worth rod stuck
    available_rod_worth = total_rod_worth - highest_rod_worth
    
    # Required shutdown margin (typically 1-2%)
    required_margin = 0.015
    
    # Actual margin
    actual_margin = available_rod_worth - required_margin
    
    return {
        "total_rod_worth": total_rod_worth * 100,
        "highest_rod_worth": highest_rod_worth * 100,
        "available_rod_worth": available_rod_worth * 100,
        "required_margin": required_margin * 100,
        "actual_margin": actual_margin * 100
    }

# Run calculations
fuel_cycle = calculate_fuel_cycle_length()
reactivity_coeffs = calculate_reactivity_coefficients()
shutdown_margin = calculate_shutdown_margin()

print(f"Total uranium in core: {fuel_cycle['total_uranium_mass']:.2f} kg")
print(f"Average power density: {fuel_cycle['power_density_per_uranium']:.2f} MW/tU")
print(f"Maximum fuel burnup: {fuel_cycle['max_burnup']:.2f} MWd/tU")
print(f"Fuel cycle length: {fuel_cycle['cycle_length_efpd']:.2f} EFPD ({fuel_cycle['cycle_length_months']:.2f} months)")
print(f"Doppler coefficient: {reactivity_coeffs['doppler']:.2f} pcm/°C")
print(f"Moderator temperature coefficient: {reactivity_coeffs['moderator_temperature']:.2f} pcm/°C")
print(f"Shutdown margin: {shutdown_margin['actual_margin']:.2f}% dk/k")
