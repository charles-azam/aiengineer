"""
Manufacturing analysis tools for the Small Modular Reactor project.
Provides functions to analyze manufacturability, supply chain, and production costs.
"""

print("Loading tools_manufacturing module")
from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS, CONTAINMENT_PARAMS

def analyze_manufacturability():
    """
    Analyze the manufacturability of key SMR components.
    Returns a dictionary with manufacturability assessments and specific manufacturing techniques.
    """
    print("\nPerforming detailed manufacturability analysis...")
    # Reactor vessel manufacturability
    vessel_diameter = PRIMARY_LOOP_PARAMS.vessel_diameter.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_diameter') else 3.0
    vessel_height = PRIMARY_LOOP_PARAMS.vessel_height.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_height') else 7.5
    
    # Check if vessel can be transported by road
    road_transportable = vessel_diameter <= 4.5  # Standard oversize load limit
    
    # Check if vessel can be manufactured in standard facilities
    standard_manufacturing = vessel_diameter <= 5.0 and vessel_height <= 12.0
    
    # Steam generator manufacturability
    sg_type = PRIMARY_LOOP_PARAMS.heat_exchanger_type
    sg_material = PRIMARY_LOOP_PARAMS.heat_exchanger_material
    
    # Assess manufacturing complexity
    if sg_type == "Shell and Tube":
        sg_complexity = "Medium"
        sg_automation = "High - automated tube insertion and welding"
    elif sg_type == "Helical Coil":
        sg_complexity = "High"
        sg_automation = "Medium - specialized coil winding equipment required"
    else:
        sg_complexity = "Unknown"
        sg_automation = "Unknown"
    
    # Containment manufacturability
    containment_type = CONTAINMENT_PARAMS.containment_type
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude
    
    # Assess if containment can be prefabricated
    if containment_diameter <= 10.0:
        containment_prefab = "Fully prefabricable in sections"
    elif containment_diameter <= 20.0:
        containment_prefab = "Partially prefabricable with on-site assembly"
    else:
        containment_prefab = "Primarily on-site construction required"
    
    # Compile results
    results = {
        "reactor_vessel": {
            "road_transportable": road_transportable,
            "standard_manufacturing": standard_manufacturing,
            "recommended_manufacturer": "Doosan Heavy Industries or Japan Steel Works",
            "manufacturing_process": "Forging and machining with automated welding",
            "material_specification": "SA-508 Grade 3 Class 1 with 308L/309L stainless steel cladding",
            "quality_control": "100% volumetric examination with phased array ultrasonic testing",
            "seismic_reinforcement": "Integrated support lugs with enhanced stiffness by Framatome"
        },
        "steam_generator": {
            "complexity": sg_complexity,
            "automation_potential": sg_automation,
            "recommended_manufacturer": "Babcock & Wilcox or Framatome",
            "special_tooling": "Custom tube sheet drilling fixtures and automated welding systems",
            "manufacturing_technique": "Precision CNC machining with robotic welding and automated inspection"
        },
        "containment": {
            "prefabrication": containment_prefab,
            "recommended_approach": "Modular steel-concrete composite construction",
            "recommended_contractor": "Bechtel Corporation or Fluor Corporation",
            "special_considerations": "Precision alignment of prefabricated sections",
            "construction_technique": "Steel-plate composite (SC) modules with factory-installed reinforcement"
        }
    }
    
    # Print analysis results
    print("\n=== MANUFACTURABILITY ANALYSIS ===")
    print(f"Reactor Vessel: {'Road transportable' if road_transportable else 'Requires special transportation'}")
    print(f"Steam Generator: {sg_complexity} complexity, {sg_automation}")
    print(f"Containment: {containment_prefab}")
    
    return results

