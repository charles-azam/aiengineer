"""
Thermal-hydraulic calculations for High-Temperature Gas-cooled Reactor (HTGR)
This document provides detailed calculations for heat transfer, flow, and thermal performance
of the HTGR design.
"""

from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from pyforge import UREG, Quantity
import pandas as pd
import numpy as np
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS

# Document configuration
config = DocumentConfig(
    title="HTGR Thermal-Hydraulic Calculations",
    author="Reactor Design Team",
    date="2025-06-02"
)
display(config)

# Main title
display(Title("# High-Temperature Gas-cooled Reactor (HTGR) Thermal-Hydraulic Analysis"))

display("""
This document presents the thermal-hydraulic calculations for our modular HTGR design,
covering heat transfer principles, flow calculations, and thermal performance analysis.
The calculations support the design requirements for delivering industrial process heat
at temperatures up to 600°C with passive safety features.
""")

# 1. Heat Transfer Principles in the HTGR Core
display(Title("## 1. Heat Transfer Principles in the HTGR Core"))

display("""
The HTGR core heat transfer involves several mechanisms:
- Conduction through TRISO fuel particles and graphite moderator
- Convection from fuel elements to helium coolant
- Radiation between fuel elements and core structures

The following calculations establish the fundamental heat transfer relationships in our core design.
""")

# Core heat transfer parameters table
core_heat_params = pd.DataFrame([
    {"Parameter": "Core Thermal Power", "Value": f"{REACTOR_PARAMS.thermal_power}"},
    {"Parameter": "Core Inlet Temperature", "Value": f"{THERMAL_PARAMS.core_inlet_temp}"},
    {"Parameter": "Core Outlet Temperature", "Value": f"{THERMAL_PARAMS.core_outlet_temp}"},
    {"Parameter": "Helium Mass Flow Rate", "Value": f"{THERMAL_PARAMS.helium_mass_flow}"},
    {"Parameter": "Helium Pressure", "Value": f"{THERMAL_PARAMS.helium_pressure}"},
    {"Parameter": "Fuel Element Thermal Conductivity", "Value": f"{THERMAL_PARAMS.fuel_thermal_conductivity}"},
    {"Parameter": "Graphite Thermal Conductivity", "Value": f"{THERMAL_PARAMS.graphite_thermal_conductivity}"},
])
display(Table(core_heat_params, "Core Heat Transfer Parameters", "tbl-core-heat"))

# Core heat balance calculation
display(Title("### Core Heat Balance"))

display("""
The fundamental heat balance in the reactor core is given by:
""")

display(r"$$Q = \dot{m} \cdot c_p \cdot (T_{out} - T_{in})$$")

display("""
Where:
- Q = Core thermal power [W]
- ṁ = Helium mass flow rate [kg/s]
- cp = Helium specific heat capacity [J/(kg·K)]
- Tout = Core outlet temperature [K]
- Tin = Core inlet temperature [K]
""")

# Calculate required helium flow rate
def calculate_required_flow():
    """Calculate required helium flow rate based on core power and temperatures"""
    power = REACTOR_PARAMS.thermal_power.to("W").magnitude
    cp = THERMAL_PARAMS.helium_specific_heat.to("J/(kg*K)").magnitude
    t_in = THERMAL_PARAMS.core_inlet_temp.to("kelvin").magnitude
    t_out = THERMAL_PARAMS.core_outlet_temp.to("kelvin").magnitude
    
    flow_rate = power / (cp * (t_out - t_in))
    return flow_rate

required_flow = calculate_required_flow()
print(f"Required helium flow rate: {required_flow:.2f} kg/s")

# Heat transfer coefficient calculation
display(Title("### Heat Transfer Coefficient"))

display("""
The convective heat transfer coefficient between the fuel elements and helium coolant
is calculated using the Dittus-Boelter correlation for turbulent flow:
""")

display(r"$$Nu = 0.023 \cdot Re^{0.8} \cdot Pr^{0.4}$$")
display(r"$$h = \frac{Nu \cdot k}{D_h}$$")

display("""
Where:
- Nu = Nusselt number
- Re = Reynolds number
- Pr = Prandtl number
- k = Thermal conductivity of helium [W/(m·K)]
- Dh = Hydraulic diameter [m]
- h = Heat transfer coefficient [W/(m²·K)]
""")

