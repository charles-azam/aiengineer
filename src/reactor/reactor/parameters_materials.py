"""
Material specifications for the Small Modular Reactor.
Contains detailed material properties and specifications.
"""

from pyforge import Parameters, Quantity

class CoreMaterials(Parameters):
    """Materials used in the reactor core."""
    fuel_pellet: str = "UO2"
    fuel_enrichment: Quantity = Quantity(19.75, "%")
    fuel_density: Quantity = Quantity(10.97, "g/cm³")
    fuel_thermal_conductivity: Quantity = Quantity(2.8, "W/m·K")
    fuel_melting_point: Quantity = Quantity(2865, "°C")
    
    cladding_material: str = "Zircaloy-4"
    cladding_thickness: Quantity = Quantity(0.57, "mm")
    cladding_density: Quantity = Quantity(6.56, "g/cm³")
    cladding_thermal_conductivity: Quantity = Quantity(17.0, "W/m·K")
    cladding_melting_point: Quantity = Quantity(1850, "°C")
    
    moderator_material: str = "Light Water"
    moderator_density: Quantity = Quantity(0.7, "g/cm³")
    moderator_thermal_conductivity: Quantity = Quantity(0.6, "W/m·K")
    
    control_rod_material: str = "Ag-In-Cd"
    control_rod_composition: str = "80% Ag, 15% In, 5% Cd"
    control_rod_density: Quantity = Quantity(10.2, "g/cm³")
    control_rod_melting_point: Quantity = Quantity(800, "°C")

class PressureVesselMaterials(Parameters):
    """Materials used in the reactor pressure vessel."""
    vessel_material: str = "SA-508 Grade 3 Class 1"
    vessel_density: Quantity = Quantity(7.85, "g/cm³")
    vessel_thermal_conductivity: Quantity = Quantity(45, "W/m·K")
    vessel_tensile_strength: Quantity = Quantity(550, "MPa")
    vessel_yield_strength: Quantity = Quantity(345, "MPa")
    
    cladding_material: str = "308L/309L Stainless Steel"
    cladding_thickness: Quantity = Quantity(5, "mm")
    cladding_density: Quantity = Quantity(7.9, "g/cm³")
    cladding_thermal_conductivity: Quantity = Quantity(15, "W/m·K")
    cladding_corrosion_resistance: str = "Excellent"
    
    manufacturer: str = "Doosan Heavy Industries"
    manufacturing_process: str = "Forging and machining with automated welding"
    quality_control: str = "100% volumetric examination with phased array ultrasonic testing"

class SteamGeneratorMaterials(Parameters):
    """Materials used in the steam generators."""
    tube_material: str = "Inconel 690"
    tube_density: Quantity = Quantity(8.19, "g/cm³")
    tube_thermal_conductivity: Quantity = Quantity(15, "W/m·K")
    tube_tensile_strength: Quantity = Quantity(725, "MPa")
    tube_yield_strength: Quantity = Quantity(345, "MPa")
    tube_corrosion_resistance: str = "Excellent"
    
    shell_material: str = "Carbon Steel SA-508"
    shell_density: Quantity = Quantity(7.85, "g/cm³")
    shell_thermal_conductivity: Quantity = Quantity(45, "W/m·K")
    shell_tensile_strength: Quantity = Quantity(550, "MPa")
    
    manufacturer: str = "Babcock & Wilcox"
    manufacturing_process: str = "Precision CNC machining with robotic welding and automated inspection"
    quality_control: str = "100% eddy current testing of tubes and radiographic examination of welds"

class ContainmentMaterials(Parameters):
    """Materials used in the containment structure."""
    concrete_type: str = "High-strength reinforced concrete"
    concrete_density: Quantity = Quantity(2400, "kg/m³")
    concrete_compressive_strength: Quantity = Quantity(60, "MPa")
    concrete_tensile_strength: Quantity = Quantity(5, "MPa")
    
    reinforcement_material: str = "High-strength steel rebar"
    reinforcement_yield_strength: Quantity = Quantity(500, "MPa")
    reinforcement_density: Quantity = Quantity(7.85, "g/cm³")
    
    liner_material: str = "Carbon Steel SA-516 Grade 70"
    liner_thickness: Quantity = Quantity(6, "mm")
    liner_density: Quantity = Quantity(7.85, "g/cm³")
    liner_yield_strength: Quantity = Quantity(345, "MPa")
    
    manufacturer: str = "Bechtel Corporation"
    manufacturing_technique: str = "Steel-plate composite (SC) modules with factory-installed reinforcement"
    quality_control: str = "Continuous monitoring during concrete pouring and non-destructive testing of welds"

# Initialize parameter instances
CORE_MATERIALS = CoreMaterials()
VESSEL_MATERIALS = PressureVesselMaterials()
STEAM_GENERATOR_MATERIALS = SteamGeneratorMaterials()
CONTAINMENT_MATERIALS = ContainmentMaterials()

print("Material parameters initialized")
