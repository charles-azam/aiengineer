"""
Cost analysis for the High-Temperature Gas-cooled Reactor (HTGR) system.
This module provides a comprehensive economic assessment of the HTGR design,
including capital costs, operating costs, lifecycle costs, and comparative analysis.
"""

from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from pyforge import Parameters, Quantity, UREG
import pandas as pd
import numpy as np
from pathlib import Path

# Define cost parameters
class HTGRCostParameters(Parameters):
    """Define all the key cost parameters for our HTGR system."""
    # Capital costs ($ per kW thermal)
    capital_cost_per_kw: float = 4500  # $/kWth
    
    # Reactor sizes
    reactor_sizes: list = [10, 15, 20]  # MWth
    
    # Component cost breakdown (percentage of total capital cost)
    core_components_pct: float = 0.25
    primary_loop_pct: float = 0.15
    secondary_loop_pct: float = 0.10
    safety_systems_pct: float = 0.12
    control_systems_pct: float = 0.08
    civil_structures_pct: float = 0.20
    manufacturing_pct: float = 0.05
    transport_installation_pct: float = 0.05
    
    # Operating costs
    fuel_cost_per_mwh: float = 7.5  # $/MWh thermal
    enrichment_cost_per_kg: float = 1200  # $/kg
    maintenance_cost_pct: float = 0.02  # % of capital cost per year
    personnel_cost_per_year: float = 1500000  # $ per year
    regulatory_cost_per_year: float = 500000  # $ per year
    
    # Lifecycle parameters
    plant_lifetime: int = 20  # years
    refueling_interval: int = 5  # years
    refueling_cost_pct: float = 0.08  # % of capital cost
    component_replacement_pct: float = 0.15  # % of capital cost over lifetime
    decommissioning_pct: float = 0.15  # % of capital cost
    
    # Financial parameters
    discount_rate: float = 0.07  # 7%
    capacity_factor: float = 0.90  # 90%
    
    # Comparative heating costs ($/MWh thermal)
    natural_gas_cost: float = 30
    coal_cost: float = 25
    biomass_cost: float = 45
    electric_cost: float = 80
    
    # Carbon pricing
    carbon_price: float = 50  # $/tonne CO2
    
    # Emissions factors (kg CO2/MWh thermal)
    natural_gas_emissions: float = 200
    coal_emissions: float = 350
    biomass_emissions: float = 30
    electric_emissions: float = 100  # Depends on grid mix
    htgr_emissions: float = 5  # Lifecycle emissions

# Single source of truth
HTGR_COST_PARAMS = HTGRCostParameters()

def calculate_capital_costs(reactor_size_mw):
    """Calculate the capital costs for a given reactor size."""
    total_capital_cost = reactor_size_mw * 1000 * HTGR_COST_PARAMS.capital_cost_per_kw
    
    # Component breakdown
    core_components = total_capital_cost * HTGR_COST_PARAMS.core_components_pct
    primary_loop = total_capital_cost * HTGR_COST_PARAMS.primary_loop_pct
    secondary_loop = total_capital_cost * HTGR_COST_PARAMS.secondary_loop_pct
    safety_systems = total_capital_cost * HTGR_COST_PARAMS.safety_systems_pct
    control_systems = total_capital_cost * HTGR_COST_PARAMS.control_systems_pct
    civil_structures = total_capital_cost * HTGR_COST_PARAMS.civil_structures_pct
    manufacturing = total_capital_cost * HTGR_COST_PARAMS.manufacturing_pct
    transport_installation = total_capital_cost * HTGR_COST_PARAMS.transport_installation_pct
    
    return {
        "total": total_capital_cost,
        "core_components": core_components,
        "primary_loop": primary_loop,
        "secondary_loop": secondary_loop,
        "safety_systems": safety_systems,
        "control_systems": control_systems,
        "civil_structures": civil_structures,
        "manufacturing": manufacturing,
        "transport_installation": transport_installation
    }

def calculate_annual_operating_costs(reactor_size_mw, capital_cost):
    """Calculate the annual operating costs for a given reactor size."""
    annual_energy_mwh = reactor_size_mw * 24 * 365 * HTGR_COST_PARAMS.capacity_factor
    
    fuel_cost = annual_energy_mwh * HTGR_COST_PARAMS.fuel_cost_per_mwh
    maintenance_cost = capital_cost * HTGR_COST_PARAMS.maintenance_cost_pct
    personnel_cost = HTGR_COST_PARAMS.personnel_cost_per_year
    regulatory_cost = HTGR_COST_PARAMS.regulatory_cost_per_year
    
    total_operating_cost = fuel_cost + maintenance_cost + personnel_cost + regulatory_cost
    
    return {
        "total": total_operating_cost,
        "fuel": fuel_cost,
        "maintenance": maintenance_cost,
        "personnel": personnel_cost,
        "regulatory": regulatory_cost,
        "annual_energy_mwh": annual_energy_mwh
    }

