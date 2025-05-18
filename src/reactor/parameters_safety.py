from pyforge import Parameters, Quantity

class SafetyParameters(Parameters):
    """Define all the key parameters for safety systems."""
    # Containment parameters
    containment_type: str = "Steel-lined reinforced concrete"
    containment_thickness: Quantity = Quantity(1.2, "m")
    containment_design_pressure: Quantity = Quantity(0.4, "MPa")
    
    # Emergency cooling systems
    eccs_type: str = "Passive safety injection system"
    eccs_water_volume: Quantity = Quantity(800, "m^3")
    eccs_activation_time: Quantity = Quantity(30, "s")
    
    # Decay heat removal
    passive_cooling_capacity: Quantity = Quantity(3, "MW")
    passive_cooling_duration: Quantity = Quantity(72, "hour")
    
    # Radiation protection
    radiation_shield_material: str = "Borated concrete"
    radiation_shield_thickness: Quantity = Quantity(2, "m")
    max_worker_dose: Quantity = Quantity(20, "mSv/year")
    
    # Seismic design
    seismic_design_basis: Quantity = Quantity(0.3, "g")
    
    # Redundancy
    safety_train_redundancy: int = 3  # N+2 redundancy

# single source of truth
SAFETY_PARAMS = SafetyParameters()

print(f"Safety parameters loaded: {SAFETY_PARAMS.containment_type} containment with {SAFETY_PARAMS.eccs_type}")
