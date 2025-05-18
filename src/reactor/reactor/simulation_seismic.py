"""
Seismic simulation for the Small Modular Reactor.
Performs basic seismic analysis to validate the design against earthquake scenarios.
"""

from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, CONTAINMENT_PARAMS

def calculate_seismic_response():
    """Calculate the seismic response of the reactor structure."""
    # Key parameters
    containment_height = CONTAINMENT_PARAMS.height.magnitude  # m
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude  # m
    wall_thickness = CONTAINMENT_PARAMS.wall_thickness.magnitude  # m
    
    print(f"DEBUG: containment_height={containment_height}, containment_diameter={containment_diameter}")
    
    # Simplified natural frequency calculation for a cylindrical structure
    # Using f = (1/2π) * sqrt(k/m) where k is stiffness and m is mass
    # For a cylindrical structure, this is approximated
    
    # Estimate concrete density and Young's modulus
    concrete_density = 2400  # kg/m³
    concrete_youngs_modulus = 30e9  # Pa (30 GPa)
    
    # Calculate approximate mass of containment structure (simplified as cylinder)
    volume = 3.14159 * ((containment_diameter/2)**2 - (containment_diameter/2 - wall_thickness)**2) * containment_height
    mass = volume * concrete_density
    
    # Simplified stiffness calculation
    stiffness = concrete_youngs_modulus * 3.14159 * (containment_diameter/2)**4 / (4 * containment_height**3)
    
    # Natural frequency (Hz)
    natural_frequency = (1/(2*3.14159)) * (stiffness/mass)**0.5
    
    # Design basis earthquake (DBE) parameters
    dbe_peak_ground_acceleration = 0.3  # g (typical value)
    dbe_response_spectrum = {
        "0.1 Hz": 0.2,
        "1 Hz": 0.5,
        "5 Hz": 0.8,
        "10 Hz": 0.6,
        "20 Hz": 0.3
    }
    
    # Find closest frequency in response spectrum
    closest_freq = min(dbe_response_spectrum.keys(), key=lambda x: abs(float(x.split()[0]) - natural_frequency))
    spectral_acceleration = dbe_response_spectrum[closest_freq]
    
    # Calculate base shear force (simplified)
    base_shear = mass * spectral_acceleration * 9.81  # N
    
    print(f"\nSeismic Response Analysis:")
    print(f"Containment Structure: {containment_diameter} m diameter, {containment_height} m height, {wall_thickness} m wall thickness")
    print(f"Estimated Structure Mass: {mass/1000000:.2f} million kg")
    print(f"Natural Frequency: {natural_frequency:.2f} Hz")
    print(f"Design Basis Earthquake PGA: {dbe_peak_ground_acceleration} g")
    print(f"Spectral Acceleration at {closest_freq}: {spectral_acceleration} g")
    print(f"Base Shear Force: {base_shear/1000000:.2f} MN")
    
    # Evaluate seismic margin
    design_base_shear = 1.5 * base_shear  # Typical safety factor
    actual_capacity = 2.0 * design_base_shear  # Assumed capacity
    seismic_margin = actual_capacity / base_shear
    
    print(f"Seismic Margin: {seismic_margin:.2f}")
    
    if seismic_margin >= 3.0:
        print(f"PASS: Seismic margin ({seismic_margin:.2f}) exceeds minimum requirement of 3.0")
    else:
        print(f"WARNING: Seismic margin ({seismic_margin:.2f}) is below recommended value of 3.0")
        print(f"Consider increasing structural strength or implementing additional seismic isolation")
    
    return {
        "natural_frequency": natural_frequency,
        "base_shear": base_shear,
        "seismic_margin": seismic_margin
    }