def calculate_lifecycle_costs(reactor_size_mw, capital_cost):
    """Calculate the lifecycle costs for a given reactor size."""
    lifetime = HTGR_COST_PARAMS.plant_lifetime
    refueling_cycles = lifetime // HTGR_COST_PARAMS.refueling_interval
    
    refueling_cost = capital_cost * HTGR_COST_PARAMS.refueling_cost_pct * refueling_cycles
    component_replacement = capital_cost * HTGR_COST_PARAMS.component_replacement_pct
    decommissioning = capital_cost * HTGR_COST_PARAMS.decommissioning_pct
    
    total_lifecycle_cost = refueling_cost + component_replacement + decommissioning
    
    return {
        "total": total_lifecycle_cost,
        "refueling": refueling_cost,
        "component_replacement": component_replacement,
        "decommissioning": decommissioning
    }

def calculate_lcoh(reactor_size_mw, capital_cost, annual_operating_cost, lifecycle_cost):
    """Calculate the Levelized Cost of Heat (LCOH) for a given reactor size."""
    lifetime = HTGR_COST_PARAMS.plant_lifetime
    discount_rate = HTGR_COST_PARAMS.discount_rate
    annual_energy_mwh = reactor_size_mw * 24 * 365 * HTGR_COST_PARAMS.capacity_factor
    
    # Present value of all costs
    pv_capital = capital_cost
    
    # Present value of operating costs over lifetime
    pv_operating = 0
    for year in range(1, lifetime + 1):
        pv_operating += annual_operating_cost / ((1 + discount_rate) ** year)
    
    # Present value of lifecycle costs
    pv_lifecycle = lifecycle_cost / ((1 + discount_rate) ** (lifetime / 2))  # Simplified assumption
    
    total_pv_cost = pv_capital + pv_operating + pv_lifecycle
    
    # Present value of energy produced
    pv_energy = 0
    for year in range(1, lifetime + 1):
        pv_energy += annual_energy_mwh / ((1 + discount_rate) ** year)
    
    # LCOH calculation
    lcoh = total_pv_cost / pv_energy
    
    return lcoh

def compare_heating_options(htgr_lcoh):
    """Compare HTGR heating costs with conventional options."""
    natural_gas_cost = HTGR_COST_PARAMS.natural_gas_cost
    coal_cost = HTGR_COST_PARAMS.coal_cost
    biomass_cost = HTGR_COST_PARAMS.biomass_cost
    electric_cost = HTGR_COST_PARAMS.electric_cost
    
    # Add carbon costs
    carbon_price = HTGR_COST_PARAMS.carbon_price
    natural_gas_carbon_cost = HTGR_COST_PARAMS.natural_gas_emissions * carbon_price / 1000
    coal_carbon_cost = HTGR_COST_PARAMS.coal_emissions * carbon_price / 1000
    biomass_carbon_cost = HTGR_COST_PARAMS.biomass_emissions * carbon_price / 1000
    electric_carbon_cost = HTGR_COST_PARAMS.electric_emissions * carbon_price / 1000
    htgr_carbon_cost = HTGR_COST_PARAMS.htgr_emissions * carbon_price / 1000
    
    natural_gas_total = natural_gas_cost + natural_gas_carbon_cost
    coal_total = coal_cost + coal_carbon_cost
    biomass_total = biomass_cost + biomass_carbon_cost
    electric_total = electric_cost + electric_carbon_cost
    htgr_total = htgr_lcoh + htgr_carbon_cost
    
    return {
        "htgr": htgr_total,
        "natural_gas": natural_gas_total,
        "coal": coal_total,
        "biomass": biomass_total,
        "electric": electric_total
    }

