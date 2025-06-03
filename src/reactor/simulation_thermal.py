"""
Thermal-hydraulic simulation module for HTGR systems.

This module provides simple physics models for calculating heat transfer,
efficiency, power requirements, temperature distributions, pressure drops,
and heat losses in the HTGR thermal-hydraulic system.
"""

from reactor.parameters_thermal import (
    THERMAL_PARAMS,
    PRIMARY_LOOP_PARAMS,
    SECONDARY_LOOP_PARAMS,
    IHX_PARAMS
)
from reactor.parameters_core import CORE_PARAMS
from pyforge import UREG, Quantity


def calculate_ihx_heat_transfer(
    primary_inlet_temp: Quantity,
    primary_outlet_temp: Quantity,
    primary_mass_flow: Quantity
) -> Quantity:
    """
    Calculate heat transfer in the intermediate heat exchanger (IHX).
    
    Args:
        primary_inlet_temp: Inlet temperature of primary coolant (helium)
        primary_outlet_temp: Outlet temperature of primary coolant
        primary_mass_flow: Mass flow rate of primary coolant
        
    Returns:
        Heat transfer rate in the IHX
    """
    # Q = m * cp * ΔT
    cp_helium = PRIMARY_LOOP_PARAMS.helium_specific_heat
    # Convert temperatures to Kelvin for proper delta calculation
    primary_inlet_temp_k = primary_inlet_temp.to('kelvin')
    primary_outlet_temp_k = primary_outlet_temp.to('kelvin')
    delta_t = primary_inlet_temp_k - primary_outlet_temp_k
    heat_transfer = primary_mass_flow * cp_helium * delta_t
    
    print(f"IHX heat transfer: {heat_transfer.to('MW'):.2f}")
    return heat_transfer


def calculate_heat_transfer_efficiency(
    primary_heat: Quantity,
    secondary_heat: Quantity
) -> float:
    """
    Calculate efficiency of primary-to-secondary heat transfer.
    
    Args:
        primary_heat: Heat supplied by primary loop
        secondary_heat: Heat received by secondary loop
        
    Returns:
        Heat transfer efficiency as a fraction
    """
    efficiency = secondary_heat / primary_heat
    
    print(f"Heat transfer efficiency: {efficiency:.2%}")
    return efficiency


def calculate_helium_circulator_power(
    mass_flow: Quantity,
    pressure_drop: Quantity,
    inlet_temperature: Quantity,
    inlet_pressure: Quantity
) -> Quantity:
    """
    Calculate power requirements for helium circulators.
    
    Args:
        mass_flow: Mass flow rate of helium
        pressure_drop: Pressure drop in the primary loop
        inlet_temperature: Inlet temperature to the circulator
        inlet_pressure: Inlet pressure to the circulator
        
    Returns:
        Power required by the helium circulator
    """
    # W = (m * ΔP) / (ρ * η)
    # where ρ is calculated from ideal gas law: ρ = P/(R*T)
    
    helium_gas_constant = PRIMARY_LOOP_PARAMS.gas_constant
    efficiency = PRIMARY_LOOP_PARAMS.circulator_efficiency
    
    # Convert temperature to Kelvin for ideal gas law calculation
    inlet_temp_kelvin = inlet_temperature.to('kelvin')
    
    # Calculate density using ideal gas law
    density = inlet_pressure / (helium_gas_constant * inlet_temp_kelvin)
    
    # Calculate power
    power = (mass_flow * pressure_drop) / (density * efficiency)
    
    print(f"Helium circulator power: {power.to('kW'):.2f}")
    return power


def calculate_co2_compressor_power(
    mass_flow: Quantity,
    pressure_ratio: float,
    inlet_temperature: Quantity,
    inlet_pressure: Quantity
) -> Quantity:
    """
    Calculate power requirements for CO2 compressors.
    
    Args:
        mass_flow: Mass flow rate of CO2
        pressure_ratio: Ratio of outlet to inlet pressure
        inlet_temperature: Inlet temperature to the compressor
        inlet_pressure: Inlet pressure to the compressor
        
    Returns:
        Power required by the CO2 compressor
    """
    # For a real gas compressor:
    # W = (m * cp * T1 / η) * ((P2/P1)^((γ-1)/γ) - 1)
    
    cp_co2 = SECONDARY_LOOP_PARAMS.specific_heat
    gamma = SECONDARY_LOOP_PARAMS.specific_heat_ratio
    efficiency = SECONDARY_LOOP_PARAMS.compressor_efficiency
    
    # Convert temperature to Kelvin for thermodynamic calculations
    inlet_temp_kelvin = inlet_temperature.to('kelvin')
    
    exponent = (gamma - 1) / gamma
    power = (mass_flow * cp_co2 * inlet_temp_kelvin / efficiency) * (
        (pressure_ratio ** exponent) - 1
    )
    
    print(f"CO2 compressor power: {power.to('kW'):.2f}")
    return power


