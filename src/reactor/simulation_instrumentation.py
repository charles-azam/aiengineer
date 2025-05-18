"""
Simulation of instrumentation and control systems for the small modular reactor.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
import numpy as np
import math

def calculate_instrument_uncertainty(sensor_accuracy, calibration_error, drift, environmental_effect):
    """
    Calculate total instrument uncertainty using square root of sum of squares method.
    
    Args:
        sensor_accuracy: Base accuracy of the sensor (% of span)
        calibration_error: Error introduced during calibration (% of span)
        drift: Drift over calibration interval (% of span)
        environmental_effect: Error due to environmental conditions (% of span)
        
    Returns:
        Total uncertainty (% of span)
    """
    total_uncertainty = math.sqrt(sensor_accuracy**2 + calibration_error**2 + 
                                 drift**2 + environmental_effect**2)
    return total_uncertainty

def calculate_response_time(sensor_time_constant, signal_processing_time, logic_execution_time):
    """
    Calculate total response time for an instrumentation channel.
    
    Args:
        sensor_time_constant: Time constant of the sensor (seconds)
        signal_processing_time: Time for signal processing (seconds)
        logic_execution_time: Time for logic execution (seconds)
        
    Returns:
        Total response time (seconds)
    """
    # Using 3 time constants for 95% response
    sensor_response_time = 3 * sensor_time_constant
    total_response_time = sensor_response_time + signal_processing_time + logic_execution_time
    return total_response_time

def calculate_protection_system_reliability(component_failure_rates, redundancy_level, diagnostic_coverage):
    """
    Calculate reliability metrics for protection system.
    
    Args:
        component_failure_rates: Dictionary of component failure rates (failures/hour)
        redundancy_level: Level of redundancy (e.g., 2 for 2-out-of-3)
        diagnostic_coverage: Fraction of failures detected by diagnostics (0-1)
        
    Returns:
        Dictionary with reliability metrics
    """
    # Calculate system failure rate using simplified beta-factor model
    beta_factor = 0.1  # Common cause failure factor
    
    # Sum of individual component failure rates
    system_failure_rate = sum(component_failure_rates.values())
    
    # Apply redundancy benefit (simplified calculation)
    redundant_failure_rate = system_failure_rate**redundancy_level
    
    # Apply common cause factor
    common_cause_rate = beta_factor * system_failure_rate
    
    # Total failure rate
    total_failure_rate = redundant_failure_rate + common_cause_rate
    
    # Apply diagnostic coverage benefit
    undetected_failure_rate = total_failure_rate * (1 - diagnostic_coverage)
    
    # Calculate metrics
    mtbf = 1 / total_failure_rate if total_failure_rate > 0 else float('inf')
    availability = 1 - (undetected_failure_rate * 24)  # Assuming 24-hour repair time for undetected failures
    
    return {
        "total_failure_rate": total_failure_rate,
        "undetected_failure_rate": undetected_failure_rate,
        "mtbf_hours": mtbf,
        "availability": availability
    }

def simulate_control_system_response(setpoint, disturbance_magnitude, controller_gain, time_constant):
    """
    Simulate simplified control system response to a disturbance.
    
    Args:
        setpoint: Desired process value
        disturbance_magnitude: Magnitude of the disturbance
        controller_gain: Proportional controller gain
        time_constant: Process time constant (seconds)
        
    Returns:
        Dictionary with response metrics
    """
    # Simplified first-order response simulation
    time_steps = 100
    time_vector = np.linspace(0, 5 * time_constant, time_steps)
    response = np.zeros(time_steps)
    
    # Initial condition after disturbance
    response[0] = setpoint + disturbance_magnitude
    
    # Simulate response
    for i in range(1, time_steps):
        dt = time_vector[i] - time_vector[i-1]
        error = setpoint - response[i-1]
        control_action = controller_gain * error
        derivative = (control_action - response[i-1]) / time_constant
        response[i] = response[i-1] + derivative * dt
    
    # Calculate metrics
    settling_time = 0
    for i in range(time_steps):
        if abs(response[i] - setpoint) < 0.05 * abs(disturbance_magnitude):
            settling_time = time_vector[i]
            break
    
    overshoot = max(0, max(response) - setpoint) / abs(disturbance_magnitude) * 100
    
    return {
        "settling_time": settling_time,
        "overshoot_percent": overshoot,
        "steady_state_error": abs(response[-1] - setpoint)
    }

# Example calculations
# Temperature sensor uncertainty
temp_uncertainty = calculate_instrument_uncertainty(0.25, 0.1, 0.15, 0.2)
print(f"Temperature measurement uncertainty: ±{temp_uncertainty:.2f}% of span")

# Pressure sensor uncertainty
pressure_uncertainty = calculate_instrument_uncertainty(0.1, 0.05, 0.1, 0.15)
print(f"Pressure measurement uncertainty: ±{pressure_uncertainty:.2f}% of span")

# Response time for SCRAM signal
scram_response = calculate_response_time(0.1, 0.02, 0.03)
print(f"SCRAM signal response time: {scram_response*1000:.1f} ms")

# Protection system reliability
component_failures = {
    "sensor": 1e-6,
    "signal_processor": 5e-7,
    "logic_solver": 2e-7,
    "output_module": 3e-7
}
reliability = calculate_protection_system_reliability(component_failures, 2, 0.95)
print(f"Protection system MTBF: {reliability['mtbf_hours']:.1f} hours")
print(f"Protection system availability: {reliability['availability']*100:.6f}%")

# Control system response simulation
controller_response = simulate_control_system_response(
    setpoint=THERMAL_PARAMS.primary_pressure.magnitude,
    disturbance_magnitude=-0.5,  # 0.5 MPa pressure drop
    controller_gain=2.0,
    time_constant=5.0  # seconds
)
print(f"Pressure control settling time: {controller_response['settling_time']:.2f} seconds")
print(f"Pressure control overshoot: {controller_response['overshoot_percent']:.2f}%")