def estimate_manufacturing_timeline():
    """
    Estimate manufacturing and construction timeline for the SMR.
    Returns a dictionary with timeline estimates.
    """
    # Base manufacturing times (in months)
    vessel_manufacturing = 12
    steam_generator_manufacturing = 8
    turbine_manufacturing = 10
    containment_construction = 18
    
    # Adjust based on design complexity
    power = REACTOR_PARAMS.electrical_power.magnitude
    if power <= 10:
        complexity_factor = 0.8
    elif power <= 30:
        complexity_factor = 1.0
    else:
        complexity_factor = 1.2
    
    # Calculate adjusted times
    vessel_time = vessel_manufacturing * complexity_factor
    sg_time = steam_generator_manufacturing * complexity_factor
    turbine_time = turbine_manufacturing * complexity_factor
    containment_time = containment_construction * complexity_factor
    
    # Calculate critical path and total time
    long_lead_items = max(vessel_time, sg_time, turbine_time)
    site_prep_time = 6
    installation_time = 12
    testing_time = 6
    
    # Total project timeline
    total_time = site_prep_time + max(long_lead_items, containment_time) + installation_time + testing_time
    
    # Compile timeline
    timeline = {
        "long_lead_items": {
            "reactor_vessel": vessel_time,
            "steam_generators": sg_time,
            "turbine_generator": turbine_time
        },
        "construction": {
            "site_preparation": site_prep_time,
            "containment": containment_time,
            "installation": installation_time,
            "testing_commissioning": testing_time
        },
        "total_project_time": total_time
    }
    
    # Print timeline
    print("\n=== MANUFACTURING TIMELINE ===")
    print(f"Long Lead Items:")
    print(f"  - Reactor Vessel: {vessel_time:.1f} months")
    print(f"  - Steam Generators: {sg_time:.1f} months")
    print(f"  - Turbine Generator: {turbine_time:.1f} months")
    print(f"Construction:")
    print(f"  - Site Preparation: {site_prep_time} months")
    print(f"  - Containment: {containment_time:.1f} months")
    print(f"  - Installation: {installation_time} months")
    print(f"  - Testing & Commissioning: {testing_time} months")
    print(f"Total Project Timeline: {total_time:.1f} months ({total_time/12:.1f} years)")
    
    return timeline