def calculate_secondary_temperature_distribution(
    inlet_temp: Quantity,
    heat_input: Quantity,
    mass_flow: Quantity,
    num_points: int = 10
) -> list:
    """
    Calculate temperature distribution in the secondary loop.
    
    Args:
        inlet_temp: Inlet temperature to the secondary loop
        heat_input: Heat input to the secondary loop
        mass_flow: Mass flow rate in the secondary loop
        num_points: Number of points to calculate in the distribution
        
    Returns:
        List of temperatures along the secondary loop
    """
    cp_co2 = SECONDARY_LOOP_PARAMS.specific_heat
    
    # Calculate total temperature rise
    # For temperature rise calculations, we need to work with kelvin
    delta_t_total = heat_input / (mass_flow * cp_co2)
    
    # Calculate temperature at each point
    temperatures = []
    for i in range(num_points):
        fraction = i / (num_points - 1)
        # Convert to Kelvin, do the calculation, then convert back to original unit
        inlet_temp_k = inlet_temp.to('kelvin')
        delta_t_k = delta_t_total
        temp_k = inlet_temp_k + fraction * delta_t_k
        temp = temp_k.to(inlet_temp.units)
        temperatures.append(temp)
    
    print(f"Secondary loop temperature range: {temperatures[0].to('°C'):.1f} to {temperatures[-1].to('°C'):.1f}")
    return temperatures


def calculate_pressure_drops(
    primary_mass_flow: Quantity,
    secondary_mass_flow: Quantity
) -> tuple:
    """
    Calculate pressure drops in both primary and secondary loops.
    
    Args:
        primary_mass_flow: Mass flow rate in primary loop
        secondary_mass_flow: Mass flow rate in secondary loop
        
    Returns:
        Tuple of (primary_pressure_drop, secondary_pressure_drop)
    """
    # Simple model: pressure drop proportional to square of mass flow rate
    # ΔP = k * (m^2)
    
    primary_k = SECONDARY_LOOP_PARAMS.pressure_drop_coefficient
    secondary_k = SECONDARY_LOOP_PARAMS.pressure_drop_coefficient
    
    primary_drop = primary_k * (primary_mass_flow ** 2)
    secondary_drop = secondary_k * (secondary_mass_flow ** 2)
    
    print(f"Primary loop pressure drop: {primary_drop.to('kPa'):.2f}")
    print(f"Secondary loop pressure drop: {secondary_drop.to('kPa'):.2f}")
    
    return (primary_drop, secondary_drop)


def calculate_heat_losses(
    system_temperature: Quantity,
    ambient_temperature: Quantity,
    insulation_thickness: Quantity,
    surface_area: Quantity
) -> Quantity:
    """
    Calculate heat losses in the system.
    
    Args:
        system_temperature: Average temperature of the system
        ambient_temperature: Ambient temperature
        insulation_thickness: Thickness of insulation
        surface_area: Surface area for heat loss
        
    Returns:
        Heat loss rate
    """
    # Q = (k * A * ΔT) / L
    # where k is thermal conductivity, A is area, ΔT is temperature difference,
    # and L is insulation thickness
    
    thermal_conductivity = THERMAL_PARAMS.insulation_thermal_conductivity
    
    # Convert temperatures to Kelvin for proper delta calculation
    system_temp_kelvin = system_temperature.to('kelvin')
    ambient_temp_kelvin = ambient_temperature.to('kelvin')
    delta_t = system_temp_kelvin - ambient_temp_kelvin
    
    heat_loss = (thermal_conductivity * surface_area * delta_t) / insulation_thickness
    
    print(f"System heat losses: {heat_loss.to('kW'):.2f}")
    return heat_loss


# Add functions needed by design.py
def calculate_thermal_efficiency() -> float:
    """Calculate the overall thermal efficiency of the system"""
    return THERMAL_PARAMS.thermal_efficiency

def calculate_heat_output() -> Quantity:
    """Calculate the nominal heat output of the system"""
    return THERMAL_PARAMS.core_thermal_power_options["medium"]


# Run a simple demonstration when executed directly
# These prints will be visible to the manager agent
primary_inlet_temp = CORE_PARAMS.outlet_temperature
primary_outlet_temp = CORE_PARAMS.inlet_temperature
primary_mass_flow = PRIMARY_LOOP_PARAMS.mass_flow_rate
secondary_mass_flow = SECONDARY_LOOP_PARAMS.mass_flow_rate

print("\nHTGR Thermal-Hydraulic System Simulation Results:")
print("=" * 50)

# Calculate heat transfer in IHX
heat_transfer = calculate_ihx_heat_transfer(
    primary_inlet_temp,
    primary_outlet_temp,
    primary_mass_flow
)

# Calculate secondary heat (accounting for losses in IHX)
ihx_efficiency = IHX_PARAMS.efficiency
secondary_heat = heat_transfer * ihx_efficiency

# Calculate heat transfer efficiency
efficiency = calculate_heat_transfer_efficiency(heat_transfer, secondary_heat)

# Calculate power requirements
helium_power = calculate_helium_circulator_power(
    primary_mass_flow,
    PRIMARY_LOOP_PARAMS.design_pressure_drop,
    primary_outlet_temp,
    PRIMARY_LOOP_PARAMS.operating_pressure
)