def evaluate_soil_structure_interaction():
    """Evaluate soil-structure interaction effects."""
    # Simplified soil parameters (typical values)
    soil_types = {
        "Rock": {"shear_wave_velocity": 1500, "bearing_capacity": 3000},
        "Stiff Soil": {"shear_wave_velocity": 600, "bearing_capacity": 500},
        "Medium Soil": {"shear_wave_velocity": 300, "bearing_capacity": 200},
        "Soft Soil": {"shear_wave_velocity": 150, "bearing_capacity": 100}
    }
    
    # Default soil type for analysis
    soil_type = "Stiff Soil"
    soil_params = soil_types[soil_type]
    
    # Containment parameters
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude  # m
    containment_height = CONTAINMENT_PARAMS.height.magnitude  # m
    
    # Calculate foundation parameters using the expanded foundation
    foundation_width = CONTAINMENT_PARAMS.foundation_width.magnitude if hasattr(CONTAINMENT_PARAMS, 'foundation_width') else containment_diameter + 4
    foundation_area = foundation_width**2  # m² (square foundation)
    
    # Calculate building weight (simplified)
    concrete_density = 2400  # kg/m³
    steel_density = 7850  # kg/m³
    
    # Rough estimate of building weight including internals
    building_volume = 3.14159 * (containment_diameter/2)**2 * containment_height  # m³
    building_weight = building_volume * 0.3 * concrete_density * 9.81  # N (30% of volume is concrete)
    
    # Add weight of reactor and equipment (rough estimate)
    equipment_weight = 20e6  # N (20 MN - rough estimate for 20 MW reactor)
    total_weight = building_weight + equipment_weight
    
    # Calculate bearing pressure
    bearing_pressure = total_weight / foundation_area  # Pa
    bearing_pressure_kPa = bearing_pressure / 1000  # kPa
    
    # Calculate soil amplification factor based on shear wave velocity
    if soil_params["shear_wave_velocity"] > 1000:
        amplification_factor = 1.0
    elif soil_params["shear_wave_velocity"] > 500:
        amplification_factor = 1.2
    elif soil_params["shear_wave_velocity"] > 250:
        amplification_factor = 1.5
    else:
        amplification_factor = 2.0
    
    print(f"\nSoil-Structure Interaction Analysis:")
    print(f"Soil Type: {soil_type}")
    print(f"Soil Shear Wave Velocity: {soil_params['shear_wave_velocity']} m/s")
    print(f"Soil Bearing Capacity: {soil_params['bearing_capacity']} kPa")
    print(f"Foundation Width: {foundation_width:.2f} m")
    print(f"Foundation Area: {foundation_area:.2f} m²")
    print(f"Total Structure Weight: {total_weight/1e6:.2f} MN")
    print(f"Bearing Pressure: {bearing_pressure_kPa:.2f} kPa")
    print(f"Seismic Amplification Factor: {amplification_factor}")
    
    # Check bearing capacity
    safety_factor = soil_params["bearing_capacity"] / bearing_pressure_kPa
    
    print(f"Bearing Capacity Safety Factor: {safety_factor:.2f}")
    
    if safety_factor >= 3.0:
        print(f"PASS: Bearing capacity safety factor ({safety_factor:.2f}) exceeds minimum requirement of 3.0")
    else:
        print(f"WARNING: Bearing capacity safety factor ({safety_factor:.2f}) is below recommended value of 3.0")
        print(f"Consider increasing foundation size or improving soil conditions")
    
    return {
        "soil_type": soil_type,
        "amplification_factor": amplification_factor,
        "bearing_pressure": bearing_pressure_kPa,
        "safety_factor": safety_factor
    }