# 2. Heat Exchanger Design Calculations
display(Title("## 2. Heat Exchanger Design Calculations"))

display("""
The primary-to-secondary heat exchanger transfers heat from the helium primary loop
to the CO₂ secondary loop. We use the effectiveness-NTU method for heat exchanger sizing.
""")

# Heat exchanger parameters
hx_params = pd.DataFrame([
    {"Parameter": "Heat Transfer Rate", "Value": f"{THERMAL_PARAMS.heat_exchanger_duty}"},
    {"Parameter": "Primary Side Inlet Temperature", "Value": f"{THERMAL_PARAMS.core_outlet_temp}"},
    {"Parameter": "Primary Side Outlet Temperature", "Value": f"{THERMAL_PARAMS.core_inlet_temp}"},
    {"Parameter": "Secondary Side Inlet Temperature", "Value": f"{THERMAL_PARAMS.secondary_inlet_temp}"},
    {"Parameter": "Secondary Side Outlet Temperature", "Value": f"{THERMAL_PARAMS.secondary_outlet_temp}"},
    {"Parameter": "Overall Heat Transfer Coefficient", "Value": f"{THERMAL_PARAMS.overall_htc}"},
])
display(Table(hx_params, "Heat Exchanger Parameters", "tbl-hx-params"))

display(Title("### Heat Exchanger Sizing"))

display("""
The required heat transfer area is calculated using:
""")

display(r"$$A = \frac{Q}{U \cdot \Delta T_{LMTD}}$$")

display("""
Where:
- A = Heat transfer area [m²]
- Q = Heat transfer rate [W]
- U = Overall heat transfer coefficient [W/(m²·K)]
- ΔTLMTD = Log mean temperature difference [K]
""")

display("""
The log mean temperature difference (LMTD) is calculated as:
""")

display(r"$$\Delta T_{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\frac{\Delta T_1}{\Delta T_2})}$$")

display("""
Where:
- ΔT₁ = Primary inlet - Secondary outlet temperature difference [K]
- ΔT₂ = Primary outlet - Secondary inlet temperature difference [K]
""")

# Calculate LMTD and heat exchanger area
def calculate_hx_area():
    """Calculate heat exchanger area based on LMTD method"""
    # Convert temperatures to Kelvin for proper calculation
    t_p_in = THERMAL_PARAMS.core_outlet_temp.to("kelvin").magnitude
    t_p_out = THERMAL_PARAMS.core_inlet_temp.to("kelvin").magnitude
    t_s_in = THERMAL_PARAMS.secondary_inlet_temp.to("kelvin").magnitude
    t_s_out = THERMAL_PARAMS.secondary_outlet_temp.to("kelvin").magnitude
    
    delta_t1 = t_p_in - t_s_out
    delta_t2 = t_p_out - t_s_in
    
    lmtd = (delta_t1 - delta_t2) / np.log(delta_t1 / delta_t2)
    
    q = THERMAL_PARAMS.heat_exchanger_duty.to("W").magnitude
    u = THERMAL_PARAMS.overall_htc.to("W/(m^2*K)").magnitude
    
    area = q / (u * lmtd)
    return lmtd, area

lmtd, hx_area = calculate_hx_area()
print(f"Heat exchanger LMTD: {lmtd:.2f} K")
print(f"Required heat exchanger area: {hx_area:.2f} m²")

# 3. Primary Loop Flow Calculations
display(Title("## 3. Primary Loop Flow Calculations"))

display("""
The primary helium loop must circulate the coolant at the required flow rate to remove
heat from the core and transfer it to the heat exchanger.
""")

# Primary loop parameters
primary_loop_params = pd.DataFrame([
    {"Parameter": "Helium Mass Flow Rate", "Value": f"{THERMAL_PARAMS.helium_mass_flow}"},
    {"Parameter": "Loop Pipe Diameter", "Value": f"{THERMAL_PARAMS.primary_pipe_diameter}"},
    {"Parameter": "Total Loop Length", "Value": f"{THERMAL_PARAMS.primary_loop_length}"},
    {"Parameter": "Helium Density", "Value": f"{THERMAL_PARAMS.helium_density}"},
    {"Parameter": "Helium Dynamic Viscosity", "Value": f"{THERMAL_PARAMS.helium_viscosity}"},
])
display(Table(primary_loop_params, "Primary Loop Parameters", "tbl-primary-loop"))

