"""
Economic analysis tools for the Small Modular Reactor project.
"""

from reactor.parameters_reactor import REACTOR_PARAMS

def calculate_lcoe(capital_cost, fuel_cost, om_cost, decommissioning_cost):
    """
    Calculate Levelized Cost of Electricity (LCOE) for the SMR.
    
    Parameters:
    -----------
    capital_cost : float
        Total capital cost in USD
    fuel_cost : float
        Annual fuel cost in USD/year
    om_cost : float
        Annual operations and maintenance cost in USD/year
    decommissioning_cost : float
        Total decommissioning cost in USD
        
    Returns:
    --------
    float
        LCOE in USD/MWh
    """
    # Parameters
    power = REACTOR_PARAMS.electrical_power.magnitude  # MW
    lifetime = REACTOR_PARAMS.design_lifetime.magnitude  # years
    
    print(f"DEBUG: power={power}, lifetime={lifetime}")
    capacity_factor = 0.90  # typical for nuclear
    discount_rate = 0.07  # 7% discount rate
    
    # Calculate annual electricity production
    annual_production = power * 8760 * capacity_factor  # MWh/year
    
    # Calculate present value of costs
    pv_capital = capital_cost
    
    pv_fuel = 0
    pv_om = 0
    for year in range(1, int(lifetime) + 1):
        pv_fuel += fuel_cost / ((1 + discount_rate) ** year)
        pv_om += om_cost / ((1 + discount_rate) ** year)
    
    pv_decommissioning = decommissioning_cost / ((1 + discount_rate) ** lifetime)
    
    total_pv_cost = pv_capital + pv_fuel + pv_om + pv_decommissioning
    
    # Calculate present value of electricity production
    pv_production = 0
    for year in range(1, int(lifetime) + 1):
        pv_production += annual_production / ((1 + discount_rate) ** year)
    
    # Calculate LCOE
    lcoe = total_pv_cost / pv_production  # USD/MWh
    
    return lcoe

def estimate_smr_costs():
    """
    Estimate costs for the 20 MW SMR based on industry benchmarks.
    """
    # Cost estimates based on industry data for small modular reactors
    # These are simplified estimates and would vary based on many factors
    
    power = REACTOR_PARAMS.electrical_power.magnitude  # MW
    
    # Capital cost (overnight cost)
    # Using $5000-7000/kW as benchmark for SMRs
    capital_cost_per_kw = 6000  # USD/kW
    capital_cost = capital_cost_per_kw * power * 1000  # USD
    
    # Fuel cost
    # Using $5-10/MWh as benchmark for nuclear fuel
    fuel_cost_per_mwh = 7  # USD/MWh
    capacity_factor = 0.90
    annual_production = power * 8760 * capacity_factor  # MWh/year
    annual_fuel_cost = fuel_cost_per_mwh * annual_production  # USD/year
    
    # Operations and maintenance cost
    # Using $25-35/MWh as benchmark for nuclear O&M
    om_cost_per_mwh = 30  # USD/MWh
    annual_om_cost = om_cost_per_mwh * annual_production  # USD/year
    
    # Decommissioning cost
    # Using 15-20% of capital cost as benchmark
    decommissioning_factor = 0.15
    decommissioning_cost = capital_cost * decommissioning_factor  # USD
    
    # Calculate LCOE
    lcoe = calculate_lcoe(capital_cost, annual_fuel_cost, annual_om_cost, decommissioning_cost)
    
    print(f"Economic Analysis for {power} MW SMR:")
    print(f"Capital Cost: ${capital_cost/1e6:.2f} million (${capital_cost_per_kw}/kW)")
    print(f"Annual Fuel Cost: ${annual_fuel_cost/1e3:.2f} thousand (${fuel_cost_per_mwh}/MWh)")
    print(f"Annual O&M Cost: ${annual_om_cost/1e3:.2f} thousand (${om_cost_per_mwh}/MWh)")
    print(f"Decommissioning Cost: ${decommissioning_cost/1e6:.2f} million")
    print(f"Levelized Cost of Electricity (LCOE): ${lcoe:.2f}/MWh")
    
    # Compare with other energy sources
    print("\nLCOE Comparison with Other Energy Sources:")
    print(f"SMR Nuclear: ${lcoe:.2f}/MWh")
    print(f"Large Nuclear: $85-95/MWh")
    print(f"Natural Gas: $45-75/MWh")
    print(f"Coal: $65-150/MWh")
    print(f"Solar PV: $35-55/MWh")
    print(f"Wind: $30-60/MWh")
    
    return {
        "capital_cost": capital_cost,
        "annual_fuel_cost": annual_fuel_cost,
        "annual_om_cost": annual_om_cost,
        "decommissioning_cost": decommissioning_cost,
        "lcoe": lcoe
    }

# Run economic analysis
print("\n=== ECONOMIC ANALYSIS ===\n")
cost_results = estimate_smr_costs()
