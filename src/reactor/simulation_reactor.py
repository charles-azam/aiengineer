"""
Simple performance calculations for the small modular reactor.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
import math

def compute_power_density() -> float:
    """
    Returns the power density (MW/m³) in the reactor core.
    """
    core_volume = math.pi * (REACTOR_PARAMS.core_diameter.magnitude/2)**2 * REACTOR_PARAMS.core_height.magnitude
    power_density = REACTOR_PARAMS.thermal_power.magnitude / core_volume
    return power_density

def compute_temperature_rise() -> float:
    """
    Returns the temperature rise (°C) in the primary coolant.
    """
    # Q = m * cp * ΔT
    # Assuming cp of water = 4200 J/(kg·K)
    cp_water = 4200  # J/(kg·K)
    power_watts = REACTOR_PARAMS.thermal_power.magnitude * 1e6  # Convert MW to W
    delta_t = power_watts / (THERMAL_PARAMS.primary_flow_rate.magnitude * cp_water)
    return delta_t

def compute_steam_flow_rate() -> float:
    """
    Returns the steam flow rate (kg/s) in the secondary loop.
    """
    # Assuming latent heat of vaporization = 1800 kJ/kg at secondary pressure
    latent_heat = 1800 * 1000  # J/kg
    power_watts = REACTOR_PARAMS.thermal_power.magnitude * 1e6 * 0.97  # 97% heat transfer efficiency
    steam_flow = power_watts / latent_heat
    return steam_flow

def compute_fuel_consumption() -> float:
    """
    Returns the approximate fuel consumption (kg/year) of U-235.
    """
    # Approximate calculation based on energy release per fission
    # 1 MWd thermal ≈ 1.05 g U-235 consumed
    power_mwd_per_year = REACTOR_PARAMS.thermal_power.magnitude * 365  # MWd/year
    u235_consumption = power_mwd_per_year * 1.05 / 1000  # kg/year
    return u235_consumption

def compute_safety_margins():
    """
    Returns a dictionary of key safety margins.
    """
    power_density = compute_power_density()
    max_safe_power_density = 100  # MW/m³
    
    primary_pressure = THERMAL_PARAMS.primary_pressure.magnitude
    design_pressure = primary_pressure * 1.25  # 25% margin
    
    return {
        "power_density_margin": max_safe_power_density / power_density,
        "pressure_margin": design_pressure / primary_pressure,
        "decay_heat_removal_capacity": SAFETY_PARAMS.passive_cooling_capacity.magnitude / (REACTOR_PARAMS.thermal_power.magnitude * 0.05)  # Assuming 5% decay heat
    }

# Run simulations
power_density = compute_power_density()
temp_rise = compute_temperature_rise()
steam_flow = compute_steam_flow_rate()
fuel_consumption = compute_fuel_consumption()
safety_margins = compute_safety_margins()

print(f"Core power density: {power_density:.2f} MW/m³")
print(f"Primary loop temperature rise: {temp_rise:.2f} °C")
print(f"Secondary loop steam flow: {steam_flow:.2f} kg/s")
print(f"Annual U-235 consumption: {fuel_consumption:.2f} kg/year")
print(f"Safety margins: Power density {safety_margins['power_density_margin']:.2f}x, Pressure {safety_margins['pressure_margin']:.2f}x")