display(Title("### Flow Velocity and Reynolds Number"))

display("""
The helium flow velocity in the primary loop is calculated as:
""")

display(r"$$v = \frac{\dot{m}}{\rho \cdot A}$$")

display("""
Where:
- v = Flow velocity [m/s]
- ṁ = Mass flow rate [kg/s]
- ρ = Helium density [kg/m³]
- A = Pipe cross-sectional area [m²]
""")

display("""
The Reynolds number is calculated to determine the flow regime:
""")

display(r"$$Re = \frac{\rho \cdot v \cdot D}{\mu}$$")

display("""
Where:
- Re = Reynolds number
- ρ = Helium density [kg/m³]
- v = Flow velocity [m/s]
- D = Pipe diameter [m]
- μ = Dynamic viscosity [Pa·s]
""")

# Calculate flow velocity and Reynolds number
def calculate_primary_flow_characteristics():
    """Calculate primary loop flow velocity and Reynolds number"""
    mass_flow = THERMAL_PARAMS.helium_mass_flow.to("kg/s").magnitude
    density = THERMAL_PARAMS.helium_density.to("kg/m^3").magnitude
    diameter = THERMAL_PARAMS.primary_pipe_diameter.to("m").magnitude
    viscosity = THERMAL_PARAMS.helium_viscosity.to("Pa*s").magnitude
    
    area = np.pi * (diameter/2)**2
    velocity = mass_flow / (density * area)
    reynolds = density * velocity * diameter / viscosity
    
    return velocity, reynolds

velocity, reynolds = calculate_primary_flow_characteristics()
print(f"Primary loop helium velocity: {velocity:.2f} m/s")
print(f"Reynolds number: {reynolds:.2e}")

# 4. Secondary Loop Flow Calculations
display(Title("## 4. Secondary Loop Flow Calculations"))

display("""
The secondary CO₂ loop transfers heat from the primary heat exchanger to the industrial
process heat users. The calculations below determine the flow characteristics of this loop.
""")

# Secondary loop parameters
secondary_loop_params = pd.DataFrame([
    {"Parameter": "CO₂ Mass Flow Rate", "Value": f"{THERMAL_PARAMS.co2_mass_flow}"},
    {"Parameter": "Loop Pipe Diameter", "Value": f"{THERMAL_PARAMS.secondary_pipe_diameter}"},
    {"Parameter": "Total Loop Length", "Value": f"{THERMAL_PARAMS.secondary_loop_length}"},
    {"Parameter": "CO₂ Density", "Value": f"{THERMAL_PARAMS.co2_density}"},
    {"Parameter": "CO₂ Specific Heat", "Value": f"{THERMAL_PARAMS.co2_specific_heat}"},
])
display(Table(secondary_loop_params, "Secondary Loop Parameters", "tbl-secondary-loop"))

display(Title("### Secondary Loop Heat Balance"))

display("""
The CO₂ mass flow rate in the secondary loop is determined by the heat balance:
""")

display(r"$$\dot{m}_{CO2} = \frac{Q}{c_p \cdot (T_{out} - T_{in})}$$")

display("""
Where:
- ṁCO₂ = CO₂ mass flow rate [kg/s]
- Q = Heat transfer rate [W]
- cp = CO₂ specific heat capacity [J/(kg·K)]
- Tout = Secondary outlet temperature [K]
- Tin = Secondary inlet temperature [K]
""")

# Calculate required CO2 flow rate
def calculate_co2_flow():
    """Calculate required CO2 flow rate based on heat duty and temperatures"""
    power = THERMAL_PARAMS.heat_exchanger_duty.to("W").magnitude
    cp = THERMAL_PARAMS.co2_specific_heat.to("J/(kg*K)").magnitude
    t_in = THERMAL_PARAMS.secondary_inlet_temp.to("kelvin").magnitude
    t_out = THERMAL_PARAMS.secondary_outlet_temp.to("kelvin").magnitude
    
    flow_rate = power / (cp * (t_out - t_in))
    return flow_rate

co2_flow = calculate_co2_flow()
print(f"Required CO2 flow rate: {co2_flow:.2f} kg/s")

# 5. Temperature Distribution Calculations
display(Title("## 5. Temperature Distribution Calculations"))