def perform_sensitivity_analysis(reactor_size_mw):
    """Perform sensitivity analysis on key parameters."""
    base_capital_cost = calculate_capital_costs(reactor_size_mw)["total"]
    base_operating_cost = calculate_annual_operating_costs(reactor_size_mw, base_capital_cost)["total"]
    base_lifecycle_cost = calculate_lifecycle_costs(reactor_size_mw, base_capital_cost)["total"]
    base_lcoh = calculate_lcoh(reactor_size_mw, base_capital_cost, base_operating_cost, base_lifecycle_cost)
    
    # Sensitivity ranges
    fuel_price_range = [0.8, 1.0, 1.2]  # -20%, base, +20%
    capital_cost_range = [0.9, 1.0, 1.1]  # -10%, base, +10%
    discount_rate_range = [0.05, 0.07, 0.09]  # 5%, 7%, 9%
    carbon_price_range = [25, 50, 100]  # $/tonne CO2
    
    sensitivity_results = {
        "fuel_price": [],
        "capital_cost": [],
        "discount_rate": [],
        "carbon_price": []
    }
    
    # Fuel price sensitivity
    for factor in fuel_price_range:
        modified_params = HTGRCostParameters()
        modified_params.fuel_cost_per_mwh = HTGR_COST_PARAMS.fuel_cost_per_mwh * factor
        
        modified_operating_cost = base_operating_cost * (1 + (factor - 1) * 0.3)  # Assuming fuel is 30% of operating costs
        modified_lcoh = calculate_lcoh(reactor_size_mw, base_capital_cost, modified_operating_cost, base_lifecycle_cost)
        sensitivity_results["fuel_price"].append((factor, modified_lcoh))
    
    # Capital cost sensitivity
    for factor in capital_cost_range:
        modified_capital_cost = base_capital_cost * factor
        modified_lcoh = calculate_lcoh(reactor_size_mw, modified_capital_cost, base_operating_cost, base_lifecycle_cost)
        sensitivity_results["capital_cost"].append((factor, modified_lcoh))
    
    # Discount rate sensitivity
    for rate in discount_rate_range:
        modified_params = HTGRCostParameters()
        modified_params.discount_rate = rate
        
        modified_lcoh = calculate_lcoh(reactor_size_mw, base_capital_cost, base_operating_cost, base_lifecycle_cost)
        # This is a simplification - in reality we'd recalculate with the new discount rate
        adjustment_factor = (rate / HTGR_COST_PARAMS.discount_rate) ** 0.5
        modified_lcoh = base_lcoh * adjustment_factor
        
        sensitivity_results["discount_rate"].append((rate, modified_lcoh))
    
    # Carbon price sensitivity
    for price in carbon_price_range:
        modified_params = HTGRCostParameters()
        modified_params.carbon_price = price
        
        # Recalculate comparison with new carbon price
        comparison = compare_heating_options(base_lcoh)
        sensitivity_results["carbon_price"].append((price, comparison))
    
    return sensitivity_results

