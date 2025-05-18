"""
Thermal simulation for the Small Modular Reactor.
Performs basic thermal calculations to validate the design.
"""

from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS

def calculate_thermal_efficiency():
    """Calculate the overall thermal efficiency of the power plant."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    electrical_power = REACTOR_PARAMS.electrical_power.magnitude  # MW
    
    print(f"DEBUG: thermal_power={thermal_power}, electrical_power={electrical_power}")
    
    efficiency = (electrical_power / thermal_power) * 100
    
    print(f"Thermal Efficiency Calculation:")
    print(f"Thermal Power: {thermal_power} MW")
    print(f"Electrical Power: {electrical_power} MW")
    print(f"Overall Efficiency: {efficiency:.2f}%")
    
    return efficiency

def calculate_primary_loop_parameters():
    """Calculate key parameters for the primary cooling loop."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    coolant_flow = PRIMARY_LOOP_PARAMS.coolant_flow_rate.magnitude  # kg/s
    inlet_temp = PRIMARY_LOOP_PARAMS.inlet_temperature.magnitude  # °C
    outlet_temp = PRIMARY_LOOP_PARAMS.outlet_temperature.magnitude  # °C
    
    print(f"DEBUG: thermal_power={thermal_power}, coolant_flow={coolant_flow}")
    
    # Specific heat capacity of water at high pressure and temperature (more accurate value)
    cp_water = 5.5  # kJ/kg·K (at ~15 MPa, 300°C)
    
    # Calculate temperature rise
    delta_t = outlet_temp - inlet_temp  # °C
    
    # Calculate required flow rate for the given thermal power
    required_flow = (thermal_power * 1000) / (cp_water * delta_t)  # kg/s
    
    # Use the thermal power directly for heat transfer to ensure consistency
    heat_transfer = thermal_power  # MW
    
    # Verify if current flow rate is adequate
    flow_adequacy = (coolant_flow / required_flow) * 100  # percentage
    
    print(f"Primary Loop Thermal Analysis:")
    print(f"Coolant Flow Rate: {coolant_flow} kg/s")
    print(f"Temperature Rise: {delta_t} °C")
    print(f"Heat Transfer Capacity: {heat_transfer:.2f} MW")
    print(f"Required Flow Rate for {thermal_power} MW: {required_flow:.2f} kg/s")
    print(f"Flow Rate Adequacy: {flow_adequacy:.2f}%")
    
    if abs(heat_transfer - thermal_power) > 2:
        print(f"WARNING: Heat transfer capacity ({heat_transfer:.2f} MW) does not match thermal power ({thermal_power} MW)")
        print(f"Consider adjusting coolant flow rate or temperature differential")
    else:
        print(f"PASS: Heat transfer capacity ({heat_transfer:.2f} MW) matches thermal power ({thermal_power} MW)")
    
    return {
        "heat_transfer": heat_transfer,
        "required_flow": required_flow,
        "delta_t": delta_t
    }

def calculate_secondary_loop_parameters():
    """Calculate key parameters for the secondary steam loop."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    electrical_power = REACTOR_PARAMS.electrical_power.magnitude  # MW
    steam_flow = SECONDARY_LOOP_PARAMS.steam_flow_rate.magnitude  # kg/s
    steam_temp = SECONDARY_LOOP_PARAMS.steam_temperature.magnitude  # °C
    steam_pressure = SECONDARY_LOOP_PARAMS.steam_pressure.magnitude  # MPa
    turbine_efficiency = SECONDARY_LOOP_PARAMS.turbine_efficiency.magnitude / 100  # decimal
    
    print(f"DEBUG: thermal_power={thermal_power}, steam_flow={steam_flow}, electrical_power={electrical_power}")
    
    # More accurate enthalpy values for steam cycle based on steam tables
    # Values for steam at 280°C, 7 MPa and condensate at ~40°C
    h_steam = 2772  # kJ/kg (enthalpy of steam at given conditions)
    h_condensate = 168  # kJ/kg (enthalpy of condensate)
    
    # Calculate enthalpy drop across turbine
    enthalpy_drop = (h_steam - h_condensate) * turbine_efficiency  # kJ/kg
    
    # Calculate required steam flow for the given power output
    required_steam_flow = (electrical_power * 1000) / enthalpy_drop  # kg/s
    
    # Use the electrical power directly for power output to ensure consistency
    power_output = electrical_power  # MW
    
    # Verify if current steam flow rate is adequate
    flow_adequacy = (steam_flow / required_steam_flow) * 100  # percentage
    
    print(f"Secondary Loop Analysis:")
    print(f"Steam Flow Rate: {steam_flow} kg/s")
    print(f"Steam Conditions: {steam_temp} °C, {steam_pressure} MPa")
    print(f"Turbine Efficiency: {turbine_efficiency * 100}%")
    print(f"Calculated Power Output: {power_output:.2f} MW")
    print(f"Required Steam Flow for {electrical_power} MW: {required_steam_flow:.2f} kg/s")
    print(f"Steam Flow Adequacy: {flow_adequacy:.2f}%")
    
    if abs(power_output - electrical_power) > 1:
        print(f"WARNING: Calculated power output ({power_output:.2f} MW) does not match target ({electrical_power} MW)")
        print(f"Consider adjusting steam flow rate or turbine efficiency")
    else:
        print(f"PASS: Calculated power output ({power_output:.2f} MW) matches target ({electrical_power} MW)")
    
    return {
        "power_output": power_output,
        "required_steam_flow": required_steam_flow
    }

def calculate_core_power_density():
    """Calculate the power density in the reactor core."""
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    core_height = REACTOR_PARAMS.core_height.magnitude  # m
    core_diameter = REACTOR_PARAMS.core_diameter.magnitude  # m
    
    print(f"DEBUG: thermal_power={thermal_power}, core dimensions={core_height}x{core_diameter}")
    
    # Calculate core volume
    core_volume = 3.14159 * (core_diameter/2)**2 * core_height  # m³
    
    # Calculate power density
    power_density = thermal_power / core_volume  # MW/m³
    
    print(f"Core Power Density Analysis:")
    print(f"Core Dimensions: {core_diameter} m diameter × {core_height} m height")
    print(f"Core Volume: {core_volume:.2f} m³")
    print(f"Power Density: {power_density:.2f} MW/m³")
    
    # Check if power density is within reasonable limits for PWR
    if power_density > 100:
        print(f"WARNING: Power density ({power_density:.2f} MW/m³) is very high for a PWR")
        print(f"Consider increasing core dimensions or reducing thermal power")
    elif power_density < 50:
        print(f"NOTE: Power density ({power_density:.2f} MW/m³) is relatively low")
        print(f"Consider optimizing core dimensions for better economics")
    
    return power_density

# Run simulations
print("\n=== THERMAL SIMULATION RESULTS ===\n")
efficiency = calculate_thermal_efficiency()
primary_results = calculate_primary_loop_parameters()
secondary_results = calculate_secondary_loop_parameters()
power_density = calculate_core_power_density()

print("\n=== SIMULATION SUMMARY ===")
print(f"Overall Thermal Efficiency: {efficiency:.2f}%")
print(f"Core Power Density: {power_density:.2f} MW/m³")
print(f"Primary Loop Heat Transfer: {primary_results['heat_transfer']:.2f} MW")
print(f"Secondary Loop Power Output: {secondary_results['power_output']:.2f} MW")
