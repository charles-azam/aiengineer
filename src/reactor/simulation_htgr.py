"""
Simulation module for High-Temperature Gas-cooled Reactor (HTGR) system.

This module provides functions to simulate the thermal and fluid dynamics
of an HTGR system, including core heat generation, coolant properties,
heat transfer, and safety margins.
"""
import math
from pyforge import Quantity
from reactor.parameters_htgr import HTGR_PARAMS

# Print debug information
print("Loading HTGR simulation module...")

def calculate_core_heat_generation(power_level: float = None) -> dict:
    """
    Calculate heat generation in the reactor core based on power parameters.
    
    Args:
        power_level: Optional override for thermal power in MW
        
    Returns:
        Dictionary with heat generation metrics
    """
    if power_level is None:
        power_level = HTGR_PARAMS.selected_power.to("MW").magnitude
    
    # Calculate power density based on core volume
    core_volume = HTGR_PARAMS.core_height.to("m").magnitude * (
        HTGR_PARAMS.core_diameter.to("m").magnitude / 2)**2 * 3.14159
    power_density = power_level / core_volume
    
    # Calculate fuel temperature based on power level and cooling
    base_temp = HTGR_PARAMS.core_inlet_temp.to("kelvin").magnitude
    temp_rise = power_level * 15  # Approximate temperature rise per MW
    max_fuel_temp = base_temp + temp_rise
    
    results = {
        "thermal_power_mw": power_level,
        "power_density_mw_per_m3": power_density,
        "max_fuel_temp_c": max_fuel_temp - 273.15,
        "total_energy_per_day_mwh": power_level * 24
    }
    
    print(f"Core heat generation: {power_level:.2f} MW at {power_density:.2f} MW/m³")
    print(f"Maximum fuel temperature: {results['max_fuel_temp_c']:.2f}°C")
    
    return results

def calculate_helium_properties(temperature: float = None, pressure: float = None) -> dict:
    """
    Calculate properties of helium coolant at operational conditions.
    
    Args:
        temperature: Optional override for helium temperature in °C
        pressure: Optional override for helium pressure in MPa
        
    Returns:
        Dictionary with helium properties
    """
    if temperature is None:
        temperature = HTGR_PARAMS.core_outlet_temperature.to("degC").magnitude
    if pressure is None:
        pressure = HTGR_PARAMS.helium_pressure.to("MPa").magnitude
    
    # Helium properties calculation based on temperature and pressure
    # Using simplified correlations for demonstration
    temp_k = temperature + 273.15
    
    # Helium specific heat capacity (J/kg·K) - nearly constant
    cp = 5193
    
    # Helium density (kg/m³) using ideal gas approximation
    density = pressure * 1e6 * 4.0026 / (8314.46 * temp_k)
    
    # Helium thermal conductivity (W/m·K)
    thermal_conductivity = 0.002682 * temp_k**0.71
    
    # Helium dynamic viscosity (Pa·s)
    viscosity = 3.674e-7 * temp_k**0.7
    
    results = {
        "temperature_c": temperature,
        "pressure_mpa": pressure,
        "density_kg_m3": density,
        "specific_heat_j_kgk": cp,
        "thermal_conductivity_w_mk": thermal_conductivity,
        "dynamic_viscosity_pa_s": viscosity
    }
    
    print(f"Helium properties at {temperature:.2f}°C, {pressure:.2f} MPa:")
    print(f"  Density: {density:.4f} kg/m³")
    print(f"  Specific heat: {cp:.2f} J/kg·K")
    
    return results

