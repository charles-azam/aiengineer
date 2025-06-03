"""
Thermal Energy Storage System Calculations.

This document provides detailed thermal calculations for high-temperature
thermal energy storage systems, including heat capacity, energy density,
heat transfer, losses, and efficiency calculations.
"""

from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
# Import unit registry first
from epyr.tools_units import UNIT_REGISTRY, Quantity

from epyr.parameters_materials import (
    MOLTEN_SALT,
    SOLID_CERAMIC,
    HIGH_TEMP_CERAMIC,
    MOLTEN_METAL,
    PHASE_CHANGE_MATERIAL
)
import pandas as pd
import numpy as np

# Print debug information
print("Loading thermal calculations document")

# Document configuration
config = DocumentConfig(
    title="Thermal Energy Storage System Calculations",
    author="EPYR Engineering Team",
    date="2025-06-02"
)
display(config)

# Introduction
display(Title("# Thermal Energy Storage System Calculations"))
display(
    "This document provides detailed thermal calculations for high-temperature "
    "thermal energy storage systems. These calculations form the foundation for "
    "our system design and performance estimates."
)

# Heat Capacity and Energy Density Calculations
display(Title("## 1. Heat Capacity and Energy Density Calculations"))

display("### 1.1 Sensible Heat Storage")
display(
    "The energy stored in a sensible heat storage medium is calculated using the formula:"
)
display("$$Q = m \cdot c_p \cdot \Delta T$$")
display(
    "Where:\n"
    "- $Q$ is the thermal energy stored [J]\n"
    "- $m$ is the mass of the storage medium [kg]\n"
    "- $c_p$ is the specific heat capacity [J/(kg·K)]\n"
    "- $\\Delta T$ is the temperature difference [K]"
)

# Example calculation for molten salt
mass = Quantity(1000, "kg")
temp_high = Quantity(565, "°C")
temp_low = Quantity(290, "°C")
delta_T = temp_high.to("K") - temp_low.to("K")

energy_salt = mass * MOLTEN_SALT.specific_heat * delta_T
energy_density_salt = energy_salt / (mass / MOLTEN_SALT.density)

display("#### Example: Molten Salt Storage")
display(f"For {mass} of molten salt with:")
display(f"- Specific heat capacity: {MOLTEN_SALT.specific_heat}")
display(f"- Temperature range: {temp_low} to {temp_high}")
display(f"- Energy stored: {energy_salt.to('MJ'):.2f}")
display(f"- Volumetric energy density: {energy_density_salt.to('MJ/m^3'):.2f}")

# Create comparison table for different materials
materials = ["Molten Salt", "Solid Ceramic", "High Temp Ceramic", "Molten Metal"]
material_params = [MOLTEN_SALT, SOLID_CERAMIC, HIGH_TEMP_CERAMIC, MOLTEN_METAL]

energy_densities = []
for material in material_params:
    energy = mass * material.specific_heat * delta_T
    vol_energy_density = energy / (mass / material.density)
    energy_densities.append({
        "Material": materials[material_params.index(material)],
        "Specific Heat": f"{material.specific_heat}",
        "Density": f"{material.density}",
        "Energy Stored (1000kg)": f"{energy.to('MJ'):.2f}",
        "Energy Density": f"{vol_energy_density.to('MJ/m^3'):.2f}"
    })

df_energy = pd.DataFrame(energy_densities)
display(Table(df_energy, "Energy Storage Comparison of Materials", "tbl-energy-density"))

display("### 1.2 Latent Heat Storage")
display(
    "For phase change materials (PCM), the total energy stored includes both sensible and latent heat:"
)
display("$$Q_{total} = m \cdot c_{p,s} \cdot (T_m - T_{min}) + m \cdot L + m \cdot c_{p,l} \cdot (T_{max} - T_m)$$")
display(
    "Where:\n"
    "- $Q_{total}$ is the total thermal energy stored [J]\n"
    "- $c_{p,s}$ and $c_{p,l}$ are the specific heat capacities in solid and liquid phases [J/(kg·K)]\n"
    "- $T_m$ is the melting temperature [K]\n"
    "- $L$ is the latent heat of fusion [J/kg]"
)

# Example calculation for PCM
pcm_mass = Quantity(1000, "kg")
pcm_temp_min = Quantity(250, "°C")
pcm_temp_max = Quantity(450, "°C")
pcm_melt_temp = Quantity(PHASE_CHANGE_MATERIAL.melting_point, "°C")

# Convert temperatures to Kelvin for calculations
pcm_temp_min_K = pcm_temp_min.to("K").magnitude
pcm_temp_max_K = pcm_temp_max.to("K").magnitude
pcm_melt_temp_K = pcm_melt_temp.to("K").magnitude