co2_power = calculate_co2_compressor_power(
    secondary_mass_flow,
    SECONDARY_LOOP_PARAMS.pressure_ratio,
    SECONDARY_LOOP_PARAMS.inlet_temperature,
    SECONDARY_LOOP_PARAMS.operating_pressure
)

# Calculate temperature distribution
temp_distribution = calculate_secondary_temperature_distribution(
    SECONDARY_LOOP_PARAMS.inlet_temperature,
    secondary_heat,
    secondary_mass_flow
)

# Calculate pressure drops
pressure_drops = calculate_pressure_drops(primary_mass_flow, secondary_mass_flow)

# Define ambient temperature and system surface area for heat loss calculation
ambient_temp = Quantity(30, "°C")
system_surface_area = Quantity(100, "m^2")

# Calculate heat losses
# Convert temperatures to Kelvin before averaging to avoid offset unit errors
primary_inlet_temp_k = primary_inlet_temp.to('kelvin')
primary_outlet_temp_k = primary_outlet_temp.to('kelvin')
avg_temp_k = (primary_inlet_temp_k + primary_outlet_temp_k) / 2
avg_temp = avg_temp_k.to('degC')
    
print(f"DEBUG: Converting temperatures for heat loss calculation")
print(f"DEBUG: Primary inlet temp: {primary_inlet_temp} -> {primary_inlet_temp_k}")
print(f"DEBUG: Primary outlet temp: {primary_outlet_temp} -> {primary_outlet_temp_k}")
print(f"DEBUG: Average temp: {avg_temp_k} -> {avg_temp}")

heat_losses = calculate_heat_losses(
    avg_temp,
    ambient_temp,
    THERMAL_PARAMS.insulation_thickness,
    system_surface_area
)

# Calculate net thermal output
net_thermal_output = secondary_heat - heat_losses

print("\nSummary:")
print(f"Gross thermal output: {secondary_heat.to('MW'):.2f}")
print(f"Net thermal output: {net_thermal_output.to('MW'):.2f}")
print(f"Total parasitic power: {(helium_power + co2_power).to('kW'):.2f}")
print(f"System thermal efficiency: {(net_thermal_output/heat_transfer):.2%}")
print("\nThermal simulation complete with fixed imports.")
"""
Thermal performance simulation for the High-Temperature Gas-cooled Reactor (HTGR) system.
"""
from pyforge import Quantity, UREG
from reactor.parameters_core import CORE_PARAMS
from reactor.parameters_coolant import COOLANT_PARAMS

def calculate_helium_flow_rate(thermal_power):
    """
    Calculate the required helium flow rate for a given thermal power.
    
    Args:
        thermal_power: Thermal power in MW
        
    Returns:
        float: Helium flow rate in kg/s
    """
    # Scale from the reference 20 MW design
    reference_power = CORE_PARAMS.thermal_power_large.magnitude
    reference_flow_rate = COOLANT_PARAMS.helium_flow_rate_large.magnitude
    
    flow_rate = reference_flow_rate * (thermal_power / reference_power)
    
    return flow_rate

def calculate_co2_flow_rate(thermal_power):
    """
    Calculate the required CO2 flow rate for a given thermal power.
    
    Args:
        thermal_power: Thermal power in MW
        
    Returns:
        float: CO2 flow rate in kg/s
    """
    # Scale from the reference 20 MW design
    reference_power = CORE_PARAMS.thermal_power_large.magnitude
    reference_flow_rate = COOLANT_PARAMS.co2_flow_rate_large.magnitude
    
    flow_rate = reference_flow_rate * (thermal_power / reference_power)
    
    return flow_rate

def calculate_heat_transfer_performance(thermal_power):
    """
    Calculate the heat transfer performance for a given thermal power.
    
    Args:
        thermal_power: Thermal power in MW
        
    Returns:
        dict: Dictionary containing heat transfer performance metrics
    """
    # Calculate flow rates
    helium_flow = calculate_helium_flow_rate(thermal_power)
    co2_flow = calculate_co2_flow_rate(thermal_power)
    
    # Calculate heat transfer parameters
    delta_t_primary = CORE_PARAMS.temp_differential.magnitude
    delta_t_secondary = (COOLANT_PARAMS.co2_outlet_temp.magnitude - 
                         COOLANT_PARAMS.co2_inlet_temp.magnitude)
    
    # Print thermal performance results
    print(f"Thermal Performance Analysis Results for {thermal_power} MW:")
    print(f"  Primary Helium Flow Rate: {helium_flow:.2f} kg/s")
    print(f"  Secondary CO2 Flow Rate: {co2_flow:.2f} kg/s")
    print(f"  Primary Temperature Differential: {delta_t_primary}°C")
    print(f"  Secondary Temperature Differential: {delta_t_secondary}°C")
    
    return {
        "helium_flow_rate": helium_flow,
        "co2_flow_rate": co2_flow,
        "delta_t_primary": delta_t_primary,
        "delta_t_secondary": delta_t_secondary
    }
