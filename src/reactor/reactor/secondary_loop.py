"""
Secondary loop for power generation in the Small Modular Reactor.
"""
from .config import SMR_CONFIG
from .utils import calculate_heat_transfer
print("Loaded secondary_loop module")

class SecondaryLoop:
    """
    Class representing the secondary loop for power generation.
    """
    def __init__(self, thermal_power, pressure, inlet_temp, outlet_temp, 
                 flow_rate, efficiency):
        """
        Initialize the secondary loop with design parameters.
        
        Args:
            thermal_power (float): Thermal power input in MW
            pressure (float): Steam pressure in MPa
            inlet_temp (float): Feedwater inlet temperature in °C
            outlet_temp (float): Steam outlet temperature in °C
            flow_rate (float): Steam/water flow rate in kg/s
            efficiency (float): Thermal-to-electrical conversion efficiency
        """
        self.thermal_power = thermal_power
        self.pressure = pressure
        self.inlet_temp = inlet_temp
        self.outlet_temp = outlet_temp
        self.flow_rate = flow_rate
        self.efficiency = efficiency
        
        # Calculate derived parameters
        self.electrical_power = thermal_power * efficiency
        self.delta_t = outlet_temp - inlet_temp
        self.heat_transfer = calculate_heat_transfer(flow_rate, self.delta_t)
        self.steam_quality = self._calculate_steam_quality()
        
    def _calculate_steam_quality(self):
        """
        Calculate the approximate steam quality.
        For superheated steam, quality is 1.0
        
        Returns:
            float: Steam quality (1.0 for superheated steam)
        """
        # For typical PWR secondary loop with superheated steam
        return 1.0
    
    def calculate_turbine_parameters(self):
        """
        Calculate turbine parameters based on steam conditions.
        
        Returns:
            dict: Dictionary containing turbine parameters
        """
        # Simplified calculations for turbine parameters
        turbine_params = {
            "inlet_pressure": self.pressure,  # MPa
            "outlet_pressure": 0.008,  # MPa (typical condenser pressure)
            "isentropic_efficiency": 0.85,
            "mechanical_efficiency": 0.98,
            "generator_efficiency": 0.985,
            "shaft_power": self.electrical_power / 0.985,  # MW
        }
        
        return turbine_params
    
    def calculate_condenser_parameters(self):
        """
        Calculate condenser parameters.
        
        Returns:
            dict: Dictionary containing condenser parameters
        """
        # Simplified calculations for condenser parameters
        waste_heat = self.thermal_power - self.electrical_power
        
        condenser_params = {
            "heat_rejection": waste_heat,  # MW
            "cooling_water_temp_in": 20.0,  # °C
            "cooling_water_temp_out": 30.0,  # °C
            "cooling_water_flow": waste_heat * 1000 / (4.18 * 10),  # kg/s
        }
        
        return condenser_params
    
    def display_info(self):
        """Display key information about the secondary loop."""
        print("\n--- SECONDARY LOOP ---")
        print(f"Thermal Power Input: {self.thermal_power} MW")
        print(f"Electrical Power Output: {self.electrical_power} MW")
        print(f"Thermal Efficiency: {self.efficiency*100:.1f}%")
        print(f"Steam Pressure: {self.pressure} MPa")
        print(f"Temperature Range: {self.inlet_temp}°C to {self.outlet_temp}°C")
        print(f"Steam/Water Flow Rate: {self.flow_rate} kg/s")
        
        turbine_params = self.calculate_turbine_parameters()
        condenser_params = self.calculate_condenser_parameters()
        
        print(f"Turbine Shaft Power: {turbine_params['shaft_power']:.2f} MW")
        print(f"Condenser Heat Rejection: {condenser_params['heat_rejection']:.2f} MW")
        print(f"Cooling Water Flow: {condenser_params['cooling_water_flow']:.1f} kg/s")
        
        # Technology and manufacturing details
        print("Technology: Conventional Rankine cycle")
        print("Turbine: Siemens SST-150 compact steam turbine")
        print("Generator: Brushless synchronous generator by ABB")
        print("Condenser: Shell and tube design with titanium tubes")
        print("Materials: Carbon steel for main steam lines, stainless steel for wet steam components")
        print("Manufacturing: Skid-mounted modular assembly for rapid installation")

def calculate_power_output(thermal_power, efficiency):
    """
    Calculate electrical power output based on thermal power and efficiency.
    
    Args:
        thermal_power (float): Thermal power in MW
        efficiency (float): Thermal-to-electrical conversion efficiency
        
    Returns:
        float: Electrical power output in MW
    """
    electrical_power = thermal_power * efficiency
    
    print(f"\nThermal Power: {thermal_power} MW")
    print(f"Thermal Efficiency: {efficiency*100:.1f}%")
    print(f"Electrical Power Output: {electrical_power} MW")
    
    return electrical_power

if __name__ == "__main__":
    # Create a secondary loop instance with configuration parameters
    secondary = SecondaryLoop(
        thermal_power=SMR_CONFIG['thermal_power'],
        pressure=SMR_CONFIG['secondary_pressure'],
        inlet_temp=SMR_CONFIG['secondary_temp_inlet'],
        outlet_temp=SMR_CONFIG['secondary_temp_outlet'],
        flow_rate=SMR_CONFIG['secondary_flow_rate'],
        efficiency=SMR_CONFIG['thermal_efficiency']
    )
    
    # Display secondary loop information
    secondary.display_info()
    
    # Calculate and display power output
    power_output = calculate_power_output(
        SMR_CONFIG['thermal_power'],
        SMR_CONFIG['thermal_efficiency']
    )
