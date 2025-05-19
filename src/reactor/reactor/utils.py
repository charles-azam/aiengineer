"""
Utility functions for calculations related to the Small Modular Reactor.
"""
import math

def calculate_heat_transfer(flow_rate, delta_t, specific_heat=4.2):
    """
    Calculate heat transfer based on mass flow rate and temperature difference.
    
    Args:
        flow_rate (float): Mass flow rate in kg/s
        delta_t (float): Temperature difference in °C
        specific_heat (float): Specific heat capacity in kJ/kg·K (default: 4.2 for water)
        
    Returns:
        float: Heat transfer in MW
    """
    # Q = m * cp * ΔT
    heat_transfer_kw = flow_rate * specific_heat * delta_t
    heat_transfer_mw = heat_transfer_kw / 1000
    
    return heat_transfer_mw

def calculate_power_density(thermal_power, core_volume):
    """
    Calculate the power density of the reactor core.
    
    Args:
        thermal_power (float): Thermal power in MW
        core_volume (float): Core volume in m³
        
    Returns:
        float: Power density in MW/m³
    """
    return thermal_power / core_volume

def calculate_efficiency(thermal_power, electrical_power):
    """
    Calculate thermal efficiency.
    
    Args:
        thermal_power (float): Thermal power in MW
        electrical_power (float): Electrical power in MW
        
    Returns:
        float: Thermal efficiency as a fraction
    """
    return electrical_power / thermal_power

def calculate_economics(electrical_power, capacity_factor, capital_cost_per_kw, design_life):
    """
    Calculate economic parameters for the SMR.
    
    Args:
        electrical_power (float): Electrical power in MW
        capacity_factor (float): Capacity factor as a fraction
        capital_cost_per_kw (float): Capital cost in $/kW
        design_life (int): Design life in years
        
    Returns:
        dict: Dictionary containing economic parameters
    """
    # Convert MW to kW for capital cost calculation
    electrical_power_kw = electrical_power * 1000
    
    # Calculate capital cost
    capital_cost = electrical_power_kw * capital_cost_per_kw
    
    # Calculate annual electricity production
    hours_per_year = 365 * 24
    annual_production = electrical_power * capacity_factor * hours_per_year
    
    # Calculate levelized cost of electricity (simplified)
    # Assuming O&M costs of $40/MWh and fuel costs of $7/MWh
    annual_om_cost = annual_production * 40
    annual_fuel_cost = annual_production * 7
    
    # Simplified LCOE calculation
    annual_capital_recovery = capital_cost / (design_life * annual_production)
    lcoe = annual_capital_recovery + 40 + 7  # $/MWh
    
    # Estimate construction time based on size
    construction_time = 24 + (electrical_power / 50)  # months
    
    return {
        "capital_cost": capital_cost,
        "annual_production": annual_production,
        "lcoe": lcoe,
        "construction_time": round(construction_time)
    }

def calculate_containment_pressure(power, volume, time):
    """
    Calculate containment pressure following a design basis accident.
    
    Args:
        power (float): Decay heat in MW
        volume (float): Containment free volume in m³
        time (float): Time after accident in seconds
        
    Returns:
        float: Containment pressure in kPa
    """
    # Simplified model for demonstration
    # Assumes ideal gas behavior and complete conversion of decay heat to steam
    
    # Constants
    water_enthalpy = 2000  # kJ/kg
    gas_constant = 8.314  # J/mol·K
    molar_mass = 18  # g/mol for water
    temperature = 400 + 273.15  # K (assumed post-accident temperature)
    
    # Calculate mass of steam generated
    energy = power * 1000 * time  # kJ
    steam_mass = energy / water_enthalpy  # kg
    
    # Calculate pressure increase (simplified ideal gas)
    moles = steam_mass * 1000 / molar_mass
    pressure = moles * gas_constant * temperature / (volume * 1000)  # kPa
    
    # Add atmospheric pressure
    pressure += 101.3  # kPa
    
    return pressure

def calculate_radiation_dose(distance, source_term, time):
    """
    Calculate radiation dose at a given distance from the reactor.
    
    Args:
        distance (float): Distance from reactor in meters
        source_term (float): Source term in TBq
        time (float): Exposure time in hours
        
    Returns:
        float: Radiation dose in mSv
    """
    # Simplified model for demonstration
    # Inverse square law with atmospheric dispersion factor
    
    # Constants
    dose_conversion = 0.02  # mSv/TBq·h at 1 km
    dispersion_factor = 0.1  # Atmospheric dispersion factor
    
    # Calculate dose
    normalized_distance = distance / 1000  # km
    dose = source_term * dose_conversion * dispersion_factor * time / (normalized_distance ** 2)
    
    return dose

if __name__ == "__main__":
    # Example calculations
    print("Utility Function Examples:")
    
    # Heat transfer example
    flow = 320  # kg/s
    delta_t = 35  # °C
    heat = calculate_heat_transfer(flow, delta_t)
    print(f"Heat transfer with flow {flow} kg/s and ΔT {delta_t}°C: {heat:.2f} MW")
    
    # Power density example
    power = 60  # MW
    volume = 6.4  # m³
    density = calculate_power_density(power, volume)
    print(f"Power density with {power} MW in {volume} m³: {density:.2f} MW/m³")
    
    # Economics example
    economics = calculate_economics(20, 0.95, 5000, 60)
    print(f"LCOE for 20 MW SMR: ${economics['lcoe']:.2f}/MWh")
    print(f"Annual production: {economics['annual_production']:,.0f} MWh")