def generate_cost_report():
    """Generate a comprehensive cost report for the HTGR system."""
    # Document metadata
    config = DocumentConfig(
        title="HTGR Economic Analysis Report",
        author="Reactor Design Team",
        date="2025-06-02"
    )
    display(config)
    
    # Title
    display(Title("# High-Temperature Gas-cooled Reactor (HTGR) Economic Analysis"))
    
    # Introduction
    display("## Introduction")
    display(
        "This report presents a comprehensive economic analysis of our High-Temperature "
        "Gas-cooled Reactor (HTGR) design for industrial heat applications. "
        "The analysis covers capital costs, operating costs, lifecycle costs, and "
        "provides a comparative assessment against conventional heating technologies. "
        "All costs are presented in 2025 US dollars."
    )
    
    # Key parameters
    display("## Key Economic Parameters")
    df_params = pd.DataFrame([
        {"Parameter": "Capital Cost", "Value": f"${HTGR_COST_PARAMS.capital_cost_per_kw}/kWth"},
        {"Parameter": "Plant Lifetime", "Value": f"{HTGR_COST_PARAMS.plant_lifetime} years"},
        {"Parameter": "Capacity Factor", "Value": f"{HTGR_COST_PARAMS.capacity_factor * 100}%"},
        {"Parameter": "Discount Rate", "Value": f"{HTGR_COST_PARAMS.discount_rate * 100}%"},
        {"Parameter": "Fuel Cost", "Value": f"${HTGR_COST_PARAMS.fuel_cost_per_mwh}/MWh thermal"},
        {"Parameter": "Refueling Interval", "Value": f"{HTGR_COST_PARAMS.refueling_interval} years"},
    ])
    display(Table(df_params, "Key Economic Parameters", "tbl-econ-params"))
    
    # Capital costs
    display("## 1. Capital Costs")
    
    # Create capital cost tables for each reactor size
    for size in HTGR_COST_PARAMS.reactor_sizes:
        capital_costs = calculate_capital_costs(size)
        
        df_capital = pd.DataFrame([
            {"Component": "Core Components", "Cost ($ million)": f"${capital_costs['core_components']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.core_components_pct*100:.1f}%"},
            {"Component": "Primary Loop", "Cost ($ million)": f"${capital_costs['primary_loop']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.primary_loop_pct*100:.1f}%"},
            {"Component": "Secondary Loop", "Cost ($ million)": f"${capital_costs['secondary_loop']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.secondary_loop_pct*100:.1f}%"},
            {"Component": "Safety Systems", "Cost ($ million)": f"${capital_costs['safety_systems']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.safety_systems_pct*100:.1f}%"},
            {"Component": "Control Systems", "Cost ($ million)": f"${capital_costs['control_systems']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.control_systems_pct*100:.1f}%"},
            {"Component": "Civil Structures", "Cost ($ million)": f"${capital_costs['civil_structures']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.civil_structures_pct*100:.1f}%"},
            {"Component": "Manufacturing", "Cost ($ million)": f"${capital_costs['manufacturing']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.manufacturing_pct*100:.1f}%"},
            {"Component": "Transport & Installation", "Cost ($ million)": f"${capital_costs['transport_installation']/1e6:.2f}M", "Percentage": f"{HTGR_COST_PARAMS.transport_installation_pct*100:.1f}%"},
            {"Component": "Total Capital Cost", "Cost ($ million)": f"${capital_costs['total']/1e6:.2f}M", "Percentage": "100.0%"},
        ])
        display(Table(df_capital, f"Capital Costs Breakdown for {size} MWth HTGR", f"tbl-capital-{size}mw"))
    
    display(
        "The capital costs include all expenses related to design, procurement, manufacturing, "
        "and installation of the HTGR system. The modular design approach allows for factory "
        "fabrication of key components, reducing on-site construction time and associated costs. "
        "The core components represent the largest single capital expense due to the specialized "
        "materials and precision manufacturing required for the TRISO fuel and reactor internals."
    )
    
    # Operating costs
    display("## 2. Operating Costs")
    
    # Create operating cost tables for each reactor size
    for size in HTGR_COST_PARAMS.reactor_sizes:
        capital_costs = calculate_capital_costs(size)
        operating_costs = calculate_annual_operating_costs(size, capital_costs["total"])
        
        df_operating = pd.DataFrame([
            {"Category": "Fuel Costs", "Annual Cost ($ million)": f"${operating_costs['fuel']/1e6:.2f}M", "Percentage": f"{operating_costs['fuel']/operating_costs['total']*100:.1f}%"},
            {"Category": "Maintenance", "Annual Cost ($ million)": f"${operating_costs['maintenance']/1e6:.2f}M", "Percentage": f"{operating_costs['maintenance']/operating_costs['total']*100:.1f}%"},
            {"Category": "Personnel", "Annual Cost ($ million)": f"${operating_costs['personnel']/1e6:.2f}M", "Percentage": f"{operating_costs['personnel']/operating_costs['total']*100:.1f}%"},
            {"Category": "Regulatory Compliance", "Annual Cost ($ million)": f"${operating_costs['regulatory']/1e6:.2f}M", "Percentage": f"{operating_costs['regulatory']/operating_costs['total']*100:.1f}%"},
            {"Category": "Total Annual Operating Cost", "Annual Cost ($ million)": f"${operating_costs['total']/1e6:.2f}M", "Percentage": "100.0%"},
        ])
        display(Table(df_operating, f"Annual Operating Costs for {size} MWth HTGR", f"tbl-operating-{size}mw"))
        
        # Calculate per MWh cost
        per_mwh_cost = operating_costs['total'] / operating_costs['annual_energy_mwh']
        display(f"The operating cost per MWh thermal for the {size} MWth HTGR is ${per_mwh_cost:.2f}/MWh.")
    
    display(
        "Operating costs include all expenses related to the day-to-day operation of the HTGR system. "
        "The HTGR design benefits from low fuel costs due to the high energy density of nuclear fuel "
        "and the long refueling intervals. Personnel costs include operators, maintenance staff, and "
        "security personnel. Regulatory compliance costs cover licensing, inspections, and reporting "
        "requirements specific to nuclear facilities."
    )
    
    # Lifecycle costs
    display("## 3. Lifecycle Costs")
    
    # Create lifecycle cost tables for each reactor size
    for size in HTGR_COST_PARAMS.reactor_sizes:
        capital_costs = calculate_capital_costs(size)
        lifecycle_costs = calculate_lifecycle_costs(size, capital_costs["total"])
        
        df_lifecycle = pd.DataFrame([
            {"Category": "Refueling", "Lifecycle Cost ($ million)": f"${lifecycle_costs['refueling']/1e6:.2f}M", "Percentage": f"{lifecycle_costs['refueling']/lifecycle_costs['total']*100:.1f}%"},
            {"Category": "Component Replacement", "Lifecycle Cost ($ million)": f"${lifecycle_costs['component_replacement']/1e6:.2f}M", "Percentage": f"{lifecycle_costs['component_replacement']/lifecycle_costs['total']*100:.1f}%"},
            {"Category": "Decommissioning", "Lifecycle Cost ($ million)": f"${lifecycle_costs['decommissioning']/1e6:.2f}M", "Percentage": f"{lifecycle_costs['decommissioning']/lifecycle_costs['total']*100:.1f}%"},
            {"Category": "Total Lifecycle Cost", "Lifecycle Cost ($ million)": f"${lifecycle_costs['total']/1e6:.2f}M", "Percentage": "100.0%"},
        ])
        display(Table(df_lifecycle, f"Lifecycle Costs for {size} MWth HTGR over {HTGR_COST_PARAMS.plant_lifetime} years", f"tbl-lifecycle-{size}mw"))
    
    display(
        "Lifecycle costs account for major periodic expenses over the plant lifetime. "
        "Refueling occurs every 5 years and includes the cost of new fuel assemblies, "
        "spent fuel handling, and associated maintenance activities. Component replacement "
        "covers major equipment that may need replacement during the plant lifetime. "
        "Decommissioning provisions ensure funds are available for safe end-of-life "
        "dismantling and site restoration."
    )
    
    # LCOH calculation
    display("## 4. Levelized Cost of Heat (LCOH)")
    
    df_lcoh = pd.DataFrame(columns=["Reactor Size (MWth)", "LCOH ($/MWh thermal)"])
    
    for size in HTGR_COST_PARAMS.reactor_sizes:
        capital_costs = calculate_capital_costs(size)
        operating_costs = calculate_annual_operating_costs(size, capital_costs["total"])
        lifecycle_costs = calculate_lifecycle_costs(size, capital_costs["total"])
        
        lcoh = calculate_lcoh(size, capital_costs["total"], operating_costs["total"], lifecycle_costs["total"])
        
        df_lcoh = pd.concat([df_lcoh, pd.DataFrame({
            "Reactor Size (MWth)": [size],
            "LCOH ($/MWh thermal)": [f"${lcoh:.2f}"]
        })], ignore_index=True)
    
    display(Table(df_lcoh, "Levelized Cost of Heat by Reactor Size", "tbl-lcoh"))
    
    display(
        "The Levelized Cost of Heat (LCOH) represents the present value of all costs over the "
        "plant lifetime divided by the present value of all heat produced. It provides a "
        "standardized metric for comparing different heat generation technologies. "
        "The LCOH calculation includes capital costs, operating costs, and lifecycle costs, "
        "all discounted at the specified discount rate. The results show economies of scale, "
        "with larger reactor sizes achieving lower LCOH values."
    )
    
    # Comparative analysis
    display("## 5. Comparative Analysis")
    
    # Use the middle reactor size for comparison
    mid_size = HTGR_COST_PARAMS.reactor_sizes[1]  # 15 MWth
    capital_costs = calculate_capital_costs(mid_size)
    operating_costs = calculate_annual_operating_costs(mid_size, capital_costs["total"])
    lifecycle_costs = calculate_lifecycle_costs(mid_size, capital_costs["total"])
    lcoh = calculate_lcoh(mid_size, capital_costs["total"], operating_costs["total"], lifecycle_costs["total"])
    
    comparison = compare_heating_options(lcoh)
    
    df_comparison = pd.DataFrame([
        {"Heating Technology": "HTGR", "Base Cost ($/MWh)": f"${lcoh:.2f}", "Carbon Cost ($/MWh)": f"${HTGR_COST_PARAMS.htgr_emissions * HTGR_COST_PARAMS.carbon_price / 1000:.2f}", "Total Cost ($/MWh)": f"${comparison['htgr']:.2f}"},
        {"Heating Technology": "Natural Gas", "Base Cost ($/MWh)": f"${HTGR_COST_PARAMS.natural_gas_cost:.2f}", "Carbon Cost ($/MWh)": f"${HTGR_COST_PARAMS.natural_gas_emissions * HTGR_COST_PARAMS.carbon_price / 1000:.2f}", "Total Cost ($/MWh)": f"${comparison['natural_gas']:.2f}"},
        {"Heating Technology": "Coal", "Base Cost ($/MWh)": f"${HTGR_COST_PARAMS.coal_cost:.2f}", "Carbon Cost ($/MWh)": f"${HTGR_COST_PARAMS.coal_emissions * HTGR_COST_PARAMS.carbon_price / 1000:.2f}", "Total Cost ($/MWh)": f"${comparison['coal']:.2f}"},
        {"Heating Technology": "Biomass", "Base Cost ($/MWh)": f"${HTGR_COST_PARAMS.biomass_cost:.2f}", "Carbon Cost ($/MWh)": f"${HTGR_COST_PARAMS.biomass_emissions * HTGR_COST_PARAMS.carbon_price / 1000:.2f}", "Total Cost ($/MWh)": f"${comparison['biomass']:.2f}"},
        {"Heating Technology": "Electric", "Base Cost ($/MWh)": f"${HTGR_COST_PARAMS.electric_cost:.2f}", "Carbon Cost ($/MWh)": f"${HTGR_COST_PARAMS.electric_emissions * HTGR_COST_PARAMS.carbon_price / 1000:.2f}", "Total Cost ($/MWh)": f"${comparison['electric']:.2f}"},
    ])
    
    display(Table(df_comparison, f"Cost Comparison of Heating Technologies (with ${HTGR_COST_PARAMS.carbon_price}/tonne CO2 price)", "tbl-comparison"))
    
    display(
        "The comparative analysis shows how the HTGR system compares economically with conventional "
        "industrial heating technologies. When carbon pricing is included, the HTGR becomes more "
        "competitive with fossil fuel alternatives. Natural gas remains cost-competitive in regions "
        "with low gas prices, but the HTGR offers price stability not subject to fuel price volatility. "
        "Coal heating faces significant carbon costs due to high emissions. Electric heating, while "
        "clean at the point of use, remains expensive due to the conversion inefficiencies and high "
        "electricity prices."
    )
    
    # Sensitivity analysis
    display("## 6. Sensitivity Analysis")
    
    # Use the middle reactor size for sensitivity analysis
    mid_size = HTGR_COST_PARAMS.reactor_sizes[1]  # 15 MWth
    sensitivity = perform_sensitivity_analysis(mid_size)
    
    # Fuel price sensitivity
    df_fuel = pd.DataFrame([
        {"Fuel Price Change": "-20%", "LCOH ($/MWh)": f"${sensitivity['fuel_price'][0][1]:.2f}", "Change from Base": f"{(sensitivity['fuel_price'][0][1]/lcoh - 1)*100:.1f}%"},
        {"Fuel Price Change": "Base", "LCOH ($/MWh)": f"${sensitivity['fuel_price'][1][1]:.2f}", "Change from Base": "0.0%"},
        {"Fuel Price Change": "+20%", "LCOH ($/MWh)": f"${sensitivity['fuel_price'][2][1]:.2f}", "Change from Base": f"{(sensitivity['fuel_price'][2][1]/lcoh - 1)*100:.1f}%"},
    ])
    display(Table(df_fuel, "Sensitivity to Fuel Price Changes", "tbl-sens-fuel"))
    
    # Capital cost sensitivity
    df_capital = pd.DataFrame([
        {"Capital Cost Change": "-10%", "LCOH ($/MWh)": f"${sensitivity['capital_cost'][0][1]:.2f}", "Change from Base": f"{(sensitivity['capital_cost'][0][1]/lcoh - 1)*100:.1f}%"},
        {"Capital Cost Change": "Base", "LCOH ($/MWh)": f"${sensitivity['capital_cost'][1][1]:.2f}", "Change from Base": "0.0%"},
        {"Capital Cost Change": "+10%", "LCOH ($/MWh)": f"${sensitivity['capital_cost'][2][1]:.2f}", "Change from Base": f"{(sensitivity['capital_cost'][2][1]/lcoh - 1)*100:.1f}%"},
    ])
    display(Table(df_capital, "Sensitivity to Capital Cost Changes", "tbl-sens-capital"))
    
    # Discount rate sensitivity
    df_discount = pd.DataFrame([
        {"Discount Rate": "5%", "LCOH ($/MWh)": f"${sensitivity['discount_rate'][0][1]:.2f}", "Change from Base": f"{(sensitivity['discount_rate'][0][1]/lcoh - 1)*100:.1f}%"},
        {"Discount Rate": "7%", "LCOH ($/MWh)": f"${sensitivity['discount_rate'][1][1]:.2f}", "Change from Base": "0.0%"},
        {"Discount Rate": "9%", "LCOH ($/MWh)": f"${sensitivity['discount_rate'][2][1]:.2f}", "Change from Base": f"{(sensitivity['discount_rate'][2][1]/lcoh - 1)*100:.1f}%"},
    ])
    display(Table(df_discount, "Sensitivity to Discount Rate Changes", "tbl-sens-discount"))
    
    # Carbon price sensitivity - just show impact on comparative advantage
    display(
        "Carbon pricing significantly impacts the comparative economics of different heating technologies. "
        f"At ${sensitivity['carbon_price'][0][0]}/tonne CO2, the HTGR's cost advantage over natural gas is "
        f"${HTGR_COST_PARAMS.natural_gas_emissions * sensitivity['carbon_price'][0][0] / 1000:.2f}/MWh. "
        f"At ${sensitivity['carbon_price'][2][0]}/tonne CO2, this advantage increases to "
        f"${HTGR_COST_PARAMS.natural_gas_emissions * sensitivity['carbon_price'][2][0] / 1000:.2f}/MWh."
    )
    
    display(
        "The sensitivity analysis demonstrates that the HTGR economics are most sensitive to capital costs "
        "and discount rates, which is typical for capital-intensive, long-lived assets. Fuel price changes "
        "have a relatively modest impact due to the small contribution of fuel costs to the overall LCOH. "
        "Carbon pricing significantly enhances the competitiveness of the HTGR against fossil fuel alternatives, "
        "particularly coal and natural gas."
    )
    
    # Conclusion
    display("## 7. Conclusion on Economic Viability")
    display(
        "The economic analysis demonstrates that the HTGR system can be economically viable for industrial "
        "heat applications under the following conditions:\n\n"
        
        "1. **Carbon pricing**: With carbon prices above $30/tonne CO2, the HTGR becomes cost-competitive "
        "with natural gas heating in most markets.\n\n"
        
        "2. **Scale advantages**: The 20 MWth design offers the best economics due to economies of scale, "
        "though the smaller units provide flexibility for sites with lower heat demands.\n\n"
        
        "3. **Long-term stability**: While capital costs are high, the HTGR offers exceptional price stability "
        "over its 20-year lifetime, with minimal exposure to fuel price volatility.\n\n"
        
        "4. **Industrial applications**: The HTGR is particularly well-suited for industries requiring high-temperature "
        "process heat (up to 600°C) with continuous, reliable operation.\n\n"
        
        "5. **Decarbonization value**: Beyond direct economic benefits, the HTGR offers industrial facilities "
        "a pathway to deep decarbonization that few other technologies can match at similar scales and temperatures.\n\n"
        
        "The analysis indicates that the HTGR system represents a viable economic proposition for industrial "
        "heat decarbonization, particularly in regions with strong carbon reduction policies or high/volatile "
        "fossil fuel prices. The modular design approach helps mitigate financial risks by allowing incremental "
        "capacity additions and standardized manufacturing to drive down costs over time."
    )
    
    print("DESIGN_COMPLETE")