def calculate_co2_properties(temperature: float = None, pressure: float = None) -> dict:
    """
    Calculate properties of CO2 coolant in secondary loop.
    
    Args:
        temperature: Optional override for CO2 temperature in °C
        pressure: Optional override for CO2 pressure in MPa
        
    Returns:
        Dictionary with CO2 properties
    """
    if temperature is None:
        temperature = HTGR_PARAMS.secondary_inlet_temp.to("degC").magnitude
    if pressure is None:
        pressure = HTGR_PARAMS.secondary_pressure.to("MPa").magnitude
    
    temp_k = temperature + 273.15
    
    # CO2 properties calculation - simplified correlations
    # Specific heat capacity (J/kg·K)
    cp = 850 + 0.2 * temperature
    
    # CO2 density (kg/m³) - simplified correlation
    density = pressure * 44.01 / (0.1889 * temp_k)
    
    # CO2 thermal conductivity (W/m·K)
    thermal_conductivity = 0.0146 + 0.00005 * temperature
    
    # CO2 dynamic viscosity (Pa·s)
    viscosity = (1.37 + 0.003 * temperature) * 1e-5
    
    results = {
        "temperature_c": temperature,
        "pressure_mpa": pressure,
        "density_kg_m3": density,
        "specific_heat_j_kgk": cp,
        "thermal_conductivity_w_mk": thermal_conductivity,
        "dynamic_viscosity_pa_s": viscosity
    }
    
    print(f"CO2 properties at {temperature:.2f}°C, {pressure:.2f} MPa:")
    print(f"  Density: {density:.4f} kg/m³")
    print(f"  Specific heat: {cp:.2f} J/kg·K")
    
    return results

def calculate_heat_transfer(helium_flow_rate: float = None, co2_flow_rate: float = None) -> dict:
    """
    Calculate heat transfer from primary to secondary loop.
    
    Args:
        helium_flow_rate: Optional override for helium flow rate in kg/s
        co2_flow_rate: Optional override for CO2 flow rate in kg/s
        
    Returns:
        Dictionary with heat transfer metrics
    """
    if helium_flow_rate is None:
        helium_flow_rate = HTGR_PARAMS.helium_flow_rate.to("kg/s").magnitude
    if co2_flow_rate is None:
        co2_flow_rate = HTGR_PARAMS.secondary_flow_rate.to("kg/s").magnitude
    
    # Get coolant properties
    helium_props = calculate_helium_properties()
    co2_props = calculate_co2_properties()
    
    # Calculate temperature differences
    helium_temp_in = HTGR_PARAMS.core_inlet_temp.to("degC").magnitude
    helium_temp_out = HTGR_PARAMS.core_outlet_temp.to("degC").magnitude
    co2_temp_in = HTGR_PARAMS.secondary_inlet_temp.to("degC").magnitude
    co2_temp_out = HTGR_PARAMS.secondary_outlet_temp.to("degC").magnitude
    
    # Calculate heat transfer in heat exchanger
    helium_heat_capacity = helium_flow_rate * helium_props["specific_heat_j_kgk"]
    co2_heat_capacity = co2_flow_rate * co2_props["specific_heat_j_kgk"]
    
    helium_heat_transfer = helium_heat_capacity * (helium_temp_out - helium_temp_in)
    co2_heat_transfer = co2_heat_capacity * (co2_temp_out - co2_temp_in)
    
    # Calculate heat exchanger effectiveness
    max_possible_heat_transfer = min(helium_heat_capacity, co2_heat_capacity) * (
        helium_temp_out - co2_temp_in)
    effectiveness = co2_heat_transfer / max_possible_heat_transfer
    
    # Calculate overall heat transfer coefficient (simplified)
    heat_exchanger_area = HTGR_PARAMS.heat_exchanger_area.to("m^2").magnitude
    log_mean_temp_diff = ((helium_temp_out - co2_temp_out) - 
                          (helium_temp_in - co2_temp_in)) / (
                          math.log((helium_temp_out - co2_temp_out) / 
                                  (helium_temp_in - co2_temp_in)))
    overall_htc = co2_heat_transfer / (heat_exchanger_area * log_mean_temp_diff)
    
    results = {
        "helium_heat_transfer_mw": helium_heat_transfer / 1e6,
        "co2_heat_transfer_mw": co2_heat_transfer / 1e6,
        "heat_exchanger_effectiveness": effectiveness,
        "overall_heat_transfer_coefficient_w_m2k": overall_htc
    }
    
    print(f"Heat transfer: {co2_heat_transfer/1e6:.2f} MW")
    print(f"Heat exchanger effectiveness: {effectiveness:.2f}")
    
    return results

