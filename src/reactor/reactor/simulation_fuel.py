"""
Fuel management simulation for the Small Modular Reactor.
Performs fuel cycle analysis and burnup calculations.
"""

from reactor.parameters_reactor import REACTOR_PARAMS

def calculate_fuel_cycle():
    """Calculate fuel cycle parameters and burnup."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    core_volume = 3.14159 * (REACTOR_PARAMS.core_diameter.magnitude/2)**2 * REACTOR_PARAMS.core_height.magnitude  # m³
    fuel_enrichment = REACTOR_PARAMS.fuel_enrichment.magnitude  # %
    fuel_assembly_count = REACTOR_PARAMS.fuel_assembly_count
    refueling_interval = REACTOR_PARAMS.refueling_interval.magnitude  # years
    
    print(f"DEBUG: thermal_power={thermal_power}, fuel_enrichment={fuel_enrichment}, assemblies={fuel_assembly_count}")
    
    # Calculate power density
    power_density = thermal_power / core_volume  # MW/m³
    
    # Use uranium loading from parameters instead of estimating
    if hasattr(REACTOR_PARAMS, 'uranium_loading'):
        total_uranium = REACTOR_PARAMS.uranium_loading.magnitude  # kg
    else:
        # Fallback to estimation if parameter not available
        uranium_density = 100  # kgU/m³
        total_uranium = uranium_density * core_volume  # kg
    
    # Calculate U-235 content
    u235_content = total_uranium * fuel_enrichment / 100  # kg
    
    # Calculate burnup based on required energy production for the refueling interval
    # For HALEU fuel with 19.75% enrichment, we can achieve higher burnup
    capacity_factor = REACTOR_PARAMS.capacity_factor.magnitude / 100 if hasattr(REACTOR_PARAMS, 'capacity_factor') else 0.9
    full_power_days = refueling_interval * 365 * capacity_factor
    energy_produced = thermal_power * full_power_days  # MWd
    average_burnup = (energy_produced / (total_uranium / 1000))  # MWd/kgU or GWd/tU
    
    # Calculate energy produced per kg of uranium
    energy_per_kg = average_burnup * 1000 / 1000  # MWd/kg
    
    # Calculate total energy from core
    total_energy = total_uranium * energy_per_kg  # MWd
    
    # Calculate core lifetime at full power
    full_power_days = total_energy / thermal_power  # days
    
    # Calculate capacity factor
    # Handle capacity_factor whether it's a Quantity or direct value
    if hasattr(REACTOR_PARAMS, 'capacity_factor'):
        if hasattr(REACTOR_PARAMS.capacity_factor, 'magnitude'):
            capacity_factor = REACTOR_PARAMS.capacity_factor.magnitude / 100
        else:
            capacity_factor = REACTOR_PARAMS.capacity_factor / 100
    else:
        # Default capacity factor if not defined
        capacity_factor = 0.90
        print(f"WARNING: capacity_factor not found in REACTOR_PARAMS, using default value of {capacity_factor}")
    
    print(f"DEBUG: capacity_factor={capacity_factor}")
    
    # Calculate actual core lifetime
    actual_lifetime = full_power_days / 365 / capacity_factor  # years
    
    print(f"\nFuel Cycle Analysis:")
    print(f"Core Power Density: {power_density:.2f} MW/m³")
    print(f"Total Uranium Loading: {total_uranium:.2f} kg")
    print(f"U-235 Content: {u235_content:.2f} kg ({fuel_enrichment}% enrichment)")
    print(f"Average Discharge Burnup: {average_burnup} GWd/tU")
    print(f"Full Power Core Lifetime: {full_power_days:.2f} days")
    print(f"Actual Core Lifetime: {actual_lifetime:.2f} years")
    
    if abs(actual_lifetime - refueling_interval) > 0.5:
        print(f"WARNING: Calculated core lifetime ({actual_lifetime:.2f} years) differs from design refueling interval ({refueling_interval} years)")
        print(f"Consider adjusting fuel loading or enrichment")
    else:
        print(f"PASS: Calculated core lifetime ({actual_lifetime:.2f} years) matches design refueling interval ({refueling_interval} years)")
    
    # Calculate fuel costs
    uranium_cost = 150  # $/kg UO2
    enrichment_cost = 1000  # $/SWU
    fabrication_cost = 300  # $/kg
    
    # Simplified SWU calculation
    swu_per_kg = 7.5 * fuel_enrichment / 5  # SWU/kg (approximation)
    
    # Calculate total fuel cost
    fuel_cost = total_uranium * (uranium_cost + fabrication_cost + swu_per_kg * enrichment_cost)  # $
    
    # Calculate fuel cost per MWh
    electricity_produced = thermal_power * 24 * full_power_days * REACTOR_PARAMS.electrical_power.magnitude / REACTOR_PARAMS.thermal_power.magnitude  # MWh
    fuel_cost_per_mwh = fuel_cost / electricity_produced  # $/MWh
    
    print(f"\nFuel Economics:")
    print(f"Total Fuel Cost: ${fuel_cost/1e6:.2f} million")
    print(f"Fuel Cost per MWh: ${fuel_cost_per_mwh:.2f}/MWh")
    
    return {
        "power_density": power_density,
        "total_uranium": total_uranium,
        "u235_content": u235_content,
        "core_lifetime": actual_lifetime,
        "fuel_cost_per_mwh": fuel_cost_per_mwh
    }

def analyze_fuel_management_strategy():
    """Analyze fuel management strategy and optimization."""
    fuel_assembly_count = REACTOR_PARAMS.fuel_assembly_count
    refueling_interval = REACTOR_PARAMS.refueling_interval.magnitude
    
    # Define fuel management strategies
    strategies = {
        "Single Batch": {
            "description": "All fuel assemblies replaced at each refueling",
            "discharge_burnup_factor": 1.0,
            "power_peaking_factor": 1.0,
            "fuel_utilization": "Low"
        },
        "3-Batch": {
            "description": "1/3 of fuel assemblies replaced at each refueling",
            "discharge_burnup_factor": 1.5,
            "power_peaking_factor": 1.3,
            "fuel_utilization": "Medium"
        },
        "4-Batch": {
            "description": "1/4 of fuel assemblies replaced at each refueling",
            "discharge_burnup_factor": 1.7,
            "power_peaking_factor": 1.4,
            "fuel_utilization": "High"
        }
    }
    
    # Select optimal strategy based on core size and refueling interval
    if fuel_assembly_count < 40:
        optimal_strategy = "3-Batch"
    else:
        optimal_strategy = "4-Batch"
    
    print(f"\nFuel Management Strategy Analysis:")
    print(f"Number of Fuel Assemblies: {fuel_assembly_count}")
    print(f"Refueling Interval: {refueling_interval} years")
    
    print(f"\nOptimal Strategy: {optimal_strategy}")
    print(f"Description: {strategies[optimal_strategy]['description']}")
    print(f"Discharge Burnup Factor: {strategies[optimal_strategy]['discharge_burnup_factor']}")
    print(f"Power Peaking Factor: {strategies[optimal_strategy]['power_peaking_factor']}")
    print(f"Fuel Utilization: {strategies[optimal_strategy]['fuel_utilization']}")
    
    # Calculate assemblies replaced per refueling
    if optimal_strategy == "Single Batch":
        assemblies_per_refueling = fuel_assembly_count
    elif optimal_strategy == "3-Batch":
        assemblies_per_refueling = fuel_assembly_count // 3
    else:  # 4-Batch
        assemblies_per_refueling = fuel_assembly_count // 4
    
    print(f"Assemblies Replaced per Refueling: {assemblies_per_refueling}")
    
    return {
        "optimal_strategy": optimal_strategy,
        "assemblies_per_refueling": assemblies_per_refueling,
        "discharge_burnup_factor": strategies[optimal_strategy]['discharge_burnup_factor']
    }

# Run fuel simulations
print("\n=== FUEL SIMULATION RESULTS ===\n")
fuel_cycle = calculate_fuel_cycle()
fuel_management = analyze_fuel_management_strategy()

print("\n=== FUEL SIMULATION SUMMARY ===")
print(f"Core Power Density: {fuel_cycle['power_density']:.2f} MW/m³")
print(f"Total Uranium: {fuel_cycle['total_uranium']:.2f} kg")
print(f"Core Lifetime: {fuel_cycle['core_lifetime']:.2f} years")
print(f"Fuel Management: {fuel_management['optimal_strategy']}")
print(f"Fuel Cost: ${fuel_cycle['fuel_cost_per_mwh']:.2f}/MWh")
"""
Fuel management simulation for the Small Modular Reactor.
Performs fuel cycle analysis and burnup calculations.
"""

from reactor.parameters_reactor import REACTOR_PARAMS

def calculate_fuel_cycle():
    """Calculate fuel cycle parameters and burnup."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    core_volume = 3.14159 * (REACTOR_PARAMS.core_diameter.magnitude/2)**2 * REACTOR_PARAMS.core_height.magnitude  # m³
    fuel_enrichment = REACTOR_PARAMS.fuel_enrichment.magnitude  # %
    fuel_assembly_count = REACTOR_PARAMS.fuel_assembly_count
    refueling_interval = REACTOR_PARAMS.refueling_interval.magnitude  # years
    
    print(f"DEBUG: thermal_power={thermal_power}, fuel_enrichment={fuel_enrichment}, assemblies={fuel_assembly_count}")
    
    # Calculate power density
    power_density = thermal_power / core_volume  # MW/m³
    
    # Estimate uranium loading (typical PWR value ~100 kgU/m³)
    uranium_density = 100  # kgU/m³
    total_uranium = uranium_density * core_volume  # kg
    
    # Calculate U-235 content
    u235_content = total_uranium * fuel_enrichment / 100  # kg
    
    # Estimate burnup (typical PWR value ~45 GWd/tU)
    average_burnup = 45  # GWd/tU
    
    # Calculate energy produced per kg of uranium
    energy_per_kg = average_burnup * 1000 / 1000  # MWd/kg
    
    # Calculate total energy from core
    total_energy = total_uranium * energy_per_kg  # MWd
    
    # Calculate core lifetime at full power
    full_power_days = total_energy / thermal_power  # days
    
    # Calculate capacity factor
    # Handle capacity_factor whether it's a Quantity or direct value
    if hasattr(REACTOR_PARAMS, 'capacity_factor'):
        if hasattr(REACTOR_PARAMS.capacity_factor, 'magnitude'):
            capacity_factor = REACTOR_PARAMS.capacity_factor.magnitude / 100
        else:
            capacity_factor = REACTOR_PARAMS.capacity_factor / 100
    else:
        # Default capacity factor if not defined
        capacity_factor = 0.90
        print(f"WARNING: capacity_factor not found in REACTOR_PARAMS, using default value of {capacity_factor}")
    
    print(f"DEBUG: capacity_factor={capacity_factor}")
    
    # Calculate actual core lifetime
    actual_lifetime = full_power_days / 365 / capacity_factor  # years
    
    print(f"\nFuel Cycle Analysis:")
    print(f"Core Power Density: {power_density:.2f} MW/m³")
    print(f"Total Uranium Loading: {total_uranium:.2f} kg")
    print(f"U-235 Content: {u235_content:.2f} kg ({fuel_enrichment}% enrichment)")
    print(f"Average Discharge Burnup: {average_burnup} GWd/tU")
    print(f"Full Power Core Lifetime: {full_power_days:.2f} days")
    print(f"Actual Core Lifetime: {actual_lifetime:.2f} years")
    
    if abs(actual_lifetime - refueling_interval) > 0.5:
        print(f"WARNING: Calculated core lifetime ({actual_lifetime:.2f} years) differs from design refueling interval ({refueling_interval} years)")
        print(f"Consider adjusting fuel loading or enrichment")
    else:
        print(f"PASS: Calculated core lifetime ({actual_lifetime:.2f} years) matches design refueling interval ({refueling_interval} years)")
    
    # Calculate fuel costs
    uranium_cost = 150  # $/kg UO2
    enrichment_cost = 1000  # $/SWU
    fabrication_cost = 300  # $/kg
    
    # Simplified SWU calculation
    swu_per_kg = 7.5 * fuel_enrichment / 5  # SWU/kg (approximation)
    
    # Calculate total fuel cost
    fuel_cost = total_uranium * (uranium_cost + fabrication_cost + swu_per_kg * enrichment_cost)  # $
    
    # Calculate fuel cost per MWh
    electricity_produced = thermal_power * 24 * full_power_days * REACTOR_PARAMS.electrical_power.magnitude / REACTOR_PARAMS.thermal_power.magnitude  # MWh
    fuel_cost_per_mwh = fuel_cost / electricity_produced  # $/MWh
    
    print(f"\nFuel Economics:")
    print(f"Total Fuel Cost: ${fuel_cost/1e6:.2f} million")
    print(f"Fuel Cost per MWh: ${fuel_cost_per_mwh:.2f}/MWh")
    
    return {
        "power_density": power_density,
        "total_uranium": total_uranium,
        "u235_content": u235_content,
        "core_lifetime": actual_lifetime,
        "fuel_cost_per_mwh": fuel_cost_per_mwh
    }

