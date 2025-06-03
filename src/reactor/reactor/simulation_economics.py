"""
Economic simulation module for HTGR systems.

This module provides simple models for calculating economic metrics
such as levelized cost of heat (LCOH) and comparative analysis with
other heating technologies.
"""

from pyforge import Quantity
from reactor.reactor.parameters_deployment import DEPLOYMENT_PARAMS

def calculate_lcoh() -> float:
    """
    Calculate the Levelized Cost of Heat (LCOH) for the HTGR system.
    
    Returns:
        LCOH in $/MWh thermal
    """
    # Simplified LCOH calculation
    # In a real implementation, this would use detailed economic models
    
    # Parameters from deployment parameters
    capital_cost_per_kw = DEPLOYMENT_PARAMS.capital_cost_per_kw  # $/kWth
    om_cost_per_kw_year = DEPLOYMENT_PARAMS.annual_om_cost_per_kw  # $/kW-year
    
    # Other assumed parameters
    capacity_factor = 0.9
    discount_rate = 0.07
    plant_lifetime = 20  # years
    fuel_cost_per_mwh = 7.5  # $/MWh
    
    # Calculate capital recovery factor
    crf = discount_rate * (1 + discount_rate)**plant_lifetime / ((1 + discount_rate)**plant_lifetime - 1)
    
    # Calculate LCOH components
    capital_component = capital_cost_per_kw * 1000 * crf / (8760 * capacity_factor)  # $/MWh
    fuel_component = fuel_cost_per_mwh  # $/MWh
    om_component = om_cost_per_kw_year * 1000 / (8760 * capacity_factor)  # $/MWh
    
    # Total LCOH
    lcoh = capital_component + fuel_component + om_component
    
    print(f"Calculated LCOH: ${lcoh:.2f}/MWh thermal")
    return lcoh

def evaluate_passive_safety_performance():
    """
    Evaluate the passive safety performance of the HTGR design.
    
    Returns:
        Dictionary containing key safety performance metrics
    """
    # Sample safety performance metrics
    # In a real implementation, this would use detailed physics models
    
    lofc_peak_temp = Quantity(1250, "°C")
    depressurization_peak_temp = Quantity(1350, "°C")
    reactivity_peak_temp = Quantity(1100, "°C")
    
    return {
        "lofc_peak_temp": lofc_peak_temp,
        "depressurization_peak_temp": depressurization_peak_temp,
        "reactivity_peak_temp": reactivity_peak_temp,
        "passive_cooling_sufficient": True,
        "fission_product_retention": 0.9999
    }

print("Economic simulation module loaded successfully")
