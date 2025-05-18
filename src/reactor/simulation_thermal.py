"""
Thermal-hydraulic calculations for the reactor system.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
import math

def compute_heat_exchanger_area() -> float:
    """
    Returns the approximate heat exchanger area (m²) needed.
    """
    # Using simplified U-LMTD method
    # Q = U * A * LMTD
    # Using a more realistic U value for primary-to-secondary heat exchangers
    U = 2500  # W/(m²·K) - typical for steam generators with water-to-steam phase change
    
    # Log mean temperature difference
    T_hot_in = THERMAL_PARAMS.primary_temp_hot.magnitude
    T_hot_out = THERMAL_PARAMS.primary_temp_cold.magnitude
    T_cold_in = THERMAL_PARAMS.secondary_temp_cold.magnitude
    T_cold_out = THERMAL_PARAMS.secondary_temp_hot.magnitude
    
    delta_T1 = T_hot_in - T_cold_out
    delta_T2 = T_hot_out - T_cold_in
    
    LMTD = (delta_T1 - delta_T2) / math.log(delta_T1 / delta_T2)
    
    # Heat transfer rate in W
    Q = REACTOR_PARAMS.thermal_power.magnitude * 1e6
    
    # Area calculation
    area = Q / (U * LMTD)
    
    # Add 10% margin for fouling and manufacturing tolerances
    area *= 1.1
    
    return area

def compute_pump_power() -> float:
    """
    Returns the approximate pump power (kW) needed for the primary loop.
    """
    # Using simplified pump power equation
    # P = Q * ΔP / η
    flow_rate = THERMAL_PARAMS.primary_flow_rate.magnitude  # kg/s
    density = 750  # kg/m³ (approximate for hot pressurized water)
    volumetric_flow = flow_rate / density  # m³/s
    
    # Pressure drop estimation (simplified)
    pressure_drop = 0.5e6  # Pa (0.5 MPa)
    
    # Pump efficiency
    efficiency = 0.75
    
    # Power calculation
    power = volumetric_flow * pressure_drop / efficiency
    return power / 1000  # Convert W to kW

def compute_turbine_power() -> float:
    """
    Returns the turbine power output (MW).
    """
    # Using simplified turbine power equation
    # P = m * Δh * η
    steam_flow = compute_steam_flow()
    
    # Enthalpy drop estimation (simplified)
    # Assuming isentropic enthalpy drop of 800 kJ/kg
    enthalpy_drop = 800 * 1000  # J/kg
    
    # Turbine efficiency
    efficiency = THERMAL_PARAMS.turbine_efficiency
    
    # Power calculation
    power = steam_flow * enthalpy_drop * efficiency
    return power / 1e6  # Convert W to MW

def compute_steam_flow() -> float:
    """
    Returns the steam flow rate (kg/s) in the secondary loop.
    """
    # Assuming latent heat of vaporization = 1800 kJ/kg at secondary pressure
    latent_heat = 1800 * 1000  # J/kg
    power_watts = REACTOR_PARAMS.thermal_power.magnitude * 1e6 * 0.97  # 97% heat transfer efficiency
    steam_flow = power_watts / latent_heat
    return steam_flow

# Debug print to verify module loading
print("simulation_thermal module loaded and functions defined")

# Add debug print
print(f"Simulation thermal module loaded successfully")

# Run simulations
heat_exchanger_area = compute_heat_exchanger_area()
pump_power = compute_pump_power()
turbine_power = compute_turbine_power()
steam_flow = compute_steam_flow()

print(f"Required heat exchanger area: {heat_exchanger_area:.2f} m²")
print(f"Primary pump power requirement: {pump_power:.2f} kW")
print(f"Turbine power output: {turbine_power:.2f} MW")
print(f"Steam flow rate: {steam_flow:.2f} kg/s")
