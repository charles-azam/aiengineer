"""
Simulation models for the Small Modular Reactor (SMR).
"""

from .parameters_reactor import REACTOR_PARAMS

print("Loaded simulation_reactor module")


def calculate_power_output():
    """
    Calculate the electrical power output based on thermal power and efficiency.
    """
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude
    efficiency = REACTOR_PARAMS.thermal_efficiency
    electrical_power = thermal_power * efficiency

    print(f"Thermal power: {thermal_power} MW")
    print(f"Thermal efficiency: {efficiency*100:.1f}%")
    print(f"Electrical power output: {electrical_power} MW")

    return electrical_power


def calculate_annual_energy_production():
    """
    Calculate the annual energy production in MWh.
    """
    electrical_power = REACTOR_PARAMS.electrical_power.magnitude
    availability = REACTOR_PARAMS.availability_factor
    hours_per_year = 365 * 24

    annual_energy = electrical_power * availability * hours_per_year
    capacity_factor = availability

    print(f"Annual energy production: {annual_energy:,.0f} MWh")
    print(f"Capacity factor: {capacity_factor*100:.1f}%")

    return annual_energy


def calculate_fuel_consumption():
    """
    Estimate annual fuel consumption based on thermal power.
    """
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude
    enrichment = REACTOR_PARAMS.enrichment / 100
    refueling_interval = REACTOR_PARAMS.refueling_interval

    # Approximate calculation - actual consumption depends on burnup
    # Assuming ~1 MT of fuel per GWd/MT burnup at 50 GWd/MT
    energy_per_month = thermal_power * 30 * 24 / 1000  # GWd
    fuel_per_month = energy_per_month / 50  # MT
    fuel_per_refueling = fuel_per_month * refueling_interval

    print(
        f"Estimated fuel load per {refueling_interval}-month cycle: {fuel_per_refueling:.2f} MT"
    )
    print(f"Fuel enrichment: {enrichment*100:.2f}% U-235")

    return fuel_per_refueling


def calculate_primary_loop_parameters():
    """
    Calculate key parameters for the primary cooling loop.
    """
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude
    flow_rate = REACTOR_PARAMS.primary_flow_rate.magnitude
    temp_inlet = REACTOR_PARAMS.primary_temp_inlet.magnitude
    temp_outlet = REACTOR_PARAMS.primary_temp_outlet.magnitude

    # Specific heat capacity of water at high pressure (approximate)
    cp_water = 4.2  # kJ/kg·K

    # Calculate temperature rise
    delta_t = temp_outlet - temp_inlet

    # Calculate heat transfer
    heat_transfer = flow_rate * cp_water * delta_t / 1000  # MW

    print(f"Primary loop flow rate: {flow_rate} kg/s")
    print(f"Primary loop temperature rise: {delta_t:.1f}°C")
    print(f"Primary loop heat transfer: {heat_transfer:.1f} MW")

    return heat_transfer


def calculate_secondary_loop_parameters():
    """
    Calculate key parameters for the secondary loop.
    """
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude
    electrical_power = REACTOR_PARAMS.electrical_power.magnitude
    efficiency = REACTOR_PARAMS.thermal_efficiency

    # Calculate waste heat
    waste_heat = thermal_power - electrical_power

    print(f"Power conversion efficiency: {efficiency*100:.1f}%")
    print(f"Electrical output: {electrical_power} MW")
    print(f"Waste heat: {waste_heat:.1f} MW")

    return waste_heat


def run_all_simulations():
    """
    Run all simulation calculations and return results.
    """
    print("===== SMR SIMULATION RESULTS =====")

    electrical_power = calculate_power_output()
    print("\n")

    annual_energy = calculate_annual_energy_production()
    print("\n")

    fuel_consumption = calculate_fuel_consumption()
    print("\n")

    primary_heat = calculate_primary_loop_parameters()
    print("\n")

    waste_heat = calculate_secondary_loop_parameters()
    print("\n")

    print("=================================")

    return {
        "electrical_power": electrical_power,
        "annual_energy": annual_energy,
        "fuel_consumption": fuel_consumption,
        "primary_heat": primary_heat,
        "waste_heat": waste_heat,
    }


# Run simulations when module is executed directly
if __name__ == "__main__":
    run_all_simulations()