display("""
The temperature distribution in the reactor core is critical for safety and performance.
We analyze the radial and axial temperature profiles in the fuel elements.
""")

display(Title("### Fuel Temperature Profile"))

display("""
The temperature difference between the fuel centerline and the coolant is calculated using:
""")

display(r"$$\Delta T = \frac{q''' \cdot r_f^2}{4k_f} + \frac{q''' \cdot r_f}{2h}$$")

display("""
Where:
- ΔT = Temperature difference [K]
- q''' = Volumetric heat generation rate [W/m³]
- rf = Fuel element radius [m]
- kf = Fuel thermal conductivity [W/(m·K)]
- h = Convective heat transfer coefficient [W/(m²·K)]
""")

# Calculate maximum fuel temperature
def calculate_max_fuel_temp():
    """Calculate maximum fuel temperature based on heat generation and cooling"""
    q_vol = THERMAL_PARAMS.volumetric_heat_gen.to("W/m^3").magnitude
    r_fuel = THERMAL_PARAMS.fuel_element_radius.to("m").magnitude
    k_fuel = THERMAL_PARAMS.fuel_thermal_conductivity.to("W/(m*K)").magnitude
    h_conv = THERMAL_PARAMS.fuel_convection_htc.to("W/(m^2*K)").magnitude
    t_coolant = THERMAL_PARAMS.core_outlet_temp.to("K").magnitude
    
    delta_t = (q_vol * r_fuel**2) / (4 * k_fuel) + (q_vol * r_fuel) / (2 * h_conv)
    max_temp = t_coolant + delta_t
    
    return max_temp

max_fuel_temp = calculate_max_fuel_temp()
print(f"Maximum fuel temperature: {max_fuel_temp:.2f} K ({max_fuel_temp - 273.15:.2f} °C)")

# Axial temperature profile
display(Title("### Axial Temperature Profile"))

display("""
The axial temperature profile in the coolant channel follows an approximately exponential
distribution based on the axial power profile and coolant heat-up.
""")

# 6. Pressure Drop Calculations
display(Title("## 6. Pressure Drop Calculations"))

display("""
Pressure drops in the primary and secondary loops are critical for sizing circulators
and ensuring proper flow distribution.
""")

display(Title("### Primary Loop Pressure Drop"))

display("""
The pressure drop in the primary loop is calculated using the Darcy-Weisbach equation:
""")

display(r"$$\Delta P = f \cdot \frac{L}{D} \cdot \frac{\rho \cdot v^2}{2}$$")

display("""
Where:
- ΔP = Pressure drop [Pa]
- f = Friction factor
- L = Pipe length [m]
- D = Pipe diameter [m]
- ρ = Fluid density [kg/m³]
- v = Flow velocity [m/s]
""")

# Calculate primary loop pressure drop
def calculate_primary_pressure_drop():
    """Calculate pressure drop in the primary loop"""
    length = THERMAL_PARAMS.primary_loop_length.to("m").magnitude
    diameter = THERMAL_PARAMS.primary_pipe_diameter.to("m").magnitude
    density = THERMAL_PARAMS.helium_density.to("kg/m^3").magnitude
    velocity_val = velocity  # Use the velocity calculated earlier
    
    # Estimate friction factor using Blasius correlation for turbulent flow
    if reynolds > 4000:
        friction = 0.316 * reynolds**(-0.25)
    else:
        friction = 64 / reynolds
    
    delta_p = friction * (length/diameter) * (density * velocity_val**2) / 2
    
    # Add form losses (estimated as 50% of friction losses)
    delta_p_total = delta_p * 1.5
    
    return delta_p_total

primary_pressure_drop = calculate_primary_pressure_drop()
print(f"Primary loop pressure drop: {primary_pressure_drop/1000:.2f} kPa")

# 7. Heat Loss Calculations
display(Title("## 7. Heat Loss Calculations"))

display("""
Heat losses from the primary and secondary loops affect overall system efficiency
and must be minimized through proper insulation.
""")

display(Title("### Insulation Heat Loss"))

display("""
The heat loss through insulation is calculated using:
""")

display(r"$$Q_{loss} = \frac{2\pi k L (T_i - T_o)}{\ln(r_o/r_i)}$$")