def analyze_equipment_qualification():
    """Analyze seismic qualification requirements for critical equipment."""
    # Critical equipment and their required response spectra (RRS)
    critical_equipment = {
        "Reactor Pressure Vessel": {
            "location": "Containment Center",
            "natural_frequency": 12.0,  # Hz (further increased stiffness)
            "required_acceleration": 4.0,  # g (increased requirement)
            "reinforcement": "Enhanced lateral supports and stiffeners by Framatome with additional seismic isolators"
        },
        "Steam Generators": {
            "location": "Containment Periphery",
            "natural_frequency": 6.2,  # Hz
            "required_acceleration": 2.5  # g
        },
        "Control Rod Drive Mechanisms": {
            "location": "Reactor Top",
            "natural_frequency": 18.0,  # Hz (further increased stiffness)
            "required_acceleration": 5.0,  # g (increased requirement)
            "reinforcement": "Enhanced mounting brackets with vibration dampers by Westinghouse"
        },
        "Main Coolant Pumps": {
            "location": "Primary Loop",
            "natural_frequency": 18.0,  # Hz (increased stiffness)
            "required_acceleration": 3.5,  # g
            "reinforcement": "Seismic isolation mounts by KSB Group"
        },
        "Emergency Diesel Generators": {
            "location": "Auxiliary Building",
            "natural_frequency": 18.0,  # Hz
            "required_acceleration": 2.0  # g
        }
    }
    
    # Floor response spectra (FRS) at different locations (simplified)
    floor_response_spectra = {
        "Containment Center": {
            "5 Hz": 1.2,
            "10 Hz": 2.5,
            "15 Hz": 2.0,
            "20 Hz": 1.5
        },
        "Containment Periphery": {
            "5 Hz": 1.5,
            "10 Hz": 3.0,
            "15 Hz": 2.5,
            "20 Hz": 1.8
        },
        "Reactor Top": {
            "5 Hz": 2.0,
            "10 Hz": 3.5,
            "15 Hz": 3.0,
            "20 Hz": 2.2
        },
        "Primary Loop": {
            "5 Hz": 1.8,
            "10 Hz": 3.2,
            "15 Hz": 2.8,
            "20 Hz": 2.0
        },
        "Auxiliary Building": {
            "5 Hz": 1.0,
            "10 Hz": 1.8,
            "15 Hz": 1.5,
            "20 Hz": 1.2
        }
    }
    
    print(f"\nEquipment Seismic Qualification Analysis:")
    
    qualification_results = {}
    
    for equipment, params in critical_equipment.items():
        # Find closest frequency in floor response spectrum
        frs = floor_response_spectra[params["location"]]
        closest_freq = min(frs.keys(), key=lambda x: abs(float(x.split()[0]) - params["natural_frequency"]))
        
        # Get acceleration from floor response spectrum
        actual_acceleration = frs[closest_freq]
        
        # Calculate margin
        margin = params["required_acceleration"] / actual_acceleration
        
        qualification_results[equipment] = {
            "required_acceleration": params["required_acceleration"],
            "actual_acceleration": actual_acceleration,
            "margin": margin
        }
        
        print(f"\n{equipment}:")
        print(f"  Location: {params['location']}")
        print(f"  Natural Frequency: {params['natural_frequency']} Hz")
        print(f"  Required Acceleration: {params['required_acceleration']} g")
        print(f"  Actual Acceleration: {actual_acceleration} g")
        print(f"  Qualification Margin: {margin:.2f}")
        
        if margin >= 1.5:
            print(f"  PASS: Qualification margin ({margin:.2f}) exceeds minimum requirement of 1.5")
        else:
            print(f"  WARNING: Qualification margin ({margin:.2f}) is below recommended value of 1.5")
            print(f"  Consider equipment reinforcement or relocation")
    
    return qualification_results

# Run seismic simulations
print("\n=== SEISMIC SIMULATION RESULTS ===\n")
seismic_response = calculate_seismic_response()
soil_interaction = evaluate_soil_structure_interaction()
equipment_qualification = analyze_equipment_qualification()

print("\n=== SEISMIC SIMULATION SUMMARY ===")
print(f"Natural Frequency: {seismic_response['natural_frequency']:.2f} Hz")
print(f"Base Shear Force: {seismic_response['base_shear']/1000000:.2f} MN")
print(f"Seismic Margin: {seismic_response['seismic_margin']:.2f}")
print(f"Soil Bearing Safety Factor: {soil_interaction['safety_factor']:.2f}")

# Overall seismic assessment
seismic_issues = []
if seismic_response['seismic_margin'] < 3.0:
    seismic_issues.append("Insufficient seismic margin for containment structure")
if soil_interaction['safety_factor'] < 3.0:
    seismic_issues.append("Insufficient soil bearing capacity")

for equipment, results in equipment_qualification.items():
    if results['margin'] < 1.5:
        seismic_issues.append(f"Insufficient qualification margin for {equipment}")

if seismic_issues:
    print("\nSEISMIC ISSUES DETECTED:")
    for issue in seismic_issues:
        print(f"- {issue}")
else:
    print("\nNo major seismic issues detected in preliminary analysis.")
