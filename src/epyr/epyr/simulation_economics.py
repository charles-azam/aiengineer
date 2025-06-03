"""
Economic analysis tools for thermal energy storage systems.

This module provides functions to calculate economic metrics for thermal storage systems
and compare them with conventional heating alternatives.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from pyforge import Parameters
from epyr.tools_units import Quantity, UNIT_REGISTRY

# Import necessary parameters from other modules

from epyr.parameters_industrial_applications import (
    IndustrialApplication,
    HeatProfile,
    ALL_INDUSTRIAL_APPLICATIONS
)

# Economic parameters
class EconomicParameters(Parameters):
    """Economic parameters for thermal storage system analysis."""
    discount_rate: float = 0.08  # 8% discount rate
    electricity_price: Quantity = Quantity(0.12, "USD_per_kWh")
    natural_gas_price: Quantity = Quantity(8.5, "USD/MMBtu")
    oil_price: Quantity = Quantity(70, "USD/barrel")
    carbon_price: Quantity = Quantity(50, "USD_per_tonne")
    project_lifetime: int = 20  # years
    maintenance_factor: float = 0.02  # 2% of CAPEX per year
    inflation_rate: float = 0.025  # 2.5% annual inflation

# Single source of truth
ECONOMIC_PARAMS = EconomicParameters()

# Emission factors (kg CO2e per kWh thermal)
EMISSION_FACTORS = {
    "natural_gas": 0.2,
    "oil": 0.27,
    "coal": 0.34,
    "electricity_grid_avg": 0.15,
    "electricity_renewable": 0.01,
}

# CAPEX Models
def calculate_thermal_storage_capex(
    capacity: Quantity,
    storage_duration: Quantity,
    material_type: str,
    include_power_equipment: bool = True
) -> Quantity:
    """
    Calculate capital expenditure for thermal storage system.
    
    Args:
        capacity: Thermal power capacity
        storage_duration: Hours of storage at full capacity
        material_type: Type of storage material
        include_power_equipment: Whether to include power conversion equipment
        
    Returns:
        Total capital expenditure in USD
    """
    # Base costs for different storage materials (USD/kWh)
    material_costs = {
        "molten_salt": 40,
        "solid_ceramic": 30,
        "high_temp_ceramic": 45,
        "molten_metal": 65,
        "phase_change_material": 55,
    }
    
    # Convert capacity to kW if not already
    capacity_kw = capacity.to("kW").magnitude
    duration_h = storage_duration.to("hour").magnitude
    
    # Calculate storage component cost
    storage_capacity_kwh = capacity_kw * duration_h
    material_cost_per_kwh = material_costs.get(material_type.lower(), 40)
    storage_cost = storage_capacity_kwh * material_cost_per_kwh
    
    # Power equipment costs (USD/kW)
    power_equipment_cost = 200 * capacity_kw if include_power_equipment else 0
    
    # Balance of plant costs (USD)
    bop_cost = 100000 + (0.1 * storage_cost)
    
    # Engineering and installation (25% of equipment costs)
    engineering_cost = 0.25 * (storage_cost + power_equipment_cost + bop_cost)
    
    # Total CAPEX
    total_capex = storage_cost + power_equipment_cost + bop_cost + engineering_cost
    
    # Scale factor for economies of scale
    if capacity_kw > 1000:
        total_capex *= 0.85  # 15% discount for large systems
    elif capacity_kw < 100:
        total_capex *= 1.2  # 20% premium for small systems
    
    print(f"Thermal storage CAPEX: ${total_capex:,.2f} for {capacity_kw} kW with {duration_h} hours storage")
    return Quantity(total_capex, "USD")

def calculate_conventional_heating_capex(
    capacity: Quantity,
    system_type: str
) -> Quantity:
    """
    Calculate capital expenditure for conventional heating systems.
    
    Args:
        capacity: Heating capacity
        system_type: Type of heating system (natural_gas, oil, electric, chp)
        
    Returns:
        Total capital expenditure in USD
    """
    # Base costs for different heating systems (USD/kW)
    system_costs = {
        "natural_gas": 150,
        "oil": 180,
        "electric": 100,
        "chp": 800,
    }
    
    # Convert capacity to kW if not already
    capacity_kw = capacity.to("kW").magnitude
    
    # Get base cost for system type
    base_cost_per_kw = system_costs.get(system_type.lower(), 200)
    
    # Calculate equipment cost
    equipment_cost = capacity_kw * base_cost_per_kw
    
    # Installation and engineering (40% of equipment cost)
    installation_cost = 0.4 * equipment_cost
    
    # Balance of plant
    bop_cost = 50000 + (0.05 * equipment_cost)
    
    # Total CAPEX
    total_capex = equipment_cost + installation_cost + bop_cost
    
    # Scale factor for economies of scale
    if capacity_kw > 1000:
        total_capex *= 0.9  # 10% discount for large systems
    elif capacity_kw < 100:
        total_capex *= 1.15  # 15% premium for small systems
    
    print(f"{system_type.title()} heating system CAPEX: ${total_capex:,.2f} for {capacity_kw} kW")
    return Quantity(total_capex, "USD")

# OPEX Models
def calculate_thermal_storage_opex(
    capex: Quantity,
    annual_energy_output: Quantity,
    electricity_price: Optional[Quantity] = None,
    maintenance_factor: Optional[float] = None,
    round_trip_efficiency: float = 0.85
) -> Quantity:
    """
    Calculate annual operational expenditure for thermal storage system.
    
    Args:
        capex: Capital expenditure
        annual_energy_output: Annual thermal energy output
        electricity_price: Price of electricity (defaults to ECONOMIC_PARAMS)
        maintenance_factor: Annual maintenance as fraction of CAPEX
        round_trip_efficiency: Thermal storage round-trip efficiency
        
    Returns:
        Annual operational expenditure in USD/year
    """
    # Use default parameters if not provided
    if electricity_price is None:
        electricity_price = ECONOMIC_PARAMS.electricity_price
    if maintenance_factor is None:
        maintenance_factor = ECONOMIC_PARAMS.maintenance_factor
    
    # Convert to consistent units
    capex_usd = capex.to("USD").magnitude
    annual_energy_mwh = annual_energy_output.to("MWh").magnitude
    electricity_price_per_mwh = electricity_price.to("USD/MWh").magnitude
    
    # Calculate maintenance costs
    maintenance_cost = capex_usd * maintenance_factor
    
    # Calculate electricity costs for charging
    electricity_cost = (annual_energy_mwh / round_trip_efficiency) * electricity_price_per_mwh
    
    # Other fixed operating costs
    fixed_operating_cost = 20000 + (0.01 * capex_usd)
    
    # Total OPEX
    total_opex = maintenance_cost + electricity_cost + fixed_operating_cost
    
    print(f"Thermal storage annual OPEX: ${total_opex:,.2f}")
    return Quantity(total_opex, "USD/year")

def calculate_conventional_heating_opex(
    capex: Quantity,
    annual_energy_output: Quantity,
    system_type: str,
    fuel_price: Optional[Quantity] = None,
    maintenance_factor: Optional[float] = None
) -> Quantity:
    """
    Calculate annual operational expenditure for conventional heating system.
    
    Args:
        capex: Capital expenditure
        annual_energy_output: Annual thermal energy output
        system_type: Type of heating system (natural_gas, oil, electric, chp)
        fuel_price: Price of fuel (defaults to ECONOMIC_PARAMS)
        maintenance_factor: Annual maintenance as fraction of CAPEX
        
    Returns:
        Annual operational expenditure in USD/year
    """
    # Use default parameters if not provided
    if maintenance_factor is None:
        maintenance_factor = ECONOMIC_PARAMS.maintenance_factor * 1.5  # Higher maintenance for conventional
    
    # Convert to consistent units
    capex_usd = capex.to("USD").magnitude
    annual_energy_mwh = annual_energy_output.to("MWh").magnitude
    
    # System efficiencies
    efficiencies = {
        "natural_gas": 0.85,
        "oil": 0.80,
        "electric": 0.99,
        "chp": 0.75,  # thermal efficiency only
    }
    
    efficiency = efficiencies.get(system_type.lower(), 0.8)
    
    # Calculate maintenance costs
    maintenance_cost = capex_usd * maintenance_factor
    
    # Calculate fuel costs based on system type
    if system_type.lower() == "natural_gas":
        if fuel_price is None:
            fuel_price = ECONOMIC_PARAMS.natural_gas_price
        # Convert MWh to MMBtu
        energy_mmbtu = annual_energy_mwh * 3.412  # 1 MWh = 3.412 MMBtu
        fuel_cost = (energy_mmbtu / efficiency) * fuel_price.to("USD/MMBtu").magnitude
    
    elif system_type.lower() == "oil":
        if fuel_price is None:
            fuel_price = ECONOMIC_PARAMS.oil_price
        # Convert MWh to barrels (approximately 1.7 MWh per barrel)
        energy_barrels = annual_energy_mwh / 1.7
        fuel_cost = (energy_barrels / efficiency) * fuel_price.to("USD/barrel").magnitude
    
    elif system_type.lower() == "electric":
        if fuel_price is None:
            fuel_price = ECONOMIC_PARAMS.electricity_price
        fuel_cost = (annual_energy_mwh / efficiency) * fuel_price.to("USD/MWh").magnitude
    
    elif system_type.lower() == "chp":
        if fuel_price is None:
            fuel_price = ECONOMIC_PARAMS.natural_gas_price
        # CHP typically uses natural gas
        energy_mmbtu = annual_energy_mwh * 3.412
        fuel_cost = (energy_mmbtu / efficiency) * fuel_price.to("USD/MMBtu").magnitude
        # Offset by electricity generation (assuming 35% electrical efficiency)
        electricity_generation = annual_energy_mwh * 0.35 / 0.75
        electricity_value = electricity_generation * ECONOMIC_PARAMS.electricity_price.to("USD/MWh").magnitude
        fuel_cost -= electricity_value
    
    else:
        # Default to natural gas if system type not recognized
        energy_mmbtu = annual_energy_mwh * 3.412
        fuel_cost = (energy_mmbtu / 0.8) * ECONOMIC_PARAMS.natural_gas_price.to("USD/MMBtu").magnitude
    
    # Other fixed operating costs
    fixed_operating_cost = 10000 + (0.015 * capex_usd)
    
    # Total OPEX
    total_opex = maintenance_cost + fuel_cost + fixed_operating_cost
    
    print(f"{system_type.title()} heating system annual OPEX: ${total_opex:,.2f}")
    return Quantity(total_opex, "USD/year")

# Economic Analysis Functions
def calculate_lcoh(
    capex: Quantity,
    annual_opex: Quantity,
    annual_energy_output: Quantity,
    project_lifetime: int = None,
    discount_rate: float = None
) -> Quantity:
    """
    Calculate Levelized Cost of Heat (LCOH).
    
    Args:
        capex: Capital expenditure
        annual_opex: Annual operational expenditure
        annual_energy_output: Annual thermal energy output
        project_lifetime: Project lifetime in years
        discount_rate: Discount rate for NPV calculation
        
    Returns:
        LCOH in USD/MWh
    """
    # Use default parameters if not provided
    if project_lifetime is None:
        project_lifetime = ECONOMIC_PARAMS.project_lifetime
    if discount_rate is None:
        discount_rate = ECONOMIC_PARAMS.discount_rate
    
    # Convert to consistent units
    capex_usd = capex.to("USD").magnitude
    annual_opex_usd = annual_opex.to("USD/year").magnitude
    annual_energy_mwh = annual_energy_output.to("MWh").magnitude
    
    # Calculate present value of all costs
    total_pv_cost = capex_usd
    total_pv_energy = 0
    
    for year in range(1, project_lifetime + 1):
        # Present value of OPEX for this year
        pv_opex = annual_opex_usd / ((1 + discount_rate) ** year)
        total_pv_cost += pv_opex
        
        # Present value of energy for this year
        pv_energy = annual_energy_mwh / ((1 + discount_rate) ** year)
        total_pv_energy += pv_energy
    
    # Calculate LCOH
    lcoh = total_pv_cost / total_pv_energy
    
    print(f"Levelized Cost of Heat (LCOH): ${lcoh:.2f}/MWh")
    return Quantity(lcoh, "USD_per_MWh")

def calculate_carbon_emissions(
    annual_energy_output: Quantity,
    system_type: str,
    grid_emission_factor: float = None
) -> Quantity:
    """
    Calculate annual carbon emissions for a heating system.
    
    Args:
        annual_energy_output: Annual thermal energy output
        system_type: Type of heating system
        grid_emission_factor: Emission factor for grid electricity
        
    Returns:
        Annual carbon emissions in tonnes CO2e
    """
    # Use default emission factor if not provided
    if grid_emission_factor is None:
        grid_emission_factor = EMISSION_FACTORS["electricity_grid_avg"]
    
    # Convert to consistent units
    annual_energy_mwh = annual_energy_output.to("MWh").magnitude
    
    # System efficiencies
    efficiencies = {
        "natural_gas": 0.85,
        "oil": 0.80,
        "electric": 0.99,
        "chp": 0.75,
        "thermal_storage": 0.85,
    }
    
    efficiency = efficiencies.get(system_type.lower(), 0.8)
    
    # Calculate emissions based on system type
    if system_type.lower() == "natural_gas":
        emissions_factor = EMISSION_FACTORS["natural_gas"]
        emissions = (annual_energy_mwh / efficiency) * emissions_factor
    
    elif system_type.lower() == "oil":
        emissions_factor = EMISSION_FACTORS["oil"]
        emissions = (annual_energy_mwh / efficiency) * emissions_factor
    
    elif system_type.lower() == "electric":
        emissions = (annual_energy_mwh / efficiency) * grid_emission_factor
    
    elif system_type.lower() == "chp":
        # CHP has lower emissions due to combined generation
        emissions_factor = EMISSION_FACTORS["natural_gas"] * 0.7  # 30% reduction due to efficiency
        emissions = (annual_energy_mwh / efficiency) * emissions_factor
    
    elif system_type.lower() == "thermal_storage":
        # Thermal storage emissions depend on charging source
        emissions = (annual_energy_mwh / efficiency) * grid_emission_factor
    
    else:
        # Default to natural gas if system type not recognized
        emissions_factor = EMISSION_FACTORS["natural_gas"]
        emissions = (annual_energy_mwh / 0.8) * emissions_factor
    
    # Convert from kg to tonnes
    emissions_tonnes = emissions / 1000
    
    print(f"{system_type.title()} annual carbon emissions: {emissions_tonnes:.2f} tonnes CO2e")
    return Quantity(emissions_tonnes, "tonne")

def calculate_payback_period(
    thermal_storage_capex: Quantity,
    conventional_capex: Quantity,
    thermal_storage_opex: Quantity,
    conventional_opex: Quantity,
    carbon_price: Optional[Quantity] = None,
    carbon_savings: Optional[Quantity] = None
) -> float:
    """
    Calculate simple payback period for thermal storage vs conventional system.
    
    Args:
        thermal_storage_capex: Capital expenditure for thermal storage
        conventional_capex: Capital expenditure for conventional system
        thermal_storage_opex: Annual OPEX for thermal storage
        conventional_opex: Annual OPEX for conventional system
        carbon_price: Price per tonne of CO2e (optional)
        carbon_savings: Annual carbon savings in tonnes (optional)
        
    Returns:
        Payback period in years
    """
    # Convert to consistent units
    ts_capex = thermal_storage_capex.to("USD").magnitude
    conv_capex = conventional_capex.to("USD").magnitude
    ts_opex = thermal_storage_opex.to("USD/year").magnitude
    conv_opex = conventional_opex.to("USD/year").magnitude
    
    # Calculate additional upfront investment
    additional_investment = ts_capex - conv_capex
    
    # Calculate annual savings
    annual_opex_savings = conv_opex - ts_opex
    
    # Add carbon savings if applicable
    if carbon_price is not None and carbon_savings is not None:
        carbon_price_usd = carbon_price.to("USD/tonne").magnitude
        carbon_savings_tonnes = carbon_savings.to("tonne").magnitude
        annual_carbon_value = carbon_price_usd * carbon_savings_tonnes
        annual_opex_savings += annual_carbon_value
    
    # Calculate payback period
    if annual_opex_savings <= 0:
        payback_period = float('inf')  # No payback
    else:
        payback_period = additional_investment / annual_opex_savings
    
    if payback_period == float('inf'):
        print("No payback - thermal storage has higher lifetime costs")
    else:
        print(f"Payback period: {payback_period:.2f} years")
    
    return payback_period

def calculate_roi(
    thermal_storage_capex: Quantity,
    conventional_capex: Quantity,
    thermal_storage_opex: Quantity,
    conventional_opex: Quantity,
    project_lifetime: int = None,
    discount_rate: float = None,
    carbon_price: Optional[Quantity] = None,
    carbon_savings: Optional[Quantity] = None
) -> float:
    """
    Calculate ROI for thermal storage vs conventional system.
    
    Args:
        thermal_storage_capex: Capital expenditure for thermal storage
        conventional_capex: Capital expenditure for conventional system
        thermal_storage_opex: Annual OPEX for thermal storage
        conventional_opex: Annual OPEX for conventional system
        project_lifetime: Project lifetime in years
        discount_rate: Discount rate for NPV calculation
        carbon_price: Price per tonne of CO2e (optional)
        carbon_savings: Annual carbon savings in tonnes (optional)
        
    Returns:
        ROI as a percentage
    """
    # Use default parameters if not provided
    if project_lifetime is None:
        project_lifetime = ECONOMIC_PARAMS.project_lifetime
    if discount_rate is None:
        discount_rate = ECONOMIC_PARAMS.discount_rate
    
    # Convert to consistent units
    ts_capex = thermal_storage_capex.to("USD").magnitude
    conv_capex = conventional_capex.to("USD").magnitude
    ts_opex = thermal_storage_opex.to("USD/year").magnitude
    conv_opex = conventional_opex.to("USD/year").magnitude
    
    # Calculate additional upfront investment
    additional_investment = ts_capex - conv_capex
    
    # Calculate NPV of savings
    npv_savings = 0
    
    for year in range(1, project_lifetime + 1):
        # Annual OPEX savings
        annual_opex_savings = conv_opex - ts_opex
        
        # Add carbon savings if applicable
        if carbon_price is not None and carbon_savings is not None:
            carbon_price_usd = carbon_price.to("USD/tonne").magnitude
            carbon_savings_tonnes = carbon_savings.to("tonne").magnitude
            annual_carbon_value = carbon_price_usd * carbon_savings_tonnes
            annual_opex_savings += annual_carbon_value
        
        # Present value of savings for this year
        pv_savings = annual_opex_savings / ((1 + discount_rate) ** year)
        npv_savings += pv_savings
    
    # Calculate ROI
    if additional_investment <= 0:
        # If thermal storage is cheaper upfront, ROI is infinite
        roi = float('inf')
    else:
        roi = (npv_savings - additional_investment) / additional_investment * 100
    
    if roi == float('inf'):
        print("ROI: Infinite (thermal storage has lower upfront cost)")
    else:
        print(f"ROI: {roi:.2f}%")
    
    return roi

def sensitivity_analysis(
    capacity: Quantity,
    storage_duration: Quantity,
    annual_energy_output: Quantity,
    material_type: str = "solid_ceramic",
    conventional_system: str = "natural_gas",
    parameter_ranges: Dict[str, List[float]] = None
) -> pd.DataFrame:
    """
    Perform sensitivity analysis on key economic parameters.
    
    Args:
        capacity: Thermal power capacity
        storage_duration: Hours of storage at full capacity
        annual_energy_output: Annual thermal energy output
        material_type: Type of storage material
        conventional_system: Type of conventional system to compare against
        parameter_ranges: Dict of parameters and their test ranges
        
    Returns:
        DataFrame with sensitivity analysis results
    """
    # Default parameter ranges if not provided
    if parameter_ranges is None:
        parameter_ranges = {
            "electricity_price": [0.08, 0.10, 0.12, 0.14, 0.16],  # USD/kWh
            "natural_gas_price": [6, 8, 10, 12, 14],  # USD/MMBtu
            "carbon_price": [0, 25, 50, 75, 100],  # USD/tonne
            "discount_rate": [0.05, 0.07, 0.08, 0.10, 0.12],
            "project_lifetime": [10, 15, 20, 25, 30],
        }
    
    results = []
    
    # Base case calculations
    ts_capex = calculate_thermal_storage_capex(capacity, storage_duration, material_type)
    conv_capex = calculate_conventional_heating_capex(capacity, conventional_system)
    
    ts_opex = calculate_thermal_storage_opex(ts_capex, annual_energy_output)
    conv_opex = calculate_conventional_heating_opex(conv_capex, annual_energy_output, conventional_system)
    
    ts_emissions = calculate_carbon_emissions(annual_energy_output, "thermal_storage")
    conv_emissions = calculate_carbon_emissions(annual_energy_output, conventional_system)
    carbon_savings = conv_emissions - ts_emissions
    
    base_lcoh = calculate_lcoh(ts_capex, ts_opex, annual_energy_output)
    base_payback = calculate_payback_period(ts_capex, conv_capex, ts_opex, conv_opex, 
                                           ECONOMIC_PARAMS.carbon_price, carbon_savings)
    base_roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                            ECONOMIC_PARAMS.project_lifetime, ECONOMIC_PARAMS.discount_rate,
                            ECONOMIC_PARAMS.carbon_price, carbon_savings)
    
    # Add base case to results
    results.append({
        "parameter": "Base Case",
        "value": "Base",
        "lcoh_usd_per_mwh": base_lcoh.magnitude,
        "payback_years": base_payback,
        "roi_percent": base_roi
    })
    
    # Test electricity price sensitivity
    for elec_price in parameter_ranges["electricity_price"]:
        temp_params = EconomicParameters()
        temp_params.electricity_price = Quantity(elec_price, "USD/kWh")
        
        ts_opex = calculate_thermal_storage_opex(ts_capex, annual_energy_output, 
                                               electricity_price=temp_params.electricity_price)
        
        lcoh = calculate_lcoh(ts_capex, ts_opex, annual_energy_output)
        payback = calculate_payback_period(ts_capex, conv_capex, ts_opex, conv_opex, 
                                          ECONOMIC_PARAMS.carbon_price, carbon_savings)
        roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                           ECONOMIC_PARAMS.project_lifetime, ECONOMIC_PARAMS.discount_rate,
                           ECONOMIC_PARAMS.carbon_price, carbon_savings)
        
        results.append({
            "parameter": "Electricity Price (USD/kWh)",
            "value": elec_price,
            "lcoh_usd_per_mwh": lcoh.magnitude,
            "payback_years": payback,
            "roi_percent": roi
        })
    
    # Test natural gas price sensitivity
    for gas_price in parameter_ranges["natural_gas_price"]:
        temp_params = EconomicParameters()
        temp_params.natural_gas_price = Quantity(gas_price, "USD/MMBtu")
        
        conv_opex = calculate_conventional_heating_opex(conv_capex, annual_energy_output, 
                                                      conventional_system, 
                                                      fuel_price=temp_params.natural_gas_price)
        
        payback = calculate_payback_period(ts_capex, conv_capex, ts_opex, conv_opex, 
                                          ECONOMIC_PARAMS.carbon_price, carbon_savings)
        roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                           ECONOMIC_PARAMS.project_lifetime, ECONOMIC_PARAMS.discount_rate,
                           ECONOMIC_PARAMS.carbon_price, carbon_savings)
        
        results.append({
            "parameter": "Natural Gas Price (USD/MMBtu)",
            "value": gas_price,
            "lcoh_usd_per_mwh": base_lcoh.magnitude,  # LCOH of thermal storage doesn't change
            "payback_years": payback,
            "roi_percent": roi
        })
    
    # Test carbon price sensitivity
    for carbon_price in parameter_ranges["carbon_price"]:
        temp_carbon_price = Quantity(carbon_price, "USD/tonne")
        
        payback = calculate_payback_period(ts_capex, conv_capex, ts_opex, conv_opex, 
                                          temp_carbon_price, carbon_savings)
        roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                           ECONOMIC_PARAMS.project_lifetime, ECONOMIC_PARAMS.discount_rate,
                           temp_carbon_price, carbon_savings)
        
        results.append({
            "parameter": "Carbon Price (USD/tonne)",
            "value": carbon_price,
            "lcoh_usd_per_mwh": base_lcoh.magnitude,  # LCOH doesn't change with carbon price
            "payback_years": payback,
            "roi_percent": roi
        })
    
    # Test discount rate sensitivity
    for discount_rate in parameter_ranges["discount_rate"]:
        lcoh = calculate_lcoh(ts_capex, ts_opex, annual_energy_output, 
                             ECONOMIC_PARAMS.project_lifetime, discount_rate)
        
        roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                           ECONOMIC_PARAMS.project_lifetime, discount_rate,
                           ECONOMIC_PARAMS.carbon_price, carbon_savings)
        
        results.append({
            "parameter": "Discount Rate",
            "value": discount_rate,
            "lcoh_usd_per_mwh": lcoh.magnitude,
            "payback_years": base_payback,  # Simple payback doesn't change with discount rate
            "roi_percent": roi
        })
    
    # Test project lifetime sensitivity
    for lifetime in parameter_ranges["project_lifetime"]:
        lcoh = calculate_lcoh(ts_capex, ts_opex, annual_energy_output, 
                             lifetime, ECONOMIC_PARAMS.discount_rate)
        
        roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                           lifetime, ECONOMIC_PARAMS.discount_rate,
                           ECONOMIC_PARAMS.carbon_price, carbon_savings)
        
        results.append({
            "parameter": "Project Lifetime (years)",
            "value": lifetime,
            "lcoh_usd_per_mwh": lcoh.magnitude,
            "payback_years": base_payback,  # Simple payback doesn't change with lifetime
            "roi_percent": roi
        })
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    print(f"Sensitivity analysis complete with {len(results_df)} scenarios")
    
    return results_df

def optimize_system_sizing(
    min_capacity: Quantity,
    max_capacity: Quantity,
    min_duration: Quantity,
    max_duration: Quantity,
    annual_energy_demand: Quantity,
    material_type: str = "solid_ceramic",
    conventional_system: str = "natural_gas",
    steps: int = 5
) -> Dict:
    """
    Optimize thermal storage system sizing based on economic metrics.
    
    Args:
        min_capacity: Minimum thermal power capacity to consider
        max_capacity: Maximum thermal power capacity to consider
        min_duration: Minimum storage duration to consider
        max_duration: Maximum storage duration to consider
        annual_energy_demand: Annual thermal energy demand
        material_type: Type of storage material
        conventional_system: Type of conventional system to compare against
        steps: Number of steps for each parameter in the optimization grid
        
    Returns:
        Dict with optimal system configuration and metrics
    """
    # Convert to consistent units
    min_capacity_kw = min_capacity.to("kW").magnitude
    max_capacity_kw = max_capacity.to("kW").magnitude
    min_duration_h = min_duration.to("hour").magnitude
    max_duration_h = max_duration.to("hour").magnitude
    
    # Create parameter grids
    capacity_values = np.linspace(min_capacity_kw, max_capacity_kw, steps)
    duration_values = np.linspace(min_duration_h, max_duration_h, steps)
    
    best_config = {
        "capacity": None,
        "duration": None,
        "lcoh": float('inf'),
        "payback": float('inf'),
        "roi": float('-inf'),
        "capex": None,
        "opex": None
    }
    
    results = []
    
    # Calculate conventional system metrics for comparison
    conv_capex = calculate_conventional_heating_capex(Quantity(max_capacity_kw, "kW"), conventional_system)
    conv_opex = calculate_conventional_heating_opex(conv_capex, annual_energy_demand, conventional_system)
    conv_emissions = calculate_carbon_emissions(annual_energy_demand, conventional_system)
    
    # Grid search
    for capacity_kw in capacity_values:
        for duration_h in duration_values:
            capacity = Quantity(capacity_kw, "kW")
            duration = Quantity(duration_h, "hour")
            
            # Calculate metrics for this configuration
            ts_capex = calculate_thermal_storage_capex(capacity, duration, material_type)
            ts_opex = calculate_thermal_storage_opex(ts_capex, annual_energy_demand)
            
            lcoh = calculate_lcoh(ts_capex, ts_opex, annual_energy_demand)
            
            ts_emissions = calculate_carbon_emissions(annual_energy_demand, "thermal_storage")
            carbon_savings = conv_emissions - ts_emissions
            
            payback = calculate_payback_period(ts_capex, conv_capex, ts_opex, conv_opex, 
                                              ECONOMIC_PARAMS.carbon_price, carbon_savings)
            
            roi = calculate_roi(ts_capex, conv_capex, ts_opex, conv_opex, 
                               ECONOMIC_PARAMS.project_lifetime, ECONOMIC_PARAMS.discount_rate,
                               ECONOMIC_PARAMS.carbon_price, carbon_savings)
            
            # Store results
            results.append({
                "capacity_kw": capacity_kw,
                "duration_h": duration_h,
                "lcoh_usd_per_mwh": lcoh.magnitude,
                "payback_years": payback,
                "roi_percent": roi,
                "capex_usd": ts_capex.magnitude,
                "opex_usd_per_year": ts_opex.magnitude
            })
            
            # Update best configuration based on ROI
            if roi > best_config["roi"] and payback < ECONOMIC_PARAMS.project_lifetime:
                best_config["capacity"] = capacity_kw
                best_config["duration"] = duration_h
                best_config["lcoh"] = lcoh.magnitude
                best_config["payback"] = payback
                best_config["roi"] = roi
                best_config["capex"] = ts_capex.magnitude
                best_config["opex"] = ts_opex.magnitude
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Print optimal configuration
    print("\nOptimal System Configuration:")
    print(f"Capacity: {best_config['capacity']:.2f} kW")
    print(f"Storage Duration: {best_config['duration']:.2f} hours")
    print(f"LCOH: ${best_config['lcoh']:.2f}/MWh")
    print(f"Payback Period: {best_config['payback']:.2f} years")
    print(f"ROI: {best_config['roi']:.2f}%")
    print(f"CAPEX: ${best_config['capex']:,.2f}")
    print(f"Annual OPEX: ${best_config['opex']:,.2f}/year")
    
    return {
        "best_config": best_config,
        "all_results": results_df
    }

def compare_heating_systems(
    capacity: Quantity,
    storage_duration: Quantity,
    annual_energy_output: Quantity,
    material_type: str = "solid_ceramic",
    include_carbon_price: bool = True
) -> pd.DataFrame:
    """
    Compare thermal storage with conventional heating systems.
    
    Args:
        capacity: Thermal power capacity
        storage_duration: Hours of storage at full capacity
        annual_energy_output: Annual thermal energy output
        material_type: Type of storage material
        include_carbon_price: Whether to include carbon pricing in calculations
        
    Returns:
        DataFrame with comparison results
    """
    # Systems to compare
    systems = ["thermal_storage", "natural_gas", "oil", "electric", "chp"]
    
    results = []
    
    # Calculate metrics for each system
    for system in systems:
        if system == "thermal_storage":
            capex = calculate_thermal_storage_capex(capacity, storage_duration, material_type)
            opex = calculate_thermal_storage_opex(capex, annual_energy_output)
        else:
            capex = calculate_conventional_heating_capex(capacity, system)
            opex = calculate_conventional_heating_opex(capex, annual_energy_output, system)
        
        lcoh = calculate_lcoh(capex, opex, annual_energy_output)
        emissions = calculate_carbon_emissions(annual_energy_output, system)
        
        # Calculate carbon cost if included
        carbon_cost = 0
        if include_carbon_price:
            carbon_cost = emissions.magnitude * ECONOMIC_PARAMS.carbon_price.to("USD/tonne").magnitude
            
        # Calculate total annual cost
        total_annual_cost = opex.magnitude + carbon_cost
        
        # Calculate total lifetime cost
        lifetime_cost = capex.magnitude
        for year in range(1, ECONOMIC_PARAMS.project_lifetime + 1):
            lifetime_cost += total_annual_cost / ((1 + ECONOMIC_PARAMS.discount_rate) ** year)
        
        results.append({
            "system": system.replace("_", " ").title(),
            "capex_usd": capex.magnitude,
            "annual_opex_usd": opex.magnitude,
            "lcoh_usd_per_mwh": lcoh.magnitude,
            "annual_emissions_tonnes": emissions.magnitude,
            "annual_carbon_cost_usd": carbon_cost,
            "total_annual_cost_usd": total_annual_cost,
            "lifetime_cost_usd": lifetime_cost
        })
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    
    # Print comparison summary
    print("\nHeating Systems Comparison:")
    for _, row in results_df.iterrows():
        print(f"{row['system']}:")
        print(f"  CAPEX: ${row['capex_usd']:,.2f}")
        print(f"  Annual OPEX: ${row['annual_opex_usd']:,.2f}/year")
        print(f"  LCOH: ${row['lcoh_usd_per_mwh']:.2f}/MWh")
        print(f"  Annual Emissions: {row['annual_emissions_tonnes']:.2f} tonnes CO2e")
        if include_carbon_price:
            print(f"  Annual Carbon Cost: ${row['annual_carbon_cost_usd']:,.2f}/year")
        print(f"  Total Annual Cost: ${row['total_annual_cost_usd']:,.2f}/year")
        print(f"  Lifetime Cost: ${row['lifetime_cost_usd']:,.2f}")
        print()
    
    return results_df

# Example usage
if __name__ == "__main__":
    # This code won't be executed when imported as a module
    # but is here for testing purposes
    
    # Define system parameters
    capacity = Quantity(1000, "kW")
    storage_duration = Quantity(8, "hour")
    annual_energy = Quantity(3000, "MWh")
    
    # Compare thermal storage with conventional systems
    comparison = compare_heating_systems(capacity, storage_duration, annual_energy)
    
    # Perform sensitivity analysis
    sensitivity = sensitivity_analysis(capacity, storage_duration, annual_energy)
    
    # Optimize system sizing
    min_capacity = Quantity(500, "kW")
    max_capacity = Quantity(2000, "kW")
    min_duration = Quantity(4, "hour")
    max_duration = Quantity(12, "hour")
    
    optimization = optimize_system_sizing(
        min_capacity, max_capacity, 
        min_duration, max_duration,
        annual_energy
    )
    
    print("Economic analysis complete")

def calculate_lcoh(capital_cost, annual_opex, annual_heat_output, discount_rate, lifetime):
    """
    Calculate the Levelized Cost of Heat (LCOH).
    
    Args:
        capital_cost: Total capital cost in $
        annual_opex: Annual operational expenditure in $/year
        annual_heat_output: Annual heat output in kWh/year
        discount_rate: Discount rate as a decimal (e.g., 0.07 for 7%)
        lifetime: System lifetime in years
        
    Returns:
        LCOH in $/kWh
    """
    npv_costs = capital_cost
    npv_energy = 0
    
    for year in range(1, lifetime + 1):
        npv_costs += annual_opex / ((1 + discount_rate) ** year)
        npv_energy += annual_heat_output / ((1 + discount_rate) ** year)
    
    return npv_costs / npv_energy

def calculate_payback_period(capital_cost, annual_savings, discount_rate=0.07):
    """
    Calculate simple and discounted payback periods.
    
    Args:
        capital_cost: Initial investment in $
        annual_savings: Annual cost savings in $/year
        discount_rate: Discount rate as a decimal
        
    Returns:
        Tuple of (simple_payback, discounted_payback) in years
    """
    # Simple payback
    simple_payback = capital_cost / annual_savings
    
    # Discounted payback
    cumulative_discounted_savings = 0
    discounted_payback = None
    
    for year in range(1, 101):  # Cap at 100 years
        cumulative_discounted_savings += annual_savings / ((1 + discount_rate) ** year)
        if cumulative_discounted_savings >= capital_cost and discounted_payback is None:
            discounted_payback = year
            break
    
    return simple_payback, discounted_payback

def calculate_roi(capital_cost, annual_savings, lifetime):
    """
    Calculate Return on Investment (ROI).
    
    Args:
        capital_cost: Initial investment in $
        annual_savings: Annual cost savings in $/year
        lifetime: System lifetime in years
        
    Returns:
        ROI as a percentage
    """
    total_savings = annual_savings * lifetime
    roi = ((total_savings - capital_cost) / capital_cost) * 100
    return roi

def calculate_conventional_heating_costs(energy_demand_kwh, fuel_type="natural_gas"):
    """
    Calculate costs for conventional heating technologies.
    
    Args:
        energy_demand_kwh: Annual energy demand in kWh
        fuel_type: Type of fuel (natural_gas, oil, electricity, etc.)
        
    Returns:
        Dictionary with cost and emissions data
    """
    fuel_costs = {
        "natural_gas": 0.03,  # $/kWh
        "oil": 0.07,          # $/kWh
        "electricity": 0.12,  # $/kWh
        "biomass": 0.05,      # $/kWh
    }
    
    efficiency = {
        "natural_gas": 0.85,
        "oil": 0.80,
        "electricity": 0.99,
        "biomass": 0.75,
    }
    
    emissions = {
        "natural_gas": 0.2,   # kg CO2/kWh
        "oil": 0.27,          # kg CO2/kWh
        "electricity": 0.15,  # kg CO2/kWh (grid average)
        "biomass": 0.02,      # kg CO2/kWh
    }
    
    capital_costs = {
        "natural_gas": 100,   # $/kW
        "oil": 120,           # $/kW
        "electricity": 50,    # $/kW
        "biomass": 200,       # $/kW
    }
    
    if fuel_type not in fuel_costs:
        raise ValueError(f"Unknown fuel type: {fuel_type}")
    
    # Calculate fuel consumption
    fuel_consumption = energy_demand_kwh / efficiency[fuel_type]
    
    # Calculate annual fuel cost
    annual_fuel_cost = fuel_consumption * fuel_costs[fuel_type]
    
    # Calculate emissions
    annual_emissions = fuel_consumption * emissions[fuel_type]
    
    # Calculate capital cost (assuming 1 kW per 1000 kWh annual demand as a rough estimate)
    system_capacity_kw = energy_demand_kwh / 8760
    system_capital_cost = system_capacity_kw * capital_costs[fuel_type]
    
    return {
        "fuel_type": fuel_type,
        "annual_fuel_cost": annual_fuel_cost,
        "annual_emissions": annual_emissions,
        "capital_cost": system_capital_cost,
        "efficiency": efficiency[fuel_type],
        "fuel_price": fuel_costs[fuel_type]
    }

def sensitivity_analysis(base_case, variables, ranges):
    """
    Perform sensitivity analysis on key parameters.
    
    Args:
        base_case: Base case LCOH in $/kWh
        variables: Dictionary of variables and their base values
        ranges: Dictionary of variables and their percentage ranges to test
        
    Returns:
        Dictionary with sensitivity results
    """
    results = {}
    
    for var, base_value in variables.items():
        if var not in ranges:
            continue
            
        var_results = []
        range_pct = ranges[var]
        
        for pct_change in np.linspace(-range_pct, range_pct, 5):
            new_value = base_value * (1 + pct_change/100)
            # This is a simplified placeholder - in reality you would recalculate LCOH
            # with the new parameter value
            impact = base_case * (1 + (pct_change/100) * 0.5)  # Simplified impact model
            var_results.append((pct_change, new_value, impact))
            
        results[var] = var_results
        
    return results

def carbon_pricing_impact(annual_emissions, carbon_price_range):
    """
    Calculate the impact of carbon pricing on total costs.
    
    Args:
        annual_emissions: Annual CO2 emissions in tonnes
        carbon_price_range: Range of carbon prices to analyze in $/tonne
        
    Returns:
        List of (carbon_price, annual_cost) tuples
    """
    results = []
    
    for carbon_price in carbon_price_range:
        annual_cost = annual_emissions * carbon_price
        results.append((carbon_price, annual_cost))
        
    return results
"""
Economic analysis tools for thermal energy storage systems.
"""
from epyr.tools_units import Quantity
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS
import numpy as np

print("Loading economic simulation module")

def calculate_capex() -> float:
    """
    Calculate capital expenditure for the thermal storage system.
    
    Returns:
        Total capital expenditure in USD
    """
    # Get parameters
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude  # kWh
    capital_cost_per_kwh = THERMAL_STORAGE_PARAMS.capital_cost.magnitude  # USD/kWh
    
    # Calculate base capital cost
    base_capex = storage_capacity * capital_cost_per_kwh
    
    # Add installation and engineering costs (typically 30% of equipment cost)
    installation_factor = 0.3
    total_capex = base_capex * (1 + installation_factor)
    
    return total_capex

def calculate_annual_opex() -> float:
    """
    Calculate annual operational expenditure.
    
    Returns:
        Annual OPEX in USD/year
    """
    # Get parameters
    capex = calculate_capex()
    maintenance_factor = THERMAL_STORAGE_PARAMS.maintenance_factor
    electricity_price = THERMAL_STORAGE_PARAMS.electricity_price.magnitude  # USD/kWh
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude  # kWh
    charge_efficiency = THERMAL_STORAGE_PARAMS.charge_efficiency
    
    # Calculate maintenance costs
    maintenance_cost = capex * maintenance_factor
    
    # Calculate electricity costs for charging
    annual_energy_input = storage_capacity * cycles_per_year / charge_efficiency
    electricity_cost = annual_energy_input * electricity_price
    
    # Other fixed operating costs (labor, insurance, etc.)
    fixed_costs = 20000  # USD/year
    
    # Total OPEX
    total_opex = maintenance_cost + electricity_cost + fixed_costs
    
    return total_opex

def calculate_lcoe() -> float:
    """
    Calculate Levelized Cost of Energy (LCOE).
    
    Returns:
        LCOE in USD/kWh
    """
    # Get parameters
    capex = calculate_capex()
    annual_opex = calculate_annual_opex()
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude  # kWh
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    lifetime = THERMAL_STORAGE_PARAMS.design_life  # years
    discount_rate = THERMAL_STORAGE_PARAMS.discount_rate
    
    # Calculate annual energy output
    annual_energy_output = storage_capacity * cycles_per_year * discharge_efficiency
    
    # Calculate present value of costs
    pv_costs = capex
    for year in range(1, lifetime + 1):
        pv_costs += annual_opex / ((1 + discount_rate) ** year)
    
    # Calculate present value of energy
    pv_energy = 0
    for year in range(1, lifetime + 1):
        pv_energy += annual_energy_output / ((1 + discount_rate) ** year)
    
    # Calculate LCOE
    lcoe = pv_costs / pv_energy
    
    return lcoe

def calculate_payback_period() -> float:
    """
    Calculate simple payback period compared to conventional heating.
    
    Returns:
        Payback period in years
    """
    # Get parameters
    capex = calculate_capex()
    annual_opex = calculate_annual_opex()
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude  # kWh
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Calculate annual energy output
    annual_energy_output = storage_capacity * cycles_per_year * discharge_efficiency
    
    # Estimate conventional heating costs
    # Assuming natural gas at $8/MMBtu with 80% efficiency
    natural_gas_price = 8.0  # USD/MMBtu
    natural_gas_efficiency = 0.8
    mmbtu_per_kwh = 0.003412  # MMBtu/kWh
    
    conventional_fuel_cost = (annual_energy_output * mmbtu_per_kwh * natural_gas_price) / natural_gas_efficiency
    
    # Estimate conventional system capex (lower than thermal storage)
    conventional_capex = capex * 0.4  # Simplified assumption
    
    # Calculate annual savings
    annual_savings = conventional_fuel_cost - annual_opex
    
    # Calculate payback period
    incremental_investment = capex - conventional_capex
    payback_period = incremental_investment / annual_savings
    
    return payback_period

def calculate_roi() -> float:
    """
    Calculate Return on Investment (ROI).
    
    Returns:
        ROI as a percentage
    """
    # Get parameters
    capex = calculate_capex()
    annual_opex = calculate_annual_opex()
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude  # kWh
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    lifetime = THERMAL_STORAGE_PARAMS.design_life  # years
    discount_rate = THERMAL_STORAGE_PARAMS.discount_rate
    
    # Calculate annual energy output
    annual_energy_output = storage_capacity * cycles_per_year * discharge_efficiency
    
    # Estimate conventional heating costs
    # Assuming natural gas at $8/MMBtu with 80% efficiency
    natural_gas_price = 8.0  # USD/MMBtu
    natural_gas_efficiency = 0.8
    mmbtu_per_kwh = 0.003412  # MMBtu/kWh
    
    conventional_fuel_cost = (annual_energy_output * mmbtu_per_kwh * natural_gas_price) / natural_gas_efficiency
    
    # Estimate conventional system capex (lower than thermal storage)
    conventional_capex = capex * 0.4  # Simplified assumption
    
    # Calculate annual savings
    annual_savings = conventional_fuel_cost - annual_opex
    
    # Calculate NPV of savings
    npv_savings = 0
    for year in range(1, lifetime + 1):
        npv_savings += annual_savings / ((1 + discount_rate) ** year)
    
    # Calculate incremental investment
    incremental_investment = capex - conventional_capex
    
    # Calculate ROI
    roi = (npv_savings - incremental_investment) / incremental_investment * 100
    
    return roi

def carbon_emission_reduction() -> float:
    """
    Calculate annual carbon emission reduction.
    
    Returns:
        Annual CO2 emission reduction in tonnes
    """
    # Get parameters
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude  # kWh
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Calculate annual energy output
    annual_energy_output = storage_capacity * cycles_per_year * discharge_efficiency
    
    # Emission factors (kg CO2/kWh)
    natural_gas_emission_factor = 0.2
    grid_electricity_emission_factor = 0.15
    
    # Calculate emissions
    conventional_emissions = annual_energy_output * natural_gas_emission_factor
    thermal_storage_emissions = annual_energy_output * grid_electricity_emission_factor / discharge_efficiency
    
    # Calculate emission reduction
    emission_reduction = (conventional_emissions - thermal_storage_emissions) / 1000  # tonnes
    
    return emission_reduction

def sensitivity_analysis() -> dict:
    """
    Perform sensitivity analysis on key parameters.
    
    Returns:
        Dictionary with sensitivity analysis results
    """
    # Base values
    base_lcoe = calculate_lcoe()
    base_payback = calculate_payback_period()
    base_roi = calculate_roi()
    
    # Parameters to analyze
    parameters = {
        "electricity_price": THERMAL_STORAGE_PARAMS.electricity_price.magnitude,
        "capital_cost": THERMAL_STORAGE_PARAMS.capital_cost.magnitude,
        "cycles_per_year": THERMAL_STORAGE_PARAMS.cycles_per_year,
        "discharge_efficiency": THERMAL_STORAGE_PARAMS.discharge_efficiency,
        "design_life": THERMAL_STORAGE_PARAMS.design_life
    }
    
    # Variation range (±30%)
    variation = 0.3
    
    results = {}
    
    # For each parameter, vary it and calculate metrics
    for param, base_value in parameters.items():
        param_results = []
        
        for factor in np.linspace(1-variation, 1+variation, 5):
            # Temporarily modify parameter
            modified_value = base_value * factor
            
            # Calculate metrics with modified parameter
            # This is a simplified approach - in a real model, we would
            # properly update the parameter in the model
            
            # Simplified calculation based on proportional changes
            if param == "electricity_price":
                lcoe_factor = 1 + (factor - 1) * 0.3  # Assuming electricity is 30% of LCOE
                payback_factor = 1 + (factor - 1) * 0.2  # Assuming smaller impact on payback
                roi_factor = 1 - (factor - 1) * 0.3  # Inverse relationship
            elif param == "capital_cost":
                lcoe_factor = 1 + (factor - 1) * 0.7  # Assuming capital is 70% of LCOE
                payback_factor = factor  # Direct relationship
                roi_factor = 1 / factor  # Inverse relationship
            elif param == "cycles_per_year":
                lcoe_factor = 1 / factor  # Inverse relationship
                payback_factor = 1 / factor  # Inverse relationship
                roi_factor = factor  # Direct relationship
            elif param == "discharge_efficiency":
                lcoe_factor = 1 / factor  # Inverse relationship
                payback_factor = 1 / factor  # Inverse relationship
                roi_factor = factor  # Direct relationship
            elif param == "design_life":
                lcoe_factor = 1 / (1 + (factor - 1) * 0.5)  # Non-linear relationship
                payback_factor = 1  # No direct impact on simple payback
                roi_factor = 1 + (factor - 1) * 0.5  # Partial impact
            
            # Calculate modified metrics
            modified_lcoe = base_lcoe * lcoe_factor
            modified_payback = base_payback * payback_factor
            modified_roi = base_roi * roi_factor
            
            param_results.append({
                "factor": factor,
                "value": modified_value,
                "lcoe": modified_lcoe,
                "payback": modified_payback,
                "roi": modified_roi
            })
        
        results[param] = param_results
    
    return results

# Print some basic economic results
capex = calculate_capex()
opex = calculate_annual_opex()
lcoe = calculate_lcoe()
payback = calculate_payback_period()
roi = calculate_roi()
carbon_reduction = carbon_emission_reduction()

print(f"Capital expenditure: ${capex:,.2f}")
print(f"Annual operational expenditure: ${opex:,.2f}")
print(f"Levelized cost of energy: ${lcoe:.4f}/kWh")
print(f"Payback period: {payback:.2f} years")
print(f"Return on investment: {roi:.2f}%")
print(f"Annual carbon emission reduction: {carbon_reduction:.2f} tonnes CO2")
"""
Economic analysis functions.
"""
from epyr.parameters_thermal_storage import THERMAL_STORAGE_PARAMS

def calculate_lcoe() -> float:
    """
    Calculate levelized cost of energy storage.
    
    Returns:
        LCOE in USD/kWh
    """
    # Simplified LCOE calculation
    capital_cost = 250  # USD/kWh
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    design_life = THERMAL_STORAGE_PARAMS.design_life
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Total capital cost
    total_capex = capital_cost * storage_capacity
    
    # Lifetime energy output
    lifetime_energy = storage_capacity * cycles_per_year * design_life * discharge_efficiency
    
    # Simple LCOE
    lcoe = total_capex / lifetime_energy
    
    return lcoe

def calculate_payback_period() -> float:
    """
    Calculate simple payback period.
    
    Returns:
        Payback period in years
    """
    # Parameters
    capital_cost = 250  # USD/kWh
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude
    cycles_per_year = THERMAL_STORAGE_PARAMS.cycles_per_year
    discharge_efficiency = THERMAL_STORAGE_PARAMS.discharge_efficiency
    
    # Electricity price differential (peak vs. off-peak)
    peak_price = 0.15  # USD/kWh
    off_peak_price = 0.05  # USD/kWh
    price_differential = peak_price - off_peak_price
    
    # Annual savings
    annual_savings = storage_capacity * cycles_per_year * discharge_efficiency * price_differential
    
    # Total capital cost
    total_capex = capital_cost * storage_capacity
    
    # Simple payback
    payback = total_capex / annual_savings
    
    return payback

def calculate_roi() -> float:
    """
    Calculate return on investment.
    
    Returns:
        ROI as a fraction
    """
    payback = calculate_payback_period()
    design_life = THERMAL_STORAGE_PARAMS.design_life
    
    # Simple ROI calculation
    roi = (design_life / payback) - 1
    
    return roi

def calculate_capex() -> float:
    """
    Calculate total capital expenditure.
    
    Returns:
        Total CAPEX in USD
    """
    capital_cost = 250  # USD/kWh
    storage_capacity = THERMAL_STORAGE_PARAMS.storage_capacity.magnitude
    
    return capital_cost * storage_capacity

print("Economic analysis module loaded")