# Calculate energy components
sensible_heat_solid = pcm_mass * PHASE_CHANGE_MATERIAL.specific_heat_solid * (pcm_melt_temp_K - pcm_temp_min_K)
latent_heat = pcm_mass * PHASE_CHANGE_MATERIAL.latent_heat
sensible_heat_liquid = pcm_mass * PHASE_CHANGE_MATERIAL.specific_heat_liquid * (pcm_temp_max_K - pcm_melt_temp_K)
# Convert all to same units before adding
sensible_heat_solid_J = sensible_heat_solid.to("joule")
latent_heat_J = latent_heat.to("joule")
sensible_heat_liquid_J = sensible_heat_liquid.to("joule")
total_energy_pcm = sensible_heat_solid_J + latent_heat_J + sensible_heat_liquid_J

display("#### Example: Phase Change Material Storage")
display(f"For {pcm_mass} of PCM with:")
display(f"- Melting point: {pcm_melt_temp}")
display(f"- Latent heat: {PHASE_CHANGE_MATERIAL.latent_heat}")
display(f"- Temperature range: {pcm_temp_min} to {pcm_temp_max}")
display(f"- Sensible heat (solid phase): {sensible_heat_solid.to('MJ'):.2f}")
display(f"- Latent heat at phase change: {latent_heat.to('MJ'):.2f}")
display(f"- Sensible heat (liquid phase): {sensible_heat_liquid.to('MJ'):.2f}")
display(f"- Total energy stored: {total_energy_pcm.to('MJ'):.2f}")

# Heat Transfer Calculations
display(Title("## 2. Heat Transfer Calculations"))

display("### 2.1 Conduction Heat Transfer")
display(
    "The rate of heat transfer through conduction is given by Fourier's law:"
)
display("$$q = -k \cdot A \cdot \frac{dT}{dx}$$")
display(
    "Where:\n"
    "- $q$ is the heat transfer rate [W]\n"
    "- $k$ is the thermal conductivity [W/(m·K)]\n"
    "- $A$ is the cross-sectional area [m²]\n"
    "- $\\frac{dT}{dx}$ is the temperature gradient [K/m]"
)

# Example calculation for conduction through storage medium
area = Quantity(10, "m^2")
thickness = Quantity(0.5, "m")
temp_diff = Quantity(200, "K")
temp_gradient = temp_diff / thickness

# Calculate for different materials
conduction_rates = []
for material in material_params:
    heat_rate = material.thermal_conductivity * area * temp_gradient
    conduction_rates.append({
        "Material": materials[material_params.index(material)],
        "Thermal Conductivity": f"{material.thermal_conductivity}",
        "Heat Transfer Rate": f"{heat_rate.to('kW'):.2f}"
    })

df_conduction = pd.DataFrame(conduction_rates)
display(Table(df_conduction, "Conduction Heat Transfer Rates", "tbl-conduction"))

display("### 2.2 Convection Heat Transfer")
display(
    "The rate of heat transfer through convection is given by Newton's law of cooling:"
)
display("$$q = h \cdot A \cdot (T_s - T_{\infty})$$")
display(
    "Where:\n"
    "- $h$ is the convection heat transfer coefficient [W/(m²·K)]\n"
    "- $A$ is the surface area [m²]\n"
    "- $T_s$ is the surface temperature [K]\n"
    "- $T_{\\infty}$ is the fluid temperature [K]"
)

# Example calculation for convection in heat exchanger
h_coeff = Quantity(500, "W/(m^2*K)")  # Typical for forced convection with liquid
surface_area = Quantity(20, "m^2")
surface_temp = Quantity(500, "°C")
fluid_temp = Quantity(300, "°C")
temp_diff_conv = surface_temp.to("K") - fluid_temp.to("K")

convection_rate = h_coeff * surface_area * temp_diff_conv

display("#### Example: Convection in Heat Exchanger")
display(f"For a heat exchanger with:")
display(f"- Convection coefficient: {h_coeff}")
display(f"- Surface area: {surface_area}")
display(f"- Surface temperature: {surface_temp}")
display(f"- Fluid temperature: {fluid_temp}")
display(f"- Heat transfer rate: {convection_rate.to('kW'):.2f}")

# Heat Loss Calculations
display(Title("## 3. Heat Loss Calculations"))

display("### 3.1 Insulation Performance")
display(
    "The heat loss through insulation can be calculated using the thermal resistance concept:"
)
display("$$q_{loss} = \frac{A \cdot (T_{inside} - T_{outside})}{R_{total}}$$")
display(
    "Where:\n"
    "- $R_{total}$ is the total thermal resistance [K/W]\n"
    "- For a multi-layer insulation: $R_{total} = \\sum_{i} \\frac{L_i}{k_i \\cdot A}$\n"
    "- $L_i$ is the thickness of each insulation layer [m]\n"
    "- $k_i$ is the thermal conductivity of each layer [W/(m·K)]"
)

# Example calculation for insulation heat loss
insulation_thickness = Quantity(0.3, "m")
insulation_k = Quantity(0.05, "W/(m*K)")  # Typical for high-temp insulation
tank_surface_area = Quantity(100, "m^2")
tank_inside_temp = Quantity(550, "°C")
ambient_temp = Quantity(25, "°C")

thermal_resistance = insulation_thickness / (insulation_k * tank_surface_area)
heat_loss = (tank_inside_temp.to("K") - ambient_temp.to("K")) / thermal_resistance

