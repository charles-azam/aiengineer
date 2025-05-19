"""
Utility tools for SMR design calculations.
"""
from pyforge import Quantity
import math

def calculate_levelized_cost(
    capital_cost: float,
    annual_om_cost: float,
    fuel_cost: float,
    decommissioning_cost: float,
    annual_energy: float,
    discount_rate: float,
    lifetime: int
) -> float:
    """
    Calculate the levelized cost of electricity (LCOE) in $/MWh.
    
    Parameters:
    - capital_cost: Initial capital cost in $
    - annual_om_cost: Annual operations and maintenance cost in $
    - fuel_cost: Annual fuel cost in $
    - decommissioning_cost: End-of-life decommissioning cost in $
    - annual_energy: Annual energy production in MWh
    - discount_rate: Annual discount rate (e.g., 0.07 for 7%)
    - lifetime: Plant lifetime in years
    
    Returns:
    - LCOE in $/MWh
    """
    # Present value of all costs
    pv_capital = capital_cost
    
    pv_om = 0
    pv_fuel = 0
    for year in range(1, lifetime + 1):
        pv_om += annual_om_cost / ((1 + discount_rate) ** year)
        pv_fuel += fuel_cost / ((1 + discount_rate) ** year)
    
    pv_decommissioning = decommissioning_cost / ((1 + discount_rate) ** lifetime)
    
    total_pv_cost = pv_capital + pv_om + pv_fuel + pv_decommissioning
    
    # Present value of energy production
    pv_energy = 0
    for year in range(1, lifetime + 1):
        pv_energy += annual_energy / ((1 + discount_rate) ** year)
    
    # LCOE calculation
    lcoe = total_pv_cost / pv_energy
    
    return lcoe

def calculate_core_power_density(thermal_power: Quantity, core_volume: Quantity) -> Quantity:
    """
    Calculate the power density of the reactor core.
    
    Parameters:
    - thermal_power: Thermal power output
    - core_volume: Volume of the reactor core
    
    Returns:
    - Power density in MW/m³
    """
    power_mw = thermal_power.to('MW').magnitude
    volume_m3 = core_volume.to('m^3').magnitude
    
    power_density = power_mw / volume_m3
    
    return Quantity(power_density, 'MW/m^3')

def calculate_core_volume(height: Quantity, diameter: Quantity) -> Quantity:
    """
    Calculate the volume of a cylindrical reactor core.
    
    Parameters:
    - height: Height of the core
    - diameter: Diameter of the core
    
    Returns:
    - Volume in m³
    """
    height_m = height.to('m').magnitude
    radius_m = diameter.to('m').magnitude / 2
    
    volume = math.pi * (radius_m ** 2) * height_m
    
    return Quantity(volume, 'm^3')

def estimate_construction_time(power_output: Quantity, is_modular: bool = True) -> int:
    """
    Estimate construction time based on power output and construction approach.
    
    Parameters:
    - power_output: Electrical power output
    - is_modular: Whether the construction uses modular approach
    
    Returns:
    - Estimated construction time in months
    """
    power_mw = power_output.to('MW').magnitude
    
    # Base construction time - simplified model
    if is_modular:
        # Modular construction is faster
        base_time = 24 + (power_mw / 50)  # months
    else:
        # Traditional construction takes longer
        base_time = 48 + (power_mw / 25)  # months
    
    return round(base_time)

def calculate_containment_volume(height: Quantity, diameter: Quantity) -> Quantity:
    """
    Calculate the volume of a cylindrical containment structure.
    
    Parameters:
    - height: Height of the containment
    - diameter: Diameter of the containment
    
    Returns:
    - Volume in m³
    """
    height_m = height.to('m').magnitude
    radius_m = diameter.to('m').magnitude / 2
    
    volume = math.pi * (radius_m ** 2) * height_m
    
    return Quantity(volume, 'm^3')