def analyze_fuel_management_strategy():
    """Analyze fuel management strategy and optimization."""
    fuel_assembly_count = REACTOR_PARAMS.fuel_assembly_count
    refueling_interval = REACTOR_PARAMS.refueling_interval.magnitude
    
    # Define fuel management strategies
    strategies = {
        "Single Batch": {
            "description": "All fuel assemblies replaced at each refueling",
            "discharge_burnup_factor": 1.0,
            "power_peaking_factor": 1.0,
            "fuel_utilization": "Low"
        },
        "3-Batch": {
            "description": "1/3 of fuel assemblies replaced at each refueling",
            "discharge_burnup_factor": 1.5,
            "power_peaking_factor": 1.3,
            "fuel_utilization": "Medium"
        },
        "4-Batch": {
            "description": "1/4 of fuel assemblies replaced at each refueling",
            "discharge_burnup_factor": 1.7,
            "power_peaking_factor": 1.4,
            "fuel_utilization": "High"
        }
    }
    
    # Select optimal strategy based on core size and refueling interval
    if fuel_assembly_count < 40:
        optimal_strategy = "3-Batch"
    else:
        optimal_strategy = "4-Batch"
    
    print(f"\nFuel Management Strategy Analysis:")
    print(f"Number of Fuel Assemblies: {fuel_assembly_count}")
    print(f"Refueling Interval: {refueling_interval} years")
    
    print(f"\nOptimal Strategy: {optimal_strategy}")
    print(f"Description: {strategies[optimal_strategy]['description']}")
    print(f"Discharge Burnup Factor: {strategies[optimal_strategy]['discharge_burnup_factor']}")
    print(f"Power Peaking Factor: {strategies[optimal_strategy]['power_peaking_factor']}")
    print(f"Fuel Utilization: {strategies[optimal_strategy]['fuel_utilization']}")
    
    # Calculate assemblies replaced per refueling
    if optimal_strategy == "Single Batch":
        assemblies_per_refueling = fuel_assembly_count
    elif optimal_strategy == "3-Batch":
        assemblies_per_refueling = fuel_assembly_count // 3
    else:  # 4-Batch
        assemblies_per_refueling = fuel_assembly_count // 4
    
    print(f"Assemblies Replaced per Refueling: {assemblies_per_refueling}")
    
    return {
        "optimal_strategy": optimal_strategy,
        "assemblies_per_refueling": assemblies_per_refueling,
        "discharge_burnup_factor": strategies[optimal_strategy]['discharge_burnup_factor']
    }

# Run fuel simulations
print("\n=== FUEL SIMULATION RESULTS ===\n")
fuel_cycle = calculate_fuel_cycle()
fuel_management = analyze_fuel_management_strategy()

print("\n=== FUEL SIMULATION SUMMARY ===")
print(f"Core Power Density: {fuel_cycle['power_density']:.2f} MW/m³")
print(f"Total Uranium: {fuel_cycle['total_uranium']:.2f} kg")
print(f"Core Lifetime: {fuel_cycle['core_lifetime']:.2f} years")
print(f"Fuel Management: {fuel_management['optimal_strategy']}")
print(f"Fuel Cost: ${fuel_cycle['fuel_cost_per_mwh']:.2f}/MWh")