def calculate_thermal_efficiency() -> dict:
    """
    Calculate overall thermal efficiency of the HTGR system.
    
    Returns:
        Dictionary with efficiency metrics
    """
    # Get heat transfer data
    heat_transfer = calculate_heat_transfer()
    
    # Calculate thermal efficiency
    thermal_power = HTGR_PARAMS.selected_power.to("MW").magnitude
    heat_delivered = heat_transfer["co2_heat_transfer_mw"]
    
    # Account for pumping power (simplified)
    helium_pumping_power = 0.05 * thermal_power  # Assume 5% for primary loop pumping
    co2_pumping_power = 0.03 * thermal_power     # Assume 3% for secondary loop pumping
    
    # Calculate net efficiency
    gross_efficiency = heat_delivered / thermal_power
    net_efficiency = (heat_delivered - helium_pumping_power - co2_pumping_power) / thermal_power
    
    results = {
        "thermal_power_mw": thermal_power,
        "heat_delivered_mw": heat_delivered,
        "helium_pumping_power_mw": helium_pumping_power,
        "co2_pumping_power_mw": co2_pumping_power,
        "gross_efficiency": gross_efficiency,
        "net_efficiency": net_efficiency
    }
    
    print(f"Thermal efficiency:")
    print(f"  Gross: {gross_efficiency:.2%}")
    print(f"  Net: {net_efficiency:.2%}")
    
    return results

def calculate_safety_margins() -> dict:
    """
    Calculate safety margins including passive decay heat removal capability.
    
    Returns:
        Dictionary with safety margin metrics
    """
    # Get core heat generation data
    core_heat = calculate_core_heat_generation()
    
    # Calculate decay heat after shutdown (simplified)
    # Using Way-Wigner formula: P/P₀ = 0.066 * (t^-0.2 - (t+T)^-0.2)
    # where t is time after shutdown in seconds, T is operating time
    
    operating_time_days = 365 * HTGR_PARAMS.core_lifetime.magnitude
    thermal_power = HTGR_PARAMS.thermal_power.to("MW").magnitude
    
    # Calculate decay heat at different times
    decay_heat_1hr = thermal_power * 0.066 * (3600**-0.2)
    decay_heat_1day = thermal_power * 0.066 * (86400**-0.2)
    decay_heat_1week = thermal_power * 0.066 * ((7*86400)**-0.2)
    
    # Calculate passive heat removal capacity (simplified)
    # Based on radiation and natural convection from reactor vessel
    vessel_surface_area = 3.14159 * HTGR_PARAMS.vessel_diameter.to("m").magnitude * (
        HTGR_PARAMS.vessel_height.to("m").magnitude)
    
    # Simplified passive cooling capacity calculation
    max_vessel_temp = 400  # °C
    ambient_temp = 30      # °C
    
    # Stefan-Boltzmann constant
    sigma = 5.67e-8  # W/(m²·K⁴)
    
    # Emissivity of vessel surface
    emissivity = 0.8
    
    # Radiation heat transfer (W)
    radiation_cooling = (emissivity * sigma * vessel_surface_area * 
                        ((max_vessel_temp + 273.15)**4 - (ambient_temp + 273.15)**4))
    
    # Natural convection (simplified)
    convection_coeff = 5  # W/(m²·K), typical for natural convection in air
    convection_cooling = convection_coeff * vessel_surface_area * (max_vessel_temp - ambient_temp)
    
    # Total passive cooling capacity
    passive_cooling_capacity = (radiation_cooling + convection_cooling) / 1e6  # MW
    
    # Safety margins
    margin_1hr = passive_cooling_capacity / decay_heat_1hr
    margin_1day = passive_cooling_capacity / decay_heat_1day
    margin_1week = passive_cooling_capacity / decay_heat_1week
    
    # Calculate temperature margins
    max_fuel_temp = core_heat["max_fuel_temp_c"]
    fuel_temp_limit = HTGR_PARAMS.fuel_temp_limit.to("degC").magnitude
    fuel_temp_margin = (fuel_temp_limit - max_fuel_temp) / fuel_temp_limit
    
    results = {
        "decay_heat_1hr_mw": decay_heat_1hr,
        "decay_heat_1day_mw": decay_heat_1day,
        "decay_heat_1week_mw": decay_heat_1week,
        "passive_cooling_capacity_mw": passive_cooling_capacity,
        "safety_margin_1hr": margin_1hr,
        "safety_margin_1day": margin_1day,
        "safety_margin_1week": margin_1week,
        "fuel_temp_margin": fuel_temp_margin
    }
    
    print(f"Safety margins:")
    print(f"  Decay heat (1 hour): {decay_heat_1hr:.2f} MW")
    print(f"  Passive cooling capacity: {passive_cooling_capacity:.2f} MW")
    print(f"  Safety margin (1 hour): {margin_1hr:.2f}")
    print(f"  Fuel temperature margin: {fuel_temp_margin:.2%}")
    
    return results

