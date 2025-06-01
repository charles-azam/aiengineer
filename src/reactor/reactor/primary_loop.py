"""
Primary coolant loop design for the Small Modular Reactor.
"""

from .config import SMR_CONFIG
from .utils import calculate_heat_transfer

print("Loaded primary_loop module")


class PrimaryLoop:
    """
    Class representing the primary coolant loop of the SMR.
    """

    def __init__(self, thermal_power, pressure, inlet_temp, outlet_temp, flow_rate):
        """
        Initialize the primary loop with design parameters.

        Args:
            thermal_power (float): Thermal power to transfer in MW
            pressure (float): Operating pressure in MPa
            inlet_temp (float): Core inlet temperature in °C
            outlet_temp (float): Core outlet temperature in °C
            flow_rate (float): Coolant flow rate in kg/s
        """
        self.thermal_power = thermal_power
        self.pressure = pressure
        self.inlet_temp = inlet_temp
        self.outlet_temp = outlet_temp
        self.flow_rate = flow_rate

        # Calculate derived parameters
        self.delta_t = outlet_temp - inlet_temp
        self.heat_transfer = calculate_heat_transfer(flow_rate, self.delta_t)

        # Design parameters
        self.num_loops = 2
        self.pump_power = self._calculate_pump_power()
        self.pipe_diameter = self._calculate_pipe_diameter()

    def _calculate_pump_power(self):
        """
        Calculate the approximate pump power required.

        Returns:
            float: Pump power in kW
        """
        # Simplified calculation - typically 1-2% of thermal power
        return self.thermal_power * 10  # kW (about 1% of thermal power)

    def _calculate_pipe_diameter(self):
        """
        Calculate the approximate primary loop pipe diameter.

        Returns:
            float: Pipe diameter in cm
        """
        # Simplified calculation based on flow rate and velocity
        # Assuming water density of ~750 kg/m³ at operating conditions
        # and target velocity of ~15 m/s
        water_density = 750  # kg/m³
        target_velocity = 15  # m/s

        # Flow rate per loop
        flow_per_loop = self.flow_rate / self.num_loops  # kg/s

        # Volumetric flow rate
        vol_flow = flow_per_loop / water_density  # m³/s

        # Area = flow rate / velocity
        area = vol_flow / target_velocity  # m²

        # Diameter = sqrt(4 * area / π)
        import math

        diameter = math.sqrt(4 * area / math.pi)  # m

        return diameter * 100  # convert to cm

    def calculate_pressure_drop(self):
        """
        Calculate the approximate pressure drop in the primary loop.

        Returns:
            float: Pressure drop in kPa
        """
        # Simplified calculation - typical values for PWR
        return 300.0  # kPa

    def display_info(self):
        """Display key information about the primary loop."""
        print("\n--- PRIMARY COOLANT LOOP ---")
        print(f"Thermal Power: {self.thermal_power} MW")
        print(f"Operating Pressure: {self.pressure} MPa")
        print(
            f"Temperature Range: {self.inlet_temp}°C to {self.outlet_temp}°C (ΔT: {self.delta_t}°C)"
        )
        print(f"Coolant Flow Rate: {self.flow_rate} kg/s")
        print(f"Number of Loops: {self.num_loops}")
        print(f"Main Pipe Diameter: {self.pipe_diameter:.1f} cm")
        print(f"Pump Power: {self.pump_power} kW")

        # Technology and manufacturing details
        print("Technology: Pressurized Water Reactor (PWR) primary system")
        print("Coolant: Light water (H₂O)")
        print("Pumps: Canned motor reactor coolant pumps by Flowserve")
        print("Materials: 316L stainless steel for piping and components")
        print(
            "Manufacturing: Factory-assembled modules with field welding of major connections"
        )
        print("Safety Features: Natural circulation capability for decay heat removal")


def calculate_safety_parameters():
    """
    Calculate and return safety parameters for the primary loop.

    Returns:
        dict: Dictionary containing safety parameters
    """
    safety_params = {
        "decay_heat_removal": 3.0,  # MW (passive capability)
        "natural_circulation_flow": 40.0,  # kg/s
        "pressure_relief_capacity": 200.0,  # kg/s
        "emergency_cooling_capacity": 5.0,  # MW
    }

    print("\n--- PRIMARY LOOP SAFETY PARAMETERS ---")
    print(f"Passive Decay Heat Removal: {safety_params['decay_heat_removal']} MW")
    print(f"Natural Circulation Flow: {safety_params['natural_circulation_flow']} kg/s")
    print(f"Pressure Relief Capacity: {safety_params['pressure_relief_capacity']} kg/s")
    print(
        f"Emergency Cooling Capacity: {safety_params['emergency_cooling_capacity']} MW"
    )

    return safety_params


if __name__ == "__main__":
    # Create a primary loop instance with configuration parameters
    primary = PrimaryLoop(
        thermal_power=SMR_CONFIG["thermal_power"],
        pressure=SMR_CONFIG["primary_pressure"],
        inlet_temp=SMR_CONFIG["primary_temp_inlet"],
        outlet_temp=SMR_CONFIG["primary_temp_outlet"],
        flow_rate=SMR_CONFIG["primary_flow_rate"],
    )

    # Display primary loop information
    primary.display_info()

    # Calculate and display safety parameters
    safety_params = calculate_safety_parameters()
