"""
Seismic analysis for the small modular reactor.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
import numpy as np
import math

def calculate_seismic_response(peak_ground_acceleration):
    """
    Calculate the seismic response of the reactor building and components.
    
    Args:
        peak_ground_acceleration: Peak ground acceleration in g
        
    Returns:
        Dictionary with seismic response metrics
    """
    # Design basis earthquake
    design_basis = SAFETY_PARAMS.seismic_design_basis.magnitude  # g
    
    # Safety factor
    safety_factor = design_basis / peak_ground_acceleration if peak_ground_acceleration > 0 else float('inf')
    
    # Simplified spectral acceleration calculation
    # Using typical nuclear power plant response spectrum
    freq_range = np.linspace(1, 33, 100)  # Hz
    damping = 0.05  # 5% damping
    
    # Calculate spectral acceleration using simplified model
    spectral_acc = []
    for freq in freq_range:
        if freq < 2.5:
            sa = peak_ground_acceleration * (0.5 + 0.3 * freq)
        elif freq < 9:
            sa = peak_ground_acceleration * 1.25
        else:
            sa = peak_ground_acceleration * 1.25 * (9/freq)**0.75
        spectral_acc.append(sa)
    
    # Maximum spectral acceleration
    max_spectral_acc = max(spectral_acc)
    
    # Calculate building response
    building_height = 25  # m (estimated containment height)
    building_width = 15   # m (estimated containment diameter)
    
    # Simplified calculation of fundamental frequency
    # For reinforced concrete structures: f ≈ 10/H for H in meters
    fundamental_freq = 10 / building_height  # Hz
    
    # Find spectral acceleration at fundamental frequency
    idx = np.argmin(np.abs(freq_range - fundamental_freq))
    building_spectral_acc = spectral_acc[idx]
    
    # Simplified base shear calculation
    building_mass = 15000  # tons (estimated)
    base_shear = building_mass * 9.81 * building_spectral_acc  # kN
    
    # Equipment response - using peak floor acceleration
    # Simplified amplification factor for equipment
    floor_amplification = 1.5
    equipment_amplification = 2.0
    peak_equipment_acc = peak_ground_acceleration * floor_amplification * equipment_amplification
    
    return {
        "safety_factor": safety_factor,
        "max_spectral_acceleration": max_spectral_acc,
        "building_fundamental_frequency": fundamental_freq,
        "building_spectral_acceleration": building_spectral_acc,
        "base_shear": base_shear / 1000,  # MN
        "peak_equipment_acceleration": peak_equipment_acc
    }

def evaluate_seismic_margins():
    """
    Evaluate seismic margins for critical components.
    
    Returns:
        Dictionary with seismic margin assessment
    """
    # High Confidence of Low Probability of Failure (HCLPF) capacities
    # These are typical values for nuclear components in g
    hclpf_capacities = {
        "Reactor Pressure Vessel": 0.5,
        "Steam Generator": 0.45,
        "Primary Piping": 0.6,
        "Control Rod Drive": 0.4,
        "Diesel Generator": 0.35,
        "Battery Rack": 0.3,
        "Electrical Cabinet": 0.25,
        "Containment Structure": 0.7
    }
    
    # Design basis earthquake
    design_basis = SAFETY_PARAMS.seismic_design_basis.magnitude  # g
    
    # Calculate seismic margins
    margins = {}
    for component, capacity in hclpf_capacities.items():
        margins[component] = capacity / design_basis
    
    # Identify limiting components
    limiting_component = min(margins, key=margins.get)
    limiting_margin = margins[limiting_component]
    
    # Calculate plant-level HCLPF
    plant_hclpf = design_basis * limiting_margin
    
    return {
        "component_margins": margins,
        "limiting_component": limiting_component,
        "limiting_margin": limiting_margin,
        "plant_hclpf": plant_hclpf
    }

def calculate_soil_structure_interaction():
    """
    Calculate simplified soil-structure interaction effects.
    
    Returns:
        Dictionary with soil-structure interaction metrics
    """
    # Assumed soil properties
    soil_shear_wave_velocity = 500  # m/s (medium stiff soil)
    soil_density = 1800  # kg/m³
    
    # Building properties
    building_height = 25  # m
    building_width = 15   # m
    building_mass = 15000 * 1000  # kg
    
    # Calculate soil stiffness (simplified)
    soil_shear_modulus = soil_density * soil_shear_wave_velocity**2
    soil_stiffness = soil_shear_modulus * building_width  # N/m
    
    # Calculate fixed-base frequency
    fixed_base_freq = 10 / building_height  # Hz
    
    # Calculate SSI frequency
    building_stiffness = (2 * math.pi * fixed_base_freq)**2 * building_mass
    effective_stiffness = (1/building_stiffness + 1/soil_stiffness)**(-1)
    ssi_freq = (1/(2*math.pi)) * math.sqrt(effective_stiffness/building_mass)
    
    # Calculate frequency shift
    freq_shift = (fixed_base_freq - ssi_freq) / fixed_base_freq * 100
    
    return {
        "fixed_base_frequency": fixed_base_freq,
        "ssi_frequency": ssi_freq,
        "frequency_shift_percent": freq_shift,
        "soil_stiffness": soil_stiffness / 1e9  # GN/m
    }

# Run seismic analysis
design_basis = SAFETY_PARAMS.seismic_design_basis.magnitude
seismic_response = calculate_seismic_response(design_basis)
seismic_margins = evaluate_seismic_margins()
ssi_effects = calculate_soil_structure_interaction()

print(f"Seismic design basis: {design_basis} g")
print(f"Building fundamental frequency: {seismic_response['building_fundamental_frequency']:.2f} Hz")
print(f"Base shear at design basis: {seismic_response['base_shear']:.2f} MN")
print(f"Limiting seismic component: {seismic_margins['limiting_component']} with margin {seismic_margins['limiting_margin']:.2f}")
print(f"Plant HCLPF capacity: {seismic_margins['plant_hclpf']:.2f} g")
print(f"Soil-structure interaction frequency shift: {ssi_effects['frequency_shift_percent']:.2f}%")
