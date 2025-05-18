"""
Safety simulation for the Small Modular Reactor.
Performs basic safety calculations to validate the design.
"""

from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, CONTAINMENT_PARAMS

def calculate_decay_heat():
    """Calculate decay heat after shutdown using simplified Way-Wigner formula."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    
    print(f"DEBUG: thermal_power={thermal_power}")
    
    # Calculate decay heat at different times after shutdown
    times = [0, 1, 10, 24, 72, 168]  # hours after shutdown
    decay_powers = []
    
    for t in times:
        if t == 0:
            decay_power = thermal_power * 0.065  # ~6.5% at shutdown
        else:
            # Simplified Way-Wigner formula: P/P₀ = 0.066 × [(t₁^(-0.2)) - (t₂^(-0.2))]
            # where t₁ is time after shutdown in seconds, t₂ is t₁ + reactor operating time
            # Assuming long operation time, we simplify to P/P₀ ≈ 0.066 × t^(-0.2)
            decay_fraction = 0.066 * (t * 3600) ** (-0.2)
            decay_power = thermal_power * decay_fraction
        
        decay_powers.append(decay_power)
    
    print(f"Decay Heat Analysis:")
    print(f"Thermal Power: {thermal_power} MW")
    print(f"Time (hours) | Decay Heat (MW) | % of Full Power")
    for i, t in enumerate(times):
        print(f"{t:12} | {decay_powers[i]:14.2f} | {decay_powers[i]/thermal_power*100:13.2f}%")
    
    return decay_powers

def evaluate_passive_cooling_capability():
    """Evaluate if passive cooling systems can handle decay heat."""
    decay_powers = calculate_decay_heat()
    passive_cooling_capacity = CONTAINMENT_PARAMS.passive_cooling_capacity.magnitude  # MW
    
    print(f"DEBUG: passive_cooling_capacity={passive_cooling_capacity}")
    
    # Define times array to match the one in calculate_decay_heat
    times = [0, 1, 10, 24, 72, 168]  # hours after shutdown
    
    print(f"\nPassive Cooling Evaluation:")
    print(f"Passive Cooling Capacity: {passive_cooling_capacity} MW")
    
    # Check if passive cooling can handle decay heat at 72 hours (index 4)
    if decay_powers[4] <= passive_cooling_capacity:
        print(f"PASS: Passive cooling capacity ({passive_cooling_capacity} MW) exceeds decay heat at 72 hours ({decay_powers[4]:.2f} MW)")
    else:
        print(f"FAIL: Passive cooling capacity ({passive_cooling_capacity} MW) is insufficient for decay heat at 72 hours ({decay_powers[4]:.2f} MW)")
        print(f"Consider increasing passive cooling capacity to at least {decay_powers[4]:.2f} MW")
    
    # Calculate how long passive cooling is sufficient
    for i, power in enumerate(decay_powers):
        if power <= passive_cooling_capacity:
            if i > 0:
                print(f"Passive cooling becomes sufficient between {times[i-1]} and {times[i]} hours after shutdown")
            else:
                print(f"Passive cooling is sufficient immediately after shutdown")
            break
    
    return {
        "is_sufficient_at_72h": decay_powers[4] <= passive_cooling_capacity,
        "decay_heat_at_72h": decay_powers[4]
    }

def analyze_loca_scenario():
    """Analyze Loss of Coolant Accident (LOCA) scenario."""
    emergency_water = CONTAINMENT_PARAMS.emergency_water_supply.magnitude  # m³
    decay_heat_24h = calculate_decay_heat()[3]  # MW at 24 hours
    
    print(f"DEBUG: emergency_water={emergency_water}, decay_heat_24h={decay_heat_24h}")
    
    # Simplified calculation for water needed to absorb decay heat
    # Assuming water heats from 25°C to 100°C and then boils away
    water_heat_capacity = 4.18  # kJ/kg·K
    water_latent_heat = 2257  # kJ/kg
    water_density = 1000  # kg/m³
    
    # Energy to heat water from 25°C to 100°C and boil it
    energy_per_kg = water_heat_capacity * (100 - 25) + water_latent_heat  # kJ/kg
    energy_per_m3 = energy_per_kg * water_density / 1000  # MJ/m³
    
    # Calculate how long emergency water lasts
    # Convert decay heat from MW to MJ/h
    decay_heat_MJ_per_h = decay_heat_24h * 3600  # MJ/h
    
    # Calculate water consumption rate
    water_consumption_rate = decay_heat_MJ_per_h / energy_per_m3  # m³/h
    
    # Calculate how long emergency water lasts
    water_duration = emergency_water / water_consumption_rate  # hours
    
    print(f"\nLOCA Scenario Analysis:")
    print(f"Emergency Water Supply: {emergency_water} m³")
    print(f"Decay Heat at 24h: {decay_heat_24h:.2f} MW")
    print(f"Water Consumption Rate: {water_consumption_rate:.2f} m³/h")
    print(f"Emergency Water Duration: {water_duration:.2f} hours")
    
    if water_duration >= 72:
        print(f"PASS: Emergency water supply lasts for {water_duration:.2f} hours (>72h requirement)")
    else:
        print(f"FAIL: Emergency water supply only lasts for {water_duration:.2f} hours (<72h requirement)")
        print(f"Consider increasing emergency water supply to at least {water_consumption_rate * 72:.2f} m³")
    
    return {
        "water_duration": water_duration,
        "is_sufficient": water_duration >= 72
    }

def evaluate_containment_integrity():
    """Evaluate containment integrity under accident conditions."""
    design_pressure = CONTAINMENT_PARAMS.design_pressure.magnitude  # MPa
    wall_thickness = CONTAINMENT_PARAMS.wall_thickness.magnitude  # m
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude  # m
    
    print(f"DEBUG: design_pressure={design_pressure}, wall_thickness={wall_thickness}")
    
    # Calculate hoop stress in containment wall (simplified)
    # σ = P·r/t where P is pressure, r is radius, t is thickness
    radius = containment_diameter / 2  # m
    hoop_stress = design_pressure * radius / wall_thickness  # MPa
    
    # Typical concrete strength
    concrete_strength = 40  # MPa
    safety_factor = concrete_strength / hoop_stress
    
    print(f"\nContainment Integrity Analysis:")
    print(f"Containment Dimensions: {containment_diameter} m diameter, {wall_thickness} m wall thickness")
    print(f"Design Pressure: {design_pressure} MPa")
    print(f"Calculated Hoop Stress: {hoop_stress:.2f} MPa")
    print(f"Safety Factor: {safety_factor:.2f}")
    
    if safety_factor >= 3:
        print(f"PASS: Containment has adequate safety factor ({safety_factor:.2f} > 3)")
    else:
        print(f"WARNING: Containment safety factor ({safety_factor:.2f}) is below recommended value of 3")
        print(f"Consider increasing wall thickness or reducing containment diameter")
    
    return {
        "hoop_stress": hoop_stress,
        "safety_factor": safety_factor,
        "is_adequate": safety_factor >= 3
    }

# Run safety simulations
print("\n=== SAFETY SIMULATION RESULTS ===\n")
decay_heat_results = calculate_decay_heat()
passive_cooling_results = evaluate_passive_cooling_capability()
loca_results = analyze_loca_scenario()
containment_results = evaluate_containment_integrity()

print("\n=== SAFETY SIMULATION SUMMARY ===")
print(f"Decay Heat at 72h: {passive_cooling_results['decay_heat_at_72h']:.2f} MW")
print(f"Passive Cooling Adequacy: {'PASS' if passive_cooling_results['is_sufficient_at_72h'] else 'FAIL'}")
print(f"Emergency Water Duration: {loca_results['water_duration']:.2f} hours")
print(f"Containment Safety Factor: {containment_results['safety_factor']:.2f}")

# Overall safety assessment
safety_issues = []
if not passive_cooling_results['is_sufficient_at_72h']:
    safety_issues.append("Insufficient passive cooling capacity")
if not loca_results['is_sufficient']:
    safety_issues.append("Insufficient emergency water supply")
if not containment_results['is_adequate']:
    safety_issues.append("Inadequate containment safety factor")

if safety_issues:
    print("\nSAFETY ISSUES DETECTED:")
    for issue in safety_issues:
        print(f"- {issue}")
else:
    print("\nNo major safety issues detected in preliminary analysis.")