def validate_simulation_results(results: dict) -> bool:
    """
    Validate that simulation results are physically realistic.
    
    Args:
        results: Dictionary with all simulation results
        
    Returns:
        Boolean indicating whether results are valid
    """
    valid = True
    
    # Check thermal efficiency is realistic (between 30-50%)
    if not (0.3 <= results["efficiency"]["net_efficiency"] <= 0.5):
        print(f"WARNING: Net efficiency {results['efficiency']['net_efficiency']:.2%} outside expected range")
        valid = False
    
    # Check fuel temperature is below limit
    fuel_temp_limit = HTGR_PARAMS.fuel_temp_limit.to("degC").magnitude
    if results["core_heat"]["max_fuel_temp_c"] > fuel_temp_limit:
        print(f"WARNING: Fuel temperature {results['core_heat']['max_fuel_temp_c']:.2f}°C exceeds limit of {fuel_temp_limit}°C")
        valid = False
    
    # Check safety margins are adequate
    if results["safety"]["safety_margin_1hr"] < 1.0:
        print(f"WARNING: Insufficient safety margin for decay heat removal after 1 hour")
        valid = False
    
    return valid

def simulation_summary() -> dict:
    """
    Run a complete simulation and print a summary of all results.
    
    Returns:
        Dictionary with all simulation results
    """
    print("\n===== HTGR SIMULATION SUMMARY =====")
    print(f"HTGR System: {HTGR_PARAMS.selected_power} thermal output")
    print(f"Core dimensions: {HTGR_PARAMS.core_diameter} diameter × {HTGR_PARAMS.core_height} height")
    print("----------------------------------")
    
    # Run all calculations
    core_heat = calculate_core_heat_generation()
    helium_props = calculate_helium_properties()
    co2_props = calculate_co2_properties()
    heat_transfer = calculate_heat_transfer()
    efficiency = calculate_thermal_efficiency()
    safety = calculate_safety_margins()
    
    # Compile all results
    results = {
        "core_heat": core_heat,
        "helium_props": helium_props,
        "co2_props": co2_props,
        "heat_transfer": heat_transfer,
        "efficiency": efficiency,
        "safety": safety
    }
    
    # Validate results
    valid = validate_simulation_results(results)
    
    print("----------------------------------")
    if valid:
        print("Simulation completed successfully. All parameters within expected ranges.")
    else:
        print("Simulation completed with warnings. Some parameters outside expected ranges.")
    
    return results

if __name__ == "__main__":
    print("\n===== Running HTGR Simulation =====")
    try:
        results = simulation_summary()
        print("\n===== Simulation Complete =====")
        print("\nDESIGN_COMPLETE")
    except Exception as e:
        print(f"Error in simulation: {e}")
"""
Simulation and performance calculations for HTGR system.
"""
from reactor.parameters_htgr import HTGR_PARAMS
from pyforge import Quantity

print("Loading HTGR performance calculations...")

def calculate_efficiency(outlet_temp: Quantity) -> float:
    """
    Calculate thermal efficiency based on outlet temperature.
    Uses a simplified model where efficiency increases with temperature.
    
    Args:
        outlet_temp: Core outlet temperature
        
    Returns:
        Thermal efficiency as a fraction
    """
    # Simplified efficiency model based on temperature
    # Higher temperatures yield better efficiency
    base_efficiency = 0.30  # Base efficiency at reference temperature
    reference_temp = Quantity(350, "°C")
    temp_factor = 0.0005  # Efficiency increase per degree C
    
    temp_diff = outlet_temp.to("°C").magnitude - reference_temp.to("°C").magnitude
    efficiency = base_efficiency + (temp_factor * temp_diff)
    
    # Cap at reasonable values
    return min(max(efficiency, 0.25), 0.45)

def calculate_capital_cost(thermal_power: Quantity) -> Quantity:
    """
    Calculate approximate capital cost based on thermal power output.
    
    Args:
        thermal_power: Thermal power output
        
    Returns:
        Approximate capital cost in USD
    """
    # Simplified cost model with economies of scale
    base_cost = Quantity(30000000, "USD")  # Base cost for reference unit
    reference_power = Quantity(10, "MW")
    scaling_factor = 0.7  # Cost scaling factor (less than 1 for economies of scale)
    
    power_ratio = thermal_power.to("MW").magnitude / reference_power.to("MW").magnitude
    cost = base_cost.magnitude * (power_ratio ** scaling_factor)
    
    return Quantity(cost, "USD")

