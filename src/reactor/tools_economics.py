"""
Economic analysis tools for the small modular reactor project.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
import numpy as np

def calculate_lcoe(
    overnight_cost_per_kw: float = 5000,  # $/kW
    capacity_factor: float = 0.9,
    discount_rate: float = 0.07,
    fuel_cost_per_mwh: float = 7,  # $/MWh
    om_cost_per_mwh: float = 25,  # $/MWh
    decommissioning_cost_per_kw: float = 500,  # $/kW
) -> float:
    """
    Calculate the Levelized Cost of Electricity (LCOE) in $/MWh.
    
    Args:
        overnight_cost_per_kw: Construction cost in $/kW
        capacity_factor: Average capacity factor (0-1)
        discount_rate: Annual discount rate (0-1)
        fuel_cost_per_mwh: Fuel cost in $/MWh
        om_cost_per_mwh: Operations and maintenance cost in $/MWh
        decommissioning_cost_per_kw: Decommissioning cost in $/kW
        
    Returns:
        LCOE in $/MWh
    """
    # Plant parameters
    power_kw = REACTOR_PARAMS.electrical_power.magnitude * 1000  # kW
    lifetime_years = REACTOR_PARAMS.design_life  # years
    
    # Capital costs
    overnight_cost = overnight_cost_per_kw * power_kw  # $
    
    # Construction period (simplified to 3 years with equal spending)
    construction_years = 3
    annual_construction_cost = overnight_cost / construction_years
    
    # Calculate present value of capital costs
    capital_pv = 0
    for year in range(construction_years):
        capital_pv += annual_construction_cost / ((1 + discount_rate) ** year)
    
    # Calculate present value of decommissioning costs
    decommissioning_cost = decommissioning_cost_per_kw * power_kw
    decommissioning_pv = decommissioning_cost / ((1 + discount_rate) ** lifetime_years)
    
    # Total present value of costs
    total_capital_pv = capital_pv + decommissioning_pv
    
    # Annual electricity production
    annual_mwh = power_kw * 8760 * capacity_factor / 1000  # MWh
    
    # Calculate present value of electricity production
    electricity_pv = 0
    for year in range(construction_years, construction_years + lifetime_years):
        electricity_pv += annual_mwh / ((1 + discount_rate) ** year)
    
    # Calculate capital component of LCOE
    lcoe_capital = total_capital_pv / electricity_pv
    
    # Add fuel and O&M costs
    lcoe_total = lcoe_capital + fuel_cost_per_mwh + om_cost_per_mwh
    
    return lcoe_total

def calculate_payback_period(
    overnight_cost_per_kw: float = 5000,  # $/kW
    electricity_price_per_mwh: float = 85,  # $/MWh
    capacity_factor: float = 0.9,
    annual_costs_per_mwh: float = 32,  # $/MWh (fuel + O&M)
) -> float:
    """
    Calculate the simple payback period in years.
    
    Args:
        overnight_cost_per_kw: Construction cost in $/kW
        electricity_price_per_mwh: Electricity selling price in $/MWh
        capacity_factor: Average capacity factor (0-1)
        annual_costs_per_mwh: Annual operating costs in $/MWh
        
    Returns:
        Payback period in years
    """
    # Plant parameters
    power_kw = REACTOR_PARAMS.electrical_power.magnitude * 1000  # kW
    
    # Total capital cost
    total_cost = overnight_cost_per_kw * power_kw  # $
    
    # Annual electricity production
    annual_mwh = power_kw * 8760 * capacity_factor / 1000  # MWh
    
    # Annual revenue
    annual_revenue = annual_mwh * electricity_price_per_mwh  # $
    
    # Annual costs
    annual_costs = annual_mwh * annual_costs_per_mwh  # $
    
    # Annual net cash flow
    annual_net_cash_flow = annual_revenue - annual_costs  # $
    
    # Simple payback period
    payback_period = total_cost / annual_net_cash_flow  # years
    
    return payback_period

# Run economic analysis
lcoe = calculate_lcoe()
payback = calculate_payback_period()

print(f"Levelized Cost of Electricity (LCOE): ${lcoe:.2f}/MWh")
print(f"Simple payback period: {payback:.2f} years")
