"""
Design specifications for the 20 MW reactor core.
"""

import math

from .config import SMR_CONFIG
from .utils import calculate_power_density

print("Loaded reactor_core module")


class ReactorCore:
    """
    Class representing the nuclear reactor core.
    """

    def __init__(
        self,
        thermal_power,
        core_height,
        core_diameter,
        fuel_type,
        enrichment,
        fuel_assemblies,
    ):
        """
        Initialize the reactor core with design parameters.

        Args:
            thermal_power (float): Thermal power output in MW
            core_height (float): Height of the core in meters
            core_diameter (float): Diameter of the core in meters
            fuel_type (str): Type of nuclear fuel
            enrichment (float): Fuel enrichment percentage
            fuel_assemblies (int): Number of fuel assemblies
        """
        self.thermal_power = thermal_power
        self.core_height = core_height
        self.core_diameter = core_diameter
        self.fuel_type = fuel_type
        self.enrichment = enrichment
        self.fuel_assemblies = fuel_assemblies

        # Calculate derived parameters
        self.core_volume = self._calculate_core_volume()
        self.power_density = calculate_power_density(thermal_power, self.core_volume)

    def _calculate_core_volume(self):
        """Calculate the volume of the cylindrical core in cubic meters."""
        radius = self.core_diameter / 2
        return math.pi * radius**2 * self.core_height

    def calculate_fuel_loading(self):
        """
        Calculate the approximate fuel loading in the core.

        Returns:
            float: Fuel loading in metric tons of uranium
        """
        # Approximate calculation based on typical PWR fuel density
        # Assuming 10.4 g/cm³ for UO2 and ~88% theoretical density in fuel pellets
        fuel_volume_fraction = 0.3  # Typical for PWR
        uranium_density = 10.4 * 0.88 * fuel_volume_fraction  # g/cm³

        # Convert core volume to cm³
        core_volume_cm3 = self.core_volume * 1e6

        # Calculate uranium mass in metric tons
        uranium_mass = uranium_density * core_volume_cm3 / 1e6

        return uranium_mass

    def calculate_burnup(self, cycle_length_days=730):
        """
        Calculate the average fuel burnup at end of cycle.

        Args:
            cycle_length_days (int): Length of fuel cycle in days

        Returns:
            float: Average burnup in GWd/MTU
        """
        fuel_loading = self.calculate_fuel_loading()
        energy_per_day = self.thermal_power / 1000  # GWth
        total_energy = energy_per_day * cycle_length_days  # GWd

        burnup = total_energy / fuel_loading  # GWd/MTU

        return burnup

    def display_info(self):
        """Display key information about the reactor core."""
        print("\n--- REACTOR CORE ---")
        print(f"Thermal Power: {self.thermal_power} MW")
        print(f"Core Dimensions: {self.core_height} m (H) × {self.core_diameter} m (D)")
        print(f"Core Volume: {self.core_volume:.2f} m³")
        print(f"Power Density: {self.power_density:.2f} MW/m³")
        print(f"Fuel Type: {self.fuel_type} enriched to {self.enrichment}% U-235")
        print(f"Fuel Assemblies: {self.fuel_assemblies}")

        fuel_loading = self.calculate_fuel_loading()
        burnup = self.calculate_burnup()
        print(f"Fuel Loading: {fuel_loading:.2f} MTU")
        print(f"Design Burnup: {burnup:.1f} GWd/MTU")

        # Technology and manufacturing details
        print("Technology: Pressurized Water Reactor (PWR)")
        print("Manufacturer: Westinghouse AP300 derived technology")
        print(
            "Materials: Zirconium alloy fuel cladding, 316L stainless steel structures"
        )
        print("Manufacturing: Factory-assembled modular core structure")


def calculate_reactivity_coefficients():
    """
    Calculate and return the reactivity coefficients for the SMR core.

    Returns:
        dict: Dictionary containing reactivity coefficients
    """
    # Typical values for a small PWR
    coefficients = {
        "fuel_temperature": -2.0,  # pcm/°C
        "moderator_temperature": -40.0,  # pcm/°C
        "void": -100.0,  # pcm/% void
        "boron": -10.0,  # pcm/ppm
    }

    print("\n--- REACTIVITY COEFFICIENTS ---")
    print(f"Fuel Temperature Coefficient: {coefficients['fuel_temperature']} pcm/°C")
    print(
        f"Moderator Temperature Coefficient: {coefficients['moderator_temperature']} pcm/°C"
    )
    print(f"Void Coefficient: {coefficients['void']} pcm/% void")
    print(f"Boron Worth: {coefficients['boron']} pcm/ppm")

    return coefficients


if __name__ == "__main__":
    # Create a reactor core instance with configuration parameters
    core = ReactorCore(
        thermal_power=SMR_CONFIG["thermal_power"],
        core_height=SMR_CONFIG["core_height"],
        core_diameter=SMR_CONFIG["core_diameter"],
        fuel_type=SMR_CONFIG["fuel_type"],
        enrichment=SMR_CONFIG["enrichment"],
        fuel_assemblies=SMR_CONFIG["fuel_assemblies"],
    )

    # Display core information
    core.display_info()

    # Calculate and display reactivity coefficients
    coefficients = calculate_reactivity_coefficients()
