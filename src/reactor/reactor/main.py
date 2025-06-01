"""
Main entry point for the Small Modular Reactor (SMR) system.
This file integrates all components and provides a summary of the system.
"""

from .config import SMR_CONFIG
from .primary_loop import PrimaryLoop
from .reactor_core import ReactorCore
from .secondary_loop import SecondaryLoop
from .utils import calculate_economics, calculate_efficiency

print("Loaded main module")


def main():
    """
    Main function to initialize and integrate all SMR components.
    """
    print("=" * 50)
    print("SMALL MODULAR REACTOR (SMR) SYSTEM SUMMARY")
    print("=" * 50)

    # Initialize components
    reactor = ReactorCore(
        thermal_power=SMR_CONFIG["thermal_power"],
        core_height=SMR_CONFIG["core_height"],
        core_diameter=SMR_CONFIG["core_diameter"],
        fuel_type=SMR_CONFIG["fuel_type"],
        enrichment=SMR_CONFIG["enrichment"],
        fuel_assemblies=SMR_CONFIG["fuel_assemblies"],
    )

    primary = PrimaryLoop(
        thermal_power=SMR_CONFIG["thermal_power"],
        pressure=SMR_CONFIG["primary_pressure"],
        inlet_temp=SMR_CONFIG["primary_temp_inlet"],
        outlet_temp=SMR_CONFIG["primary_temp_outlet"],
        flow_rate=SMR_CONFIG["primary_flow_rate"],
    )

    secondary = SecondaryLoop(
        thermal_power=SMR_CONFIG["thermal_power"],
        pressure=SMR_CONFIG["secondary_pressure"],
        inlet_temp=SMR_CONFIG["secondary_temp_inlet"],
        outlet_temp=SMR_CONFIG["secondary_temp_outlet"],
        flow_rate=SMR_CONFIG["secondary_flow_rate"],
        efficiency=SMR_CONFIG["thermal_efficiency"],
    )

    # Display system information
    print("\nSYSTEM CONFIGURATION:")
    print(f"Thermal Power: {SMR_CONFIG['thermal_power']} MW")
    print(f"Electrical Power: {SMR_CONFIG['electrical_power']} MW")
    print(f"Thermal Efficiency: {SMR_CONFIG['thermal_efficiency']*100:.1f}%")
    print(f"Design Life: {SMR_CONFIG['design_life']} years")
    print(f"Refueling Interval: {SMR_CONFIG['refueling_interval']} months")

    # Display component information
    print("\nCOMPONENT SUMMARY:")
    reactor.display_info()
    primary.display_info()
    secondary.display_info()

    # Calculate and display performance metrics
    efficiency = calculate_efficiency(
        thermal_power=SMR_CONFIG["thermal_power"],
        electrical_power=SMR_CONFIG["electrical_power"],
    )

    economics = calculate_economics(
        electrical_power=SMR_CONFIG["electrical_power"],
        capacity_factor=SMR_CONFIG["availability_factor"],
        capital_cost_per_kw=5000,  # $5000/kW
        design_life=SMR_CONFIG["design_life"],
    )

    print("\nPERFORMANCE METRICS:")
    print(f"Net Thermal Efficiency: {efficiency*100:.2f}%")
    print(f"Annual Electricity Production: {economics['annual_production']:,.0f} MWh")
    print(f"Levelized Cost of Electricity: ${economics['lcoe']:.2f}/MWh")
    print(f"Estimated Construction Time: {economics['construction_time']} months")

    print("\nSAFETY FEATURES:")
    print("- Passive decay heat removal system")
    print("- Automatic depressurization system")
    print("- Emergency core cooling system")
    print("- Containment isolation and cooling")

    print("\nMANUFACTURING APPROACH:")
    print("- Factory fabrication of major components")
    print("- Modular assembly for reduced on-site construction")
    print("- Standardized design for series production")
    print("- Transportable by rail, road, or barge")

    print("=" * 50)


if __name__ == "__main__":
    main()