def analyze_supply_chain():
    """
    Analyze the supply chain for key SMR components.
    Identifies critical suppliers and potential bottlenecks.
    """
    # Key components and their suppliers
    key_components = {
        "Reactor Pressure Vessel": {
            "suppliers": ["Doosan Heavy Industries (South Korea)", "Japan Steel Works (Japan)", "Framatome (France)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "Medium - Limited number of qualified manufacturers"
        },
        "Steam Generators": {
            "suppliers": ["Babcock & Wilcox (USA)", "Framatome (France)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple qualified suppliers"
        },
        "Control Rod Drive Mechanisms": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "SKODA JS (Czech Republic)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Medium - Specialized components"
        },
        "Reactor Coolant Pumps": {
            "suppliers": ["KSB Group (Germany)", "Curtiss-Wright (USA)", "Flowserve (USA)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple suppliers"
        },
        "Digital Control Systems": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Lockheed Martin (USA)"],
            "lead_time": "6-10 months",
            "bottleneck_risk": "Medium - Qualification and licensing requirements"
        },
        "Turbine Generator": {
            "suppliers": ["General Electric (USA)", "Siemens (Germany)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Low - Standard technology"
        },
        "Fuel Assemblies": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Global Nuclear Fuel (USA)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "High - Limited HALEU supply chain"
        }
    }
    
    # Identify critical path items
    critical_path = []
    for component, data in key_components.items():
        if "High" in data["bottleneck_risk"]:
            critical_path.append(component)
    
    # Print supply chain analysis
    print("\n=== SUPPLY CHAIN ANALYSIS ===")
    print("Critical Components:")
    for component in critical_path:
        data = key_components[component]
        print(f"  - {component}: {data['bottleneck_risk']}")
        print(f"    Suppliers: {', '.join(data['suppliers'])}")
        print(f"    Lead Time: {data['lead_time']}")
    
    print("\nSupply Chain Recommendations:")
    if "Fuel Assemblies" in critical_path:
        print("  - Secure HALEU supply through long-term contracts with multiple suppliers")
    if "Reactor Pressure Vessel" in critical_path:
        print("  - Place early orders for reactor pressure vessel to secure manufacturing slot")
    print("  - Develop qualification program for alternative suppliers to reduce bottleneck risks")
    print("  - Implement digital supply chain tracking system to monitor critical components")
    
    return {
        "components": key_components,
        "critical_path": critical_path
    }

# Run manufacturing analysis when imported
if __name__ != "__main__":  # This ensures it runs when imported but not when executed directly
    print("Initializing manufacturing analysis tools")
    manufacturability = analyze_manufacturability()
    timeline = estimate_manufacturing_timeline()
    supply_chain = analyze_supply_chain()
"""
Manufacturing analysis tools for the Small Modular Reactor project.
Provides functions to analyze manufacturability, supply chain, and production costs.
"""

print("Loading tools_manufacturing module")
from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS, CONTAINMENT_PARAMS

def analyze_manufacturability():
    """
    Analyze the manufacturability of key SMR components.
    Returns a dictionary with manufacturability assessments and specific manufacturing techniques.
    """
    print("\nPerforming detailed manufacturability analysis...")
    # Reactor vessel manufacturability
    vessel_diameter = PRIMARY_LOOP_PARAMS.vessel_diameter.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_diameter') else 3.0
    vessel_height = PRIMARY_LOOP_PARAMS.vessel_height.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_height') else 7.5
    
    # Check if vessel can be transported by road
    road_transportable = vessel_diameter <= 4.5  # Standard oversize load limit
    
    # Check if vessel can be manufactured in standard facilities
    standard_manufacturing = vessel_diameter <= 5.0 and vessel_height <= 12.0
    
    # Steam generator manufacturability
    sg_type = PRIMARY_LOOP_PARAMS.heat_exchanger_type
    sg_material = PRIMARY_LOOP_PARAMS.heat_exchanger_material
    
    # Assess manufacturing complexity
    if sg_type == "Shell and Tube":
        sg_complexity = "Medium"
        sg_automation = "High - automated tube insertion and welding"
    elif sg_type == "Helical Coil":
        sg_complexity = "High"
        sg_automation = "Medium - specialized coil winding equipment required"
    else:
        sg_complexity = "Unknown"
        sg_automation = "Unknown"
    
    # Containment manufacturability
    containment_type = CONTAINMENT_PARAMS.containment_type
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude
    
    # Assess if containment can be prefabricated
    if containment_diameter <= 10.0:
        containment_prefab = "Fully prefabricable in sections"
    elif containment_diameter <= 20.0:
        containment_prefab = "Partially prefabricable with on-site assembly"
    else:
        containment_prefab = "Primarily on-site construction required"
    
    # Compile results
    results = {
        "reactor_vessel": {
            "road_transportable": road_transportable,
            "standard_manufacturing": standard_manufacturing,
            "recommended_manufacturer": "Doosan Heavy Industries or Japan Steel Works",
            "manufacturing_process": "Forging and machining with automated welding",
            "material_specification": "SA-508 Grade 3 Class 1 with 308L/309L stainless steel cladding",
            "quality_control": "100% volumetric examination with phased array ultrasonic testing",
            "seismic_reinforcement": "Integrated support lugs with enhanced stiffness by Framatome"
        },
        "steam_generator": {
            "complexity": sg_complexity,
            "automation_potential": sg_automation,
            "recommended_manufacturer": "Babcock & Wilcox or Framatome",
            "special_tooling": "Custom tube sheet drilling fixtures and automated welding systems",
            "manufacturing_technique": "Precision CNC machining with robotic welding and automated inspection"
        },
        "containment": {
            "prefabrication": containment_prefab,
            "recommended_approach": "Modular steel-concrete composite construction",
            "recommended_contractor": "Bechtel Corporation or Fluor Corporation",
            "special_considerations": "Precision alignment of prefabricated sections",
            "construction_technique": "Steel-plate composite (SC) modules with factory-installed reinforcement"
        }
    }
    
    # Print analysis results
    print("\n=== MANUFACTURABILITY ANALYSIS ===")
    print(f"Reactor Vessel: {'Road transportable' if road_transportable else 'Requires special transportation'}")
    print(f"Steam Generator: {sg_complexity} complexity, {sg_automation}")
    print(f"Containment: {containment_prefab}")
    
    return results

def estimate_manufacturing_timeline():
    """
    Estimate manufacturing and construction timeline for the SMR.
    Returns a dictionary with timeline estimates.
    """
    # Base manufacturing times (in months)
    vessel_manufacturing = 12
    steam_generator_manufacturing = 8
    turbine_manufacturing = 10
    containment_construction = 18
    
    # Adjust based on design complexity
    power = REACTOR_PARAMS.electrical_power.magnitude
    if power <= 10:
        complexity_factor = 0.8
    elif power <= 30:
        complexity_factor = 1.0
    else:
        complexity_factor = 1.2
    
    # Calculate adjusted times
    vessel_time = vessel_manufacturing * complexity_factor
    sg_time = steam_generator_manufacturing * complexity_factor
    turbine_time = turbine_manufacturing * complexity_factor
    containment_time = containment_construction * complexity_factor
    
    # Calculate critical path and total time
    long_lead_items = max(vessel_time, sg_time, turbine_time)
    site_prep_time = 6
    installation_time = 12
    testing_time = 6
    
    # Total project timeline
    total_time = site_prep_time + max(long_lead_items, containment_time) + installation_time + testing_time
    
    # Compile timeline
    timeline = {
        "long_lead_items": {
            "reactor_vessel": vessel_time,
            "steam_generators": sg_time,
            "turbine_generator": turbine_time
        },
        "construction": {
            "site_preparation": site_prep_time,
            "containment": containment_time,
            "installation": installation_time,
            "testing_commissioning": testing_time
        },
        "total_project_time": total_time
    }
    
    # Print timeline
    print("\n=== MANUFACTURING TIMELINE ===")
    print(f"Long Lead Items:")
    print(f"  - Reactor Vessel: {vessel_time:.1f} months")
    print(f"  - Steam Generators: {sg_time:.1f} months")
    print(f"  - Turbine Generator: {turbine_time:.1f} months")
    print(f"Construction:")
    print(f"  - Site Preparation: {site_prep_time} months")
    print(f"  - Containment: {containment_time:.1f} months")
    print(f"  - Installation: {installation_time} months")
    print(f"  - Testing & Commissioning: {testing_time} months")
    print(f"Total Project Timeline: {total_time:.1f} months ({total_time/12:.1f} years)")
    
    return timeline

def analyze_supply_chain():
    """
    Analyze the supply chain for key SMR components.
    Identifies critical suppliers and potential bottlenecks.
    """
    # Key components and their suppliers
    key_components = {
        "Reactor Pressure Vessel": {
            "suppliers": ["Doosan Heavy Industries (South Korea)", "Japan Steel Works (Japan)", "Framatome (France)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "Medium - Limited number of qualified manufacturers"
        },
        "Steam Generators": {
            "suppliers": ["Babcock & Wilcox (USA)", "Framatome (France)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple qualified suppliers"
        },
        "Control Rod Drive Mechanisms": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "SKODA JS (Czech Republic)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Medium - Specialized components"
        },
        "Reactor Coolant Pumps": {
            "suppliers": ["KSB Group (Germany)", "Curtiss-Wright (USA)", "Flowserve (USA)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple suppliers"
        },
        "Digital Control Systems": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Lockheed Martin (USA)"],
            "lead_time": "6-10 months",
            "bottleneck_risk": "Medium - Qualification and licensing requirements"
        },
        "Turbine Generator": {
            "suppliers": ["General Electric (USA)", "Siemens (Germany)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Low - Standard technology"
        },
        "Fuel Assemblies": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Global Nuclear Fuel (USA)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "High - Limited HALEU supply chain"
        }
    }
    
    # Identify critical path items
    critical_path = []
    for component, data in key_components.items():
        if "High" in data["bottleneck_risk"]:
            critical_path.append(component)
    
    # Print supply chain analysis
    print("\n=== SUPPLY CHAIN ANALYSIS ===")
    print("Critical Components:")
    for component in critical_path:
        data = key_components[component]
        print(f"  - {component}: {data['bottleneck_risk']}")
        print(f"    Suppliers: {', '.join(data['suppliers'])}")
        print(f"    Lead Time: {data['lead_time']}")
    
    print("\nSupply Chain Recommendations:")
    if "Fuel Assemblies" in critical_path:
        print("  - Secure HALEU supply through long-term contracts with multiple suppliers")
    if "Reactor Pressure Vessel" in critical_path:
        print("  - Place early orders for reactor pressure vessel to secure manufacturing slot")
    print("  - Develop qualification program for alternative suppliers to reduce bottleneck risks")
    print("  - Implement digital supply chain tracking system to monitor critical components")
    
    return {
        "components": key_components,
        "critical_path": critical_path
    }

# Run manufacturing analysis when imported
if __name__ != "__main__":  # This ensures it runs when imported but not when executed directly
    print("Initializing manufacturing analysis tools")
    manufacturability = analyze_manufacturability()
    timeline = estimate_manufacturing_timeline()
    supply_chain = analyze_supply_chain()
"""
Manufacturing analysis tools for the Small Modular Reactor project.
Provides functions to analyze manufacturability, supply chain, and production costs.
"""

print("Loading tools_manufacturing module")
from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS, CONTAINMENT_PARAMS

def analyze_manufacturability():
    """
    Analyze the manufacturability of key SMR components.
    Returns a dictionary with manufacturability assessments.
    """
    # Reactor vessel manufacturability
    vessel_diameter = PRIMARY_LOOP_PARAMS.vessel_diameter.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_diameter') else 3.0
    vessel_height = PRIMARY_LOOP_PARAMS.vessel_height.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_height') else 7.5
    
    # Check if vessel can be transported by road
    road_transportable = vessel_diameter <= 4.5  # Standard oversize load limit
    
    # Check if vessel can be manufactured in standard facilities
    standard_manufacturing = vessel_diameter <= 5.0 and vessel_height <= 12.0
    
    # Steam generator manufacturability
    sg_type = PRIMARY_LOOP_PARAMS.heat_exchanger_type
    sg_material = PRIMARY_LOOP_PARAMS.heat_exchanger_material
    
    # Assess manufacturing complexity
    if sg_type == "Shell and Tube":
        sg_complexity = "Medium"
        sg_automation = "High - automated tube insertion and welding"
    elif sg_type == "Helical Coil":
        sg_complexity = "High"
        sg_automation = "Medium - specialized coil winding equipment required"
    else:
        sg_complexity = "Unknown"
        sg_automation = "Unknown"
    
    # Containment manufacturability
    containment_type = CONTAINMENT_PARAMS.containment_type
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude
    
    # Assess if containment can be prefabricated
    if containment_diameter <= 10.0:
        containment_prefab = "Fully prefabricable in sections"
    elif containment_diameter <= 20.0:
        containment_prefab = "Partially prefabricable with on-site assembly"
    else:
        containment_prefab = "Primarily on-site construction required"
    
    # Compile results
    results = {
        "reactor_vessel": {
            "road_transportable": road_transportable,
            "standard_manufacturing": standard_manufacturing,
            "recommended_manufacturer": "Doosan Heavy Industries or Japan Steel Works",
            "manufacturing_process": "Forging and machining with automated welding"
        },
        "steam_generator": {
            "complexity": sg_complexity,
            "automation_potential": sg_automation,
            "recommended_manufacturer": "Babcock & Wilcox or Framatome",
            "special_tooling": "Custom tube sheet drilling fixtures and automated welding systems"
        },
        "containment": {
            "prefabrication": containment_prefab,
            "recommended_approach": "Modular steel-concrete composite construction",
            "recommended_contractor": "Bechtel Corporation or Fluor Corporation",
            "special_considerations": "Precision alignment of prefabricated sections"
        }
    }
    
    # Print analysis results
    print("\n=== MANUFACTURABILITY ANALYSIS ===")
    print(f"Reactor Vessel: {'Road transportable' if road_transportable else 'Requires special transportation'}")
    print(f"Steam Generator: {sg_complexity} complexity, {sg_automation}")
    print(f"Containment: {containment_prefab}")
    
    return results

def estimate_manufacturing_timeline():
    """
    Estimate manufacturing and construction timeline for the SMR.
    Returns a dictionary with timeline estimates.
    """
    # Base manufacturing times (in months)
    vessel_manufacturing = 12
    steam_generator_manufacturing = 8
    turbine_manufacturing = 10
    containment_construction = 18
    
    # Adjust based on design complexity
    power = REACTOR_PARAMS.electrical_power.magnitude
    if power <= 10:
        complexity_factor = 0.8
    elif power <= 30:
        complexity_factor = 1.0
    else:
        complexity_factor = 1.2
    
    # Calculate adjusted times
    vessel_time = vessel_manufacturing * complexity_factor
    sg_time = steam_generator_manufacturing * complexity_factor
    turbine_time = turbine_manufacturing * complexity_factor
    containment_time = containment_construction * complexity_factor
    
    # Calculate critical path and total time
    long_lead_items = max(vessel_time, sg_time, turbine_time)
    site_prep_time = 6
    installation_time = 12
    testing_time = 6
    
    # Total project timeline
    total_time = site_prep_time + max(long_lead_items, containment_time) + installation_time + testing_time
    
    # Compile timeline
    timeline = {
        "long_lead_items": {
            "reactor_vessel": vessel_time,
            "steam_generators": sg_time,
            "turbine_generator": turbine_time
        },
        "construction": {
            "site_preparation": site_prep_time,
            "containment": containment_time,
            "installation": installation_time,
            "testing_commissioning": testing_time
        },
        "total_project_time": total_time
    }
    
    # Print timeline
    print("\n=== MANUFACTURING TIMELINE ===")
    print(f"Long Lead Items:")
    print(f"  - Reactor Vessel: {vessel_time:.1f} months")
    print(f"  - Steam Generators: {sg_time:.1f} months")
    print(f"  - Turbine Generator: {turbine_time:.1f} months")
    print(f"Construction:")
    print(f"  - Site Preparation: {site_prep_time} months")
    print(f"  - Containment: {containment_time:.1f} months")
    print(f"  - Installation: {installation_time} months")
    print(f"  - Testing & Commissioning: {testing_time} months")
    print(f"Total Project Timeline: {total_time:.1f} months ({total_time/12:.1f} years)")
    
    return timeline

def analyze_supply_chain():
    """
    Analyze the supply chain for key SMR components.
    Identifies critical suppliers and potential bottlenecks.
    """
    # Key components and their suppliers
    key_components = {
        "Reactor Pressure Vessel": {
            "suppliers": ["Doosan Heavy Industries (South Korea)", "Japan Steel Works (Japan)", "Framatome (France)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "Medium - Limited number of qualified manufacturers"
        },
        "Steam Generators": {
            "suppliers": ["Babcock & Wilcox (USA)", "Framatome (France)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple qualified suppliers"
        },
        "Control Rod Drive Mechanisms": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "SKODA JS (Czech Republic)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Medium - Specialized components"
        },
        "Reactor Coolant Pumps": {
            "suppliers": ["KSB Group (Germany)", "Curtiss-Wright (USA)", "Flowserve (USA)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple suppliers"
        },
        "Digital Control Systems": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Lockheed Martin (USA)"],
            "lead_time": "6-10 months",
            "bottleneck_risk": "Medium - Qualification and licensing requirements"
        },
        "Turbine Generator": {
            "suppliers": ["General Electric (USA)", "Siemens (Germany)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Low - Standard technology"
        },
        "Fuel Assemblies": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Global Nuclear Fuel (USA)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "High - Limited HALEU supply chain"
        }
    }
    
    # Identify critical path items
    critical_path = []
    for component, data in key_components.items():
        if "High" in data["bottleneck_risk"]:
            critical_path.append(component)
    
    # Print supply chain analysis
    print("\n=== SUPPLY CHAIN ANALYSIS ===")
    print("Critical Components:")
    for component in critical_path:
        data = key_components[component]
        print(f"  - {component}: {data['bottleneck_risk']}")
        print(f"    Suppliers: {', '.join(data['suppliers'])}")
        print(f"    Lead Time: {data['lead_time']}")
    
    print("\nSupply Chain Recommendations:")
    if "Fuel Assemblies" in critical_path:
        print("  - Secure HALEU supply through long-term contracts with multiple suppliers")
    if "Reactor Pressure Vessel" in critical_path:
        print("  - Place early orders for reactor pressure vessel to secure manufacturing slot")
    print("  - Develop qualification program for alternative suppliers to reduce bottleneck risks")
    print("  - Implement digital supply chain tracking system to monitor critical components")
    
    return {
        "components": key_components,
        "critical_path": critical_path
    }

# Run manufacturing analysis when imported
if __name__ != "__main__":  # This ensures it runs when imported but not when executed directly
    print("Initializing manufacturing analysis tools")
    manufacturability = analyze_manufacturability()
    timeline = estimate_manufacturing_timeline()
    supply_chain = analyze_supply_chain()
"""
Manufacturing analysis tools for the Small Modular Reactor project.
Provides functions to analyze manufacturability, supply chain, and production costs.
"""

print("Loading tools_manufacturing module")
from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS, CONTAINMENT_PARAMS

def analyze_manufacturability():
    """
    Analyze the manufacturability of key SMR components.
    Returns a dictionary with manufacturability assessments.
    """
    # Reactor vessel manufacturability
    vessel_diameter = PRIMARY_LOOP_PARAMS.vessel_diameter.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_diameter') else 3.0
    vessel_height = PRIMARY_LOOP_PARAMS.vessel_height.magnitude if hasattr(PRIMARY_LOOP_PARAMS, 'vessel_height') else 7.5
    
    # Check if vessel can be transported by road
    road_transportable = vessel_diameter <= 4.5  # Standard oversize load limit
    
    # Check if vessel can be manufactured in standard facilities
    standard_manufacturing = vessel_diameter <= 5.0 and vessel_height <= 12.0
    
    # Steam generator manufacturability
    sg_type = PRIMARY_LOOP_PARAMS.heat_exchanger_type
    sg_material = PRIMARY_LOOP_PARAMS.heat_exchanger_material
    
    # Assess manufacturing complexity
    if sg_type == "Shell and Tube":
        sg_complexity = "Medium"
        sg_automation = "High - automated tube insertion and welding"
    elif sg_type == "Helical Coil":
        sg_complexity = "High"
        sg_automation = "Medium - specialized coil winding equipment required"
    else:
        sg_complexity = "Unknown"
        sg_automation = "Unknown"
    
    # Containment manufacturability
    containment_type = CONTAINMENT_PARAMS.containment_type
    containment_diameter = CONTAINMENT_PARAMS.diameter.magnitude
    
    # Assess if containment can be prefabricated
    if containment_diameter <= 10.0:
        containment_prefab = "Fully prefabricable in sections"
    elif containment_diameter <= 20.0:
        containment_prefab = "Partially prefabricable with on-site assembly"
    else:
        containment_prefab = "Primarily on-site construction required"
    
    # Compile results
    results = {
        "reactor_vessel": {
            "road_transportable": road_transportable,
            "standard_manufacturing": standard_manufacturing,
            "recommended_manufacturer": "Doosan Heavy Industries or Japan Steel Works",
            "manufacturing_process": "Forging and machining with automated welding"
        },
        "steam_generator": {
            "complexity": sg_complexity,
            "automation_potential": sg_automation,
            "recommended_manufacturer": "Babcock & Wilcox or Framatome",
            "special_tooling": "Custom tube sheet drilling fixtures and automated welding systems"
        },
        "containment": {
            "prefabrication": containment_prefab,
            "recommended_approach": "Modular steel-concrete composite construction",
            "recommended_contractor": "Bechtel Corporation or Fluor Corporation",
            "special_considerations": "Precision alignment of prefabricated sections"
        }
    }
    
    # Print analysis results
    print("\n=== MANUFACTURABILITY ANALYSIS ===")
    print(f"Reactor Vessel: {'Road transportable' if road_transportable else 'Requires special transportation'}")
    print(f"Steam Generator: {sg_complexity} complexity, {sg_automation}")
    print(f"Containment: {containment_prefab}")
    
    return results

def estimate_manufacturing_timeline():
    """
    Estimate manufacturing and construction timeline for the SMR.
    Returns a dictionary with timeline estimates.
    """
    # Base manufacturing times (in months)
    vessel_manufacturing = 12
    steam_generator_manufacturing = 8
    turbine_manufacturing = 10
    containment_construction = 18
    
    # Adjust based on design complexity
    power = REACTOR_PARAMS.electrical_power.magnitude
    if power <= 10:
        complexity_factor = 0.8
    elif power <= 30:
        complexity_factor = 1.0
    else:
        complexity_factor = 1.2
    
    # Calculate adjusted times
    vessel_time = vessel_manufacturing * complexity_factor
    sg_time = steam_generator_manufacturing * complexity_factor
    turbine_time = turbine_manufacturing * complexity_factor
    containment_time = containment_construction * complexity_factor
    
    # Calculate critical path and total time
    long_lead_items = max(vessel_time, sg_time, turbine_time)
    site_prep_time = 6
    installation_time = 12
    testing_time = 6
    
    # Total project timeline
    total_time = site_prep_time + max(long_lead_items, containment_time) + installation_time + testing_time
    
    # Compile timeline
    timeline = {
        "long_lead_items": {
            "reactor_vessel": vessel_time,
            "steam_generators": sg_time,
            "turbine_generator": turbine_time
        },
        "construction": {
            "site_preparation": site_prep_time,
            "containment": containment_time,
            "installation": installation_time,
            "testing_commissioning": testing_time
        },
        "total_project_time": total_time
    }
    
    # Print timeline
    print("\n=== MANUFACTURING TIMELINE ===")
    print(f"Long Lead Items:")
    print(f"  - Reactor Vessel: {vessel_time:.1f} months")
    print(f"  - Steam Generators: {sg_time:.1f} months")
    print(f"  - Turbine Generator: {turbine_time:.1f} months")
    print(f"Construction:")
    print(f"  - Site Preparation: {site_prep_time} months")
    print(f"  - Containment: {containment_time:.1f} months")
    print(f"  - Installation: {installation_time} months")
    print(f"  - Testing & Commissioning: {testing_time} months")
    print(f"Total Project Timeline: {total_time:.1f} months ({total_time/12:.1f} years)")
    
    return timeline

def analyze_supply_chain():
    """
    Analyze the supply chain for key SMR components.
    Identifies critical suppliers and potential bottlenecks.
    """
    # Key components and their suppliers
    key_components = {
        "Reactor Pressure Vessel": {
            "suppliers": ["Doosan Heavy Industries (South Korea)", "Japan Steel Works (Japan)", "Framatome (France)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "Medium - Limited number of qualified manufacturers"
        },
        "Steam Generators": {
            "suppliers": ["Babcock & Wilcox (USA)", "Framatome (France)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple qualified suppliers"
        },
        "Control Rod Drive Mechanisms": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "SKODA JS (Czech Republic)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Medium - Specialized components"
        },
        "Reactor Coolant Pumps": {
            "suppliers": ["KSB Group (Germany)", "Curtiss-Wright (USA)", "Flowserve (USA)"],
            "lead_time": "8-12 months",
            "bottleneck_risk": "Low - Multiple suppliers"
        },
        "Digital Control Systems": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Lockheed Martin (USA)"],
            "lead_time": "6-10 months",
            "bottleneck_risk": "Medium - Qualification and licensing requirements"
        },
        "Turbine Generator": {
            "suppliers": ["General Electric (USA)", "Siemens (Germany)", "Mitsubishi Heavy Industries (Japan)"],
            "lead_time": "10-14 months",
            "bottleneck_risk": "Low - Standard technology"
        },
        "Fuel Assemblies": {
            "suppliers": ["Westinghouse (USA)", "Framatome (France)", "Global Nuclear Fuel (USA)"],
            "lead_time": "12-18 months",
            "bottleneck_risk": "High - Limited HALEU supply chain"
        }
    }
    
    # Identify critical path items
    critical_path = []
    for component, data in key_components.items():
        if "High" in data["bottleneck_risk"]:
            critical_path.append(component)
    
    # Print supply chain analysis
    print("\n=== SUPPLY CHAIN ANALYSIS ===")
    print("Critical Components:")
    for component in critical_path:
        data = key_components[component]
        print(f"  - {component}: {data['bottleneck_risk']}")
        print(f"    Suppliers: {', '.join(data['suppliers'])}")
        print(f"    Lead Time: {data['lead_time']}")
    
    print("\nSupply Chain Recommendations:")
    if "Fuel Assemblies" in critical_path:
        print("  - Secure HALEU supply through long-term contracts with multiple suppliers")
    if "Reactor Pressure Vessel" in critical_path:
        print("  - Place early orders for reactor pressure vessel to secure manufacturing slot")
    print("  - Develop qualification program for alternative suppliers to reduce bottleneck risks")
    print("  - Implement digital supply chain tracking system to monitor critical components")
    
    return {
        "components": key_components,
        "critical_path": critical_path
    }

# Run manufacturing analysis when imported
if __name__ != "__main__":  # This ensures it runs when imported but not when executed directly
    print("Initializing manufacturing analysis tools")