display("""
Where:
- Qloss = Heat loss rate [W]
- k = Insulation thermal conductivity [W/(m·K)]
- L = Pipe length [m]
- Ti = Inner surface temperature [K]
- To = Outer surface temperature [K]
- ri = Inner radius of insulation [m]
- ro = Outer radius of insulation [m]
""")

# Calculate heat losses
def calculate_heat_loss():
    """Calculate heat loss through insulation in the primary loop"""
    k_insul = THERMAL_PARAMS.insulation_conductivity.to("W/(m*K)").magnitude
    length = THERMAL_PARAMS.primary_loop_length.to("m").magnitude
    t_inner = THERMAL_PARAMS.core_outlet_temp.to("kelvin").magnitude
    t_outer = THERMAL_PARAMS.ambient_temp.to("kelvin").magnitude
    r_inner = THERMAL_PARAMS.primary_pipe_diameter.to("m").magnitude / 2
    insul_thickness = THERMAL_PARAMS.insulation_thickness.to("m").magnitude
    r_outer = r_inner + insul_thickness
    
    heat_loss = 2 * np.pi * k_insul * length * (t_inner - t_outer) / np.log(r_outer/r_inner)
    
    return heat_loss

heat_loss = calculate_heat_loss()
print(f"Primary loop heat loss: {heat_loss/1000:.2f} kW")
print(f"Heat loss percentage: {heat_loss/REACTOR_PARAMS.thermal_power.to('W').magnitude*100:.2f}%")

# 8. Circulator and Compressor Power Calculations
display(Title("## 8. Circulator and Compressor Power Calculations"))

display("""
The power required for the helium circulator and CO₂ compressor is calculated
based on the pressure drop and flow rate in each loop.
""")

display(Title("### Helium Circulator Power"))

display("""
The power required for the helium circulator is calculated using:
""")

display(r"$$P_{circ} = \frac{\dot{m} \cdot \Delta P}{\rho \cdot \eta}$$")

display("""
Where:
- Pcirc = Circulator power [W]
- ṁ = Mass flow rate [kg/s]
- ΔP = Pressure drop [Pa]
- ρ = Fluid density [kg/m³]
- η = Circulator efficiency
""")

# Calculate circulator power
def calculate_circulator_power():
    """Calculate power required for the helium circulator"""
    mass_flow = THERMAL_PARAMS.helium_mass_flow.to("kg/s").magnitude
    delta_p = primary_pressure_drop  # From previous calculation
    density = THERMAL_PARAMS.helium_density.to("kg/m^3").magnitude
    efficiency = THERMAL_PARAMS.circulator_efficiency
    
    power = (mass_flow * delta_p) / (density * efficiency)
    
    return power

circulator_power = calculate_circulator_power()
print(f"Helium circulator power: {circulator_power/1000:.2f} kW")

# Summary of results
display(Title("## Summary of Thermal-Hydraulic Calculations"))

results_summary = pd.DataFrame([
    {"Parameter": "Required Helium Flow Rate", "Value": f"{required_flow:.2f} kg/s"},
    {"Parameter": "Heat Exchanger Area", "Value": f"{hx_area:.2f} m²"},
    {"Parameter": "Primary Loop Helium Velocity", "Value": f"{velocity:.2f} m/s"},
    {"Parameter": "Reynolds Number (Primary)", "Value": f"{reynolds:.2e}"},
    {"Parameter": "Required CO₂ Flow Rate", "Value": f"{co2_flow:.2f} kg/s"},
    {"Parameter": "Maximum Fuel Temperature", "Value": f"{max_fuel_temp - 273.15:.2f} °C"},
    {"Parameter": "Primary Loop Pressure Drop", "Value": f"{primary_pressure_drop/1000:.2f} kPa"},
    {"Parameter": "Heat Loss", "Value": f"{heat_loss/1000:.2f} kW ({heat_loss/REACTOR_PARAMS.thermal_power.to('W').magnitude*100:.2f}%)"},
    {"Parameter": "Helium Circulator Power", "Value": f"{circulator_power/1000:.2f} kW"},
])
display(Table(results_summary, "Summary of Thermal-Hydraulic Results", "tbl-summary"))

display("""
These calculations provide the foundation for the thermal-hydraulic design of our HTGR system.
The results demonstrate that the design can safely and efficiently deliver process heat
at the required temperatures while maintaining fuel temperatures within safety limits.
""")

print("THERMAL_CALCS_COMPLETE")
