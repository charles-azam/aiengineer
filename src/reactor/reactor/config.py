"""
Configuration parameters for the Small Modular Reactor (SMR) system.
"""

# Main configuration dictionary for the SMR
SMR_CONFIG = {
    # Core parameters
    "thermal_power": 60.0,  # MW thermal
    "electrical_power": 20.0,  # MW electrical
    "thermal_efficiency": 0.33,  # Conversion efficiency
    "core_height": 2.5,  # m
    "core_diameter": 1.8,  # m
    "fuel_type": "UO2",  # Uranium dioxide
    "enrichment": 4.95,  # % U-235
    "fuel_assemblies": 37,  # Number of fuel assemblies
    # Primary loop parameters
    "primary_pressure": 15.5,  # MPa
    "primary_temp_inlet": 290.0,  # °C
    "primary_temp_outlet": 325.0,  # °C
    "primary_flow_rate": 320.0,  # kg/s
    # Secondary loop parameters
    "secondary_pressure": 7.0,  # MPa
    "secondary_temp_inlet": 230.0,  # °C
    "secondary_temp_outlet": 290.0,  # °C
    "secondary_flow_rate": 110.0,  # kg/s
    # Operational parameters
    "design_life": 60,  # years
    "refueling_interval": 24,  # months
    "availability_factor": 0.95,  # % uptime
    # Physical dimensions
    "containment_height": 25.0,  # m
    "containment_diameter": 15.0,  # m
    "total_weight": 350.0,  # ton
    # Safety parameters
    "safety_systems": [
        "Passive Residual Heat Removal System",
        "Automatic Depressurization System",
        "In-containment Refueling Water Storage Tank",
        "Passive Containment Cooling System",
    ],
    # Manufacturing parameters
    "modular_components": [
        "Reactor Vessel",
        "Steam Generators",
        "Pressurizer",
        "Containment Vessel",
        "Control Rod Drive Mechanisms",
        "Turbine-Generator Set",
    ],
    # Economic parameters
    "capital_cost_per_kw": 5000,  # $/kW
    "om_cost_per_mwh": 40,  # $/MWh
    "fuel_cost_per_mwh": 7,  # $/MWh
    "decommissioning_cost_per_kw": 500,  # $/kW
    "discount_rate": 0.07,  # 7%
}

# Constants for calculations
WATER_SPECIFIC_HEAT = 4.2  # kJ/kg·K
STEAM_ENTHALPY_VAPORIZATION = 2000  # kJ/kg at ~7 MPa


def print_config_summary():
    """Print a summary of the SMR configuration."""
    print("SMR CONFIGURATION SUMMARY")
    print("-" * 30)
    print(f"Thermal Power: {SMR_CONFIG['thermal_power']} MW")
    print(f"Electrical Power: {SMR_CONFIG['electrical_power']} MW")
    print(f"Thermal Efficiency: {SMR_CONFIG['thermal_efficiency']*100:.1f}%")
    print(
        f"Core Dimensions: {SMR_CONFIG['core_height']}m × {SMR_CONFIG['core_diameter']}m (H×D)"
    )
    print(
        f"Primary Loop: {SMR_CONFIG['primary_pressure']} MPa, "
        f"{SMR_CONFIG['primary_temp_inlet']}°C to {SMR_CONFIG['primary_temp_outlet']}°C"
    )
    print(
        f"Secondary Loop: {SMR_CONFIG['secondary_pressure']} MPa, "
        f"{SMR_CONFIG['secondary_temp_inlet']}°C to {SMR_CONFIG['secondary_temp_outlet']}°C"
    )
    print(f"Design Life: {SMR_CONFIG['design_life']} years")
    print("-" * 30)


if __name__ == "__main__":
    print_config_summary()