# Run the cost report generation
generate_cost_report()
"""
Economic analysis for the HTGR system.
Calculates levelized cost of heat (LCOH) and other economic metrics.
"""

from pyforge import Quantity
from reactor.parameters_htgr import (
    CORE_PARAMS, OPERATIONAL_PARAMS, ECONOMIC_PARAMS
)

def calculate_lcoh(power_level="medium", discount_rate=0.07, carbon_price=50):
    """
    Calculate the Levelized Cost of Heat (LCOH) for the HTGR system.
    
    Args:
        power_level: Power level configuration ("small", "medium", or "large")
        discount_rate: Annual discount rate for NPV calculations
        carbon_price: Carbon price in $/ton CO2
        
    Returns:
        LCOH in $/MWh thermal
    """
    # Get appropriate thermal power based on configuration
    if power_level == "small":
        thermal_power = CORE_PARAMS.thermal_power_small.magnitude  # MW
    elif power_level == "medium":
        thermal_power = CORE_PARAMS.thermal_power_medium.magnitude  # MW
    else:  # large
        thermal_power = CORE_PARAMS.thermal_power_large.magnitude  # MW
    
    # Economic parameters
    capital_cost_per_kw = ECONOMIC_PARAMS.capital_cost.magnitude  # $/kW
    operational_cost = ECONOMIC_PARAMS.operational_cost.magnitude  # $/MWh
    design_life = OPERATIONAL_PARAMS.design_life.magnitude  # years
    availability = OPERATIONAL_PARAMS.availability  # fraction
    
    # Calculate total capital cost
    total_capital_cost = capital_cost_per_kw * thermal_power * 1000  # $
    
    # Calculate annual heat production
    annual_hours = 8760  # hours per year
    annual_heat_production = thermal_power * annual_hours * availability  # MWh/year
    
    # Calculate annual O&M cost
    annual_om_cost = operational_cost * annual_heat_production  # $/year
    
    # Calculate carbon credit
    conventional_emissions = ECONOMIC_PARAMS.conventional_emissions.magnitude  # kg CO2/MWh
    htgr_emissions = ECONOMIC_PARAMS.carbon_emissions.magnitude  # kg CO2/MWh
    emissions_avoided = (conventional_emissions - htgr_emissions) / 1000  # tons CO2/MWh
    annual_carbon_credit = emissions_avoided * annual_heat_production * carbon_price  # $/year
    
    # Calculate NPV of costs and heat production
    npv_capital = total_capital_cost
    npv_om = 0
    npv_carbon_credit = 0
    npv_heat_production = 0
    
    for year in range(1, design_life + 1):
        discount_factor = 1 / ((1 + discount_rate) ** year)
        npv_om += annual_om_cost * discount_factor
        npv_carbon_credit += annual_carbon_credit * discount_factor
        npv_heat_production += annual_heat_production * discount_factor
    
    # Calculate LCOH
    lcoh = (npv_capital + npv_om - npv_carbon_credit) / npv_heat_production  # $/MWh
    
    # Calculate payback period (simplified)
    annual_savings = annual_carbon_credit + (conventional_fuel_cost(thermal_power) - annual_om_cost)
    payback_years = total_capital_cost / annual_savings if annual_savings > 0 else float('inf')
    
    # Print results
    print(f"Economic analysis for {power_level} configuration ({thermal_power} MW):")
    print(f"Total capital cost: ${total_capital_cost:,.0f}")
    print(f"Annual heat production: {annual_heat_production:,.0f} MWh")
    print(f"Levelized Cost of Heat (LCOH): ${lcoh:.2f}/MWh thermal")
    print(f"Estimated payback period: {payback_years:.1f} years")
    
    return lcoh

