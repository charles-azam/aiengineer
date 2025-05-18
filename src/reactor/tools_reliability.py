"""
Reliability analysis tools for the small modular reactor.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
import numpy as np
import math

def calculate_system_reliability(component_reliabilities, system_type="series"):
    """
    Calculate system reliability based on component reliabilities.
    
    Args:
        component_reliabilities: List of component reliabilities (0-1)
        system_type: "series", "parallel", or "k-out-of-n"
        
    Returns:
        System reliability (0-1)
    """
    if system_type == "series":
        # All components must work
        return np.prod(component_reliabilities)
    
    elif system_type == "parallel":
        # At least one component must work
        return 1 - np.prod([1 - r for r in component_reliabilities])
    
    elif isinstance(system_type, tuple) and len(system_type) == 2:
        # k-out-of-n system
        k, n = system_type
        if k > n or k < 1:
            raise ValueError("Invalid k-out-of-n parameters")
        
        # Calculate using binomial probability
        reliability = 0
        for i in range(k, n + 1):
            reliability += math.comb(n, i) * np.prod(component_reliabilities)**i * \
                          (1 - np.prod(component_reliabilities))**(n - i)
        return reliability
    
    else:
        raise ValueError("Invalid system type")

def calculate_mtbf(failure_rate):
    """
    Calculate Mean Time Between Failures (MTBF) from failure rate.
    
    Args:
        failure_rate: Failure rate in failures per hour
        
    Returns:
        MTBF in hours
    """
    if failure_rate <= 0:
        return float('inf')
    return 1 / failure_rate

def calculate_availability(mtbf, mttr):
    """
    Calculate availability from MTBF and MTTR.
    
    Args:
        mtbf: Mean Time Between Failures in hours
        mttr: Mean Time To Repair in hours
        
    Returns:
        Availability (0-1)
    """
    return mtbf / (mtbf + mttr)

def calculate_safety_system_reliability():
    """
    Calculate reliability metrics for key safety systems.
    
    Returns:
        Dictionary with reliability metrics for safety systems
    """
    # Safety system redundancy
    redundancy = SAFETY_PARAMS.safety_train_redundancy
    
    # Component failure rates (failures per demand)
    component_failure_rates = {
        "ECCS Valve": 1e-3,
        "ECCS Pump": 2e-3,
        "Diesel Generator": 5e-3,
        "Battery System": 1e-4,
        "Instrumentation": 5e-4,
        "Control Logic": 2e-4
    }
    
    # Calculate system failure probabilities
    # For N+2 redundancy, we need at least 1 out of N+2 to work
    # So failure requires all N+2 to fail
    system_failure_probs = {}
    for component, failure_rate in component_failure_rates.items():
        # Apply common cause factor (beta model)
        beta = 0.1  # Common cause factor
        independent_failure_prob = failure_rate**redundancy
        common_cause_failure_prob = beta * failure_rate
        system_failure_probs[component] = independent_failure_prob + common_cause_failure_prob
    
    # Calculate system reliabilities
    system_reliabilities = {component: 1 - failure_prob 
                           for component, failure_prob in system_failure_probs.items()}
    
    # Calculate overall safety system reliability
    # Assuming series configuration of different systems
    overall_reliability = np.prod(list(system_reliabilities.values()))
    
    # Calculate probability of core damage (simplified)
    initiating_event_frequency = 1e-3  # per reactor-year
    conditional_core_damage_prob = 1 - overall_reliability
    core_damage_frequency = initiating_event_frequency * conditional_core_damage_prob
    
    return {
        "system_reliabilities": system_reliabilities,
        "overall_safety_system_reliability": overall_reliability,
        "core_damage_frequency": core_damage_frequency
    }

def calculate_component_lifetime(design_life, safety_factor, operating_conditions):
    """
    Calculate expected component lifetime based on design parameters.
    
    Args:
        design_life: Design life in years
        safety_factor: Safety factor applied to design
        operating_conditions: Dictionary with operating condition factors
        
    Returns:
        Expected lifetime in years
    """
    # Base lifetime
    base_lifetime = design_life * safety_factor
    
    # Apply operating condition factors
    condition_factor = 1.0
    for condition, factor in operating_conditions.items():
        condition_factor *= factor
    
    expected_lifetime = base_lifetime * condition_factor
    
    return expected_lifetime

# Run reliability analysis
safety_reliability = calculate_safety_system_reliability()

# Calculate reliability for key components
reactor_vessel_conditions = {
    "temperature": 0.9,  # Operating below max temperature
    "pressure_cycles": 0.85,  # Effect of pressure cycles
    "radiation": 0.95,  # Effect of radiation
    "water_chemistry": 0.98  # Effect of water chemistry
}

vessel_lifetime = calculate_component_lifetime(
    design_life=REACTOR_PARAMS.design_life,
    safety_factor=1.5,
    operating_conditions=reactor_vessel_conditions
)

# Calculate system availability
eccs_mtbf = calculate_mtbf(1e-5)  # failures/hour
eccs_mttr = 24  # hours
eccs_availability = calculate_availability(eccs_mtbf, eccs_mttr)

print(f"Overall safety system reliability: {safety_reliability['overall_safety_system_reliability']:.6f}")
print(f"Core damage frequency: {safety_reliability['core_damage_frequency']:.2e} per reactor-year")
print(f"Expected reactor vessel lifetime: {vessel_lifetime:.1f} years")
print(f"ECCS availability: {eccs_availability:.6f}")