display("#### Example: Heat Loss Through Insulation")
display(f"For a storage tank with:")
display(f"- Insulation thickness: {insulation_thickness}")
display(f"- Insulation thermal conductivity: {insulation_k}")
display(f"- Tank surface area: {tank_surface_area}")
display(f"- Inside temperature: {tank_inside_temp}")
display(f"- Ambient temperature: {ambient_temp}")
display(f"- Heat loss rate: {heat_loss.to('kW'):.2f}")

# System Efficiency Calculations
display(Title("## 4. System Efficiency Calculations"))

display("### 4.1 Round-Trip Efficiency")
display(
    "The round-trip efficiency of a thermal energy storage system is calculated as:"
)
display("$$\eta_{RT} = \frac{E_{out}}{E_{in}} = \frac{E_{stored} - E_{losses}}{E_{in}}$$")
display(
    "Where:\n"
    "- $\\eta_{RT}$ is the round-trip efficiency\n"
    "- $E_{out}$ is the energy extracted from storage [J]\n"
    "- $E_{in}$ is the energy input to storage [J]\n"
    "- $E_{losses}$ includes thermal losses, conversion losses, etc. [J]"
)

# Example calculation for system efficiency
energy_input = Quantity(1000, "MWh")
storage_duration = Quantity(24, "hour")
heat_loss_rate = Quantity(50, "kW")
conversion_efficiency_in = 0.95  # 95% efficiency in charging
conversion_efficiency_out = 0.90  # 90% efficiency in discharging

total_heat_loss = heat_loss_rate * storage_duration
energy_after_charging = energy_input * conversion_efficiency_in
energy_after_storage = energy_after_charging - total_heat_loss
energy_output = energy_after_storage * conversion_efficiency_out
round_trip_efficiency = energy_output / energy_input

display("#### Example: Round-Trip Efficiency Calculation")
display(f"For a thermal storage system with:")
display(f"- Energy input: {energy_input}")
display(f"- Storage duration: {storage_duration}")
display(f"- Heat loss rate: {heat_loss_rate}")
display(f"- Charging efficiency: {conversion_efficiency_in*100}%")
display(f"- Discharging efficiency: {conversion_efficiency_out*100}%")
display(f"- Total heat loss: {total_heat_loss.to('MWh'):.2f}")
display(f"- Energy after charging: {energy_after_charging.to('MWh'):.2f}")
display(f"- Energy after storage period: {energy_after_storage.to('MWh'):.2f}")
display(f"- Energy output: {energy_output.to('MWh'):.2f}")
display(f"- Round-trip efficiency: {round_trip_efficiency.magnitude*100:.1f}%")

# Thermal Stratification Effects
display(Title("## 5. Thermal Stratification Effects"))

display(
    "Thermal stratification in liquid storage media can improve system efficiency. "
    "The thermocline thickness in a stratified tank can be estimated using:"
)
display("$$\delta = \frac{k \cdot t}{\rho \cdot c_p \cdot v}$$")
display(
    "Where:\n"
    "- $\\delta$ is the thermocline thickness [m]\n"
    "- $k$ is the thermal conductivity [W/(m·K)]\n"
    "- $t$ is time [s]\n"
    "- $\\rho$ is density [kg/m³]\n"
    "- $c_{p}$ is specific heat capacity [J/(kg·K)]\n"
    "- $v$ is the characteristic velocity [m/s]"
)

# Example calculation for thermocline thickness
time_period = Quantity(8, "hour")
flow_velocity = Quantity(0.001, "m/s")  # Very slow flow for stratification

thermocline_thickness = (MOLTEN_SALT.thermal_conductivity * time_period) / (
    MOLTEN_SALT.density * MOLTEN_SALT.specific_heat * flow_velocity
)

display("#### Example: Thermocline Thickness in Molten Salt Storage")
display(f"For a molten salt storage with:")
display(f"- Thermal conductivity: {MOLTEN_SALT.thermal_conductivity}")
display(f"- Density: {MOLTEN_SALT.density}")
display(f"- Specific heat: {MOLTEN_SALT.specific_heat}")
display(f"- Time period: {time_period}")
display(f"- Flow velocity: {flow_velocity}")
display(f"- Estimated thermocline thickness: {thermocline_thickness.to('cm'):.2f}")

# Conclusion
display(Title("# Conclusion"))
display(
    "These thermal calculations provide the foundation for designing an efficient "
    "thermal energy storage system. The calculations demonstrate that:\n\n"
    "1. Different storage media offer varying energy densities, with molten salt and "
    "high-temperature ceramics providing good thermal storage capabilities.\n\n"
    "2. Heat transfer rates are critical for charging and discharging, with material "
    "selection significantly impacting system performance.\n\n"
    "3. Proper insulation is essential to minimize heat losses during storage periods.\n\n"
    "4. Round-trip efficiency depends on multiple factors including conversion efficiencies "
    "and thermal losses.\n\n"
    "5. Thermal stratification can be leveraged to improve system performance in liquid-based storage."
)

print("Thermal calculations document generated successfully.")