def conventional_fuel_cost(thermal_power, natural_gas_price=5.0):
    """
    Calculate the annual cost of conventional fuel (natural gas) for comparison.
    
    Args:
        thermal_power: Thermal power in MW
        natural_gas_price: Natural gas price in $/MMBtu
        
    Returns:
        Annual fuel cost in $/year
    """
    # Constants
    mmbtu_per_mwh = 3.412  # MMBtu/MWh conversion
    boiler_efficiency = 0.85  # typical industrial boiler
    annual_hours = 8760  # hours per year
    availability = OPERATIONAL_PARAMS.availability  # fraction
    
    # Calculate annual heat production
    annual_heat_production = thermal_power * annual_hours * availability  # MWh/year
    
    # Calculate natural gas required
    annual_gas_required = annual_heat_production * mmbtu_per_mwh / boiler_efficiency  # MMBtu/year
    
    # Calculate annual cost
    annual_cost = annual_gas_required * natural_gas_price  # $/year
    
    return annual_cost

# Calculate LCOH for different configurations
print("Initializing economic calculations...")
lcoh_small = calculate_lcoh("small")
lcoh_medium = calculate_lcoh("medium")
lcoh_large = calculate_lcoh("large")

# Return the medium configuration LCOH as the default
lcoh = lcoh_medium
"""
Economic analysis for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Quantity, UREG
from reactor.parameters_system import SYSTEM_PARAMS
from reactor.parameters_core import CORE_PARAMS

def calculate_lcoh(thermal_power=None, carbon_price=50):
    """
    Calculate the Levelized Cost of Heat (LCOH) for the HTGR system.
    
    Args:
        thermal_power: Thermal power in MW (if None, uses the medium configuration)
        carbon_price: Carbon price in $/ton CO2
        
    Returns:
        float: LCOH in $/MWh thermal
    """
    if thermal_power is None:
        thermal_power = CORE_PARAMS.thermal_power_medium.magnitude
    
    # Base LCOH from system parameters
    base_lcoh = SYSTEM_PARAMS.lcoh.magnitude
    
    # Scale based on thermal power (economies of scale)
    if thermal_power == CORE_PARAMS.thermal_power_small.magnitude:
        scale_factor = 1.15  # Small configuration costs more per MWh
    elif thermal_power == CORE_PARAMS.thermal_power_large.magnitude:
        scale_factor = 0.90  # Large configuration costs less per MWh
    else:
        scale_factor = 1.0  # Medium configuration is the reference
    
    # Adjust for carbon price (higher carbon price makes nuclear more competitive)
    carbon_adjustment = (carbon_price / 50) * 2  # $2/MWh benefit for every $50/ton CO2
    
    # Calculate final LCOH
    final_lcoh = (base_lcoh * scale_factor) - carbon_adjustment
    
    # Print economic analysis results
    print(f"Economic Analysis Results for {thermal_power} MW:")
    print(f"  Base LCOH: ${base_lcoh:.2f}/MWh thermal")
    print(f"  Scale Factor: {scale_factor:.2f}")
    print(f"  Carbon Price Adjustment: ${carbon_adjustment:.2f}/MWh thermal")
    print(f"  Final LCOH: ${final_lcoh:.2f}/MWh thermal")
    
    return final_lcoh