def calculate_annual_heat_production(thermal_power: Quantity, capacity_factor: float = 0.9) -> Quantity:
    """
    Calculate annual heat production based on thermal power and capacity factor.
    
    Args:
        thermal_power: Thermal power output
        capacity_factor: Annual capacity factor (default 0.9)
        
    Returns:
        Annual heat production in MWh
    """
    hours_per_year = 8760
    annual_production = thermal_power.to("MW").magnitude * hours_per_year * capacity_factor
    
    return Quantity(annual_production, "MW*hour")

def calculate_lcoh(capital_cost: Quantity, annual_heat: Quantity, 
                  fixed_om_rate: float = 0.04, fuel_cost: float = 5.0,
                  discount_rate: float = 0.07, lifetime: int = 20) -> float:
    """
    Calculate Levelized Cost of Heat (LCOH) in USD/MWh.
    
    Args:
        capital_cost: Total capital cost in USD
        annual_heat: Annual heat production in MWh
        fixed_om_rate: Fixed O&M as fraction of capital cost
        fuel_cost: Fuel cost in USD/MWh-thermal
        discount_rate: Annual discount rate
        lifetime: Plant lifetime in years
        
    Returns:
        LCOH in USD/MWh
    """
    # Capital recovery factor
    crf = discount_rate * (1 + discount_rate)**lifetime / ((1 + discount_rate)**lifetime - 1)
    
    # Annualized capital cost
    annual_capital = capital_cost.magnitude * crf
    
    # Fixed O&M cost
    annual_om = capital_cost.magnitude * fixed_om_rate
    
    # Fuel cost
    annual_fuel = annual_heat.magnitude * fuel_cost
    
    # Total annual cost
    total_annual_cost = annual_capital + annual_om + annual_fuel
    
    # LCOH
    lcoh = total_annual_cost / annual_heat.magnitude
    
    return lcoh

def get_performance_metrics() -> dict:
    """
    Calculate and return performance metrics for all HTGR variants.
    
    Returns:
        Dictionary with performance metrics for each variant
    """
    variants = {
        'small': {
            'thermal_power': HTGR_PARAMS.thermal_power_options[0],
        },
        'medium': {
            'thermal_power': HTGR_PARAMS.thermal_power_options[1],
        },
        'large': {
            'thermal_power': HTGR_PARAMS.thermal_power_options[2],
        }
    }
    
    # Calculate metrics for each variant
    for variant, data in variants.items():
        thermal_power = data['thermal_power']
        
        # Calculate efficiency
        efficiency = calculate_efficiency(HTGR_PARAMS.core_outlet_temperature)
        data['efficiency'] = efficiency
        
        # Calculate potential electrical output
        electrical_potential = thermal_power.magnitude * efficiency
        data['electrical_potential'] = electrical_potential
        
        # Calculate capital cost
        capital_cost = calculate_capital_cost(thermal_power)
        data['capital_cost'] = capital_cost
        
        # Calculate annual heat production
        annual_heat = calculate_annual_heat_production(thermal_power)
        data['annual_heat_production'] = annual_heat
        
        # Calculate LCOH
        lcoh = calculate_lcoh(capital_cost, annual_heat)
        data['lcoh'] = lcoh
    
    return variants

# Print performance metrics when run directly
print("HTGR Performance Metrics:")
performance_metrics = get_performance_metrics()
for variant, metrics in performance_metrics.items():
    print(f"\n{variant.capitalize()} Variant ({metrics['thermal_power']}):")
    print(f"  Thermal Efficiency: {metrics['efficiency']:.2%}")
    print(f"  Potential Electrical Output: {metrics['electrical_potential']:.2f} MW")
    print(f"  Capital Cost: ${metrics['capital_cost'].magnitude:,.0f}")
    print(f"  Annual Heat Production: {metrics['annual_heat_production'].magnitude:,.0f} MWh")
    print(f"  LCOH: ${metrics['lcoh']:.2f}/MWh")

print("\nDESIGN_COMPLETE")
