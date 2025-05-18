"""
Maintenance simulation for the Small Modular Reactor.
Analyzes maintenance requirements, schedules, and costs.
"""

from reactor.parameters_reactor import REACTOR_PARAMS, PRIMARY_LOOP_PARAMS, SECONDARY_LOOP_PARAMS

def calculate_maintenance_schedule():
    """Calculate the maintenance schedule for the SMR."""
    # Key parameters
    design_lifetime = REACTOR_PARAMS.design_lifetime.magnitude  # years
    refueling_interval = REACTOR_PARAMS.refueling_interval.magnitude  # years
    
    print(f"DEBUG: design_lifetime={design_lifetime}, refueling_interval={refueling_interval}")
    
    # Define maintenance categories
    maintenance_categories = {
        "Refueling Outage": {
            "frequency": refueling_interval,  # years
            "duration": 21,  # days
            "activities": [
                "Fuel replacement",
                "Reactor vessel inspection",
                "Control rod drive mechanism maintenance",
                "Primary loop inspection"
            ]
        },
        "Major Overhaul": {
            "frequency": 10,  # years
            "duration": 60,  # days
            "activities": [
                "Steam generator inspection and tube plugging",
                "Turbine overhaul",
                "Reactor coolant pump overhaul",
                "Electrical system maintenance",
                "Instrumentation and control system updates"
            ]
        },
        "Routine Maintenance": {
            "frequency": 1,  # years
            "duration": 7,  # days
            "activities": [
                "Secondary loop maintenance",
                "Cooling water system maintenance",
                "Electrical system testing",
                "Instrumentation calibration",
                "Valve testing and maintenance"
            ]
        }
    }
    
    # Calculate number of each maintenance type over lifetime
    refueling_outages = int(design_lifetime / refueling_interval)
    major_overhauls = int(design_lifetime / maintenance_categories["Major Overhaul"]["frequency"])
    routine_maintenances = int(design_lifetime / maintenance_categories["Routine Maintenance"]["frequency"])
    
    # Calculate total downtime
    refueling_downtime = refueling_outages * maintenance_categories["Refueling Outage"]["duration"]
    overhaul_downtime = major_overhauls * maintenance_categories["Major Overhaul"]["duration"]
    routine_downtime = routine_maintenances * maintenance_categories["Routine Maintenance"]["duration"]
    
    total_downtime = refueling_downtime + overhaul_downtime + routine_downtime
    total_downtime_years = total_downtime / 365
    
    # Calculate availability factor
    availability = (design_lifetime - total_downtime_years) / design_lifetime * 100
    
    print(f"\nMaintenance Schedule Analysis:")
    print(f"Design Lifetime: {design_lifetime} years")
    print(f"Refueling Interval: {refueling_interval} years")
    print(f"Number of Refueling Outages: {refueling_outages}")
    print(f"Number of Major Overhauls: {major_overhauls}")
    print(f"Number of Routine Maintenance Periods: {routine_maintenances}")
    print(f"Total Maintenance Downtime: {total_downtime} days ({total_downtime_years:.2f} years)")
    print(f"Projected Availability Factor: {availability:.2f}%")
    
    return {
        "refueling_outages": refueling_outages,
        "major_overhauls": major_overhauls,
        "routine_maintenances": routine_maintenances,
        "total_downtime_days": total_downtime,
        "availability_factor": availability
    }

def estimate_maintenance_costs():
    """Estimate the maintenance costs over the reactor lifetime."""
    # Key parameters
    design_lifetime = REACTOR_PARAMS.design_lifetime.magnitude  # years
    refueling_interval = REACTOR_PARAMS.refueling_interval.magnitude  # years
    electrical_power = REACTOR_PARAMS.electrical_power.magnitude  # MW
    
    # Maintenance cost estimates (based on industry benchmarks)
    refueling_cost = 2.5 * electrical_power  # $million per refueling
    major_overhaul_cost = 5.0 * electrical_power  # $million per major overhaul
    routine_maintenance_cost = 0.5 * electrical_power  # $million per year
    
    # Calculate number of each maintenance type over lifetime
    refueling_outages = int(design_lifetime / refueling_interval)
    major_overhauls = int(design_lifetime / 10)  # Assuming major overhaul every 10 years
    
    # Calculate total costs
    total_refueling_cost = refueling_outages * refueling_cost
    total_overhaul_cost = major_overhauls * major_overhaul_cost
    total_routine_cost = design_lifetime * routine_maintenance_cost
    
    total_maintenance_cost = total_refueling_cost + total_overhaul_cost + total_routine_cost
    annual_maintenance_cost = total_maintenance_cost / design_lifetime
    
    # Calculate maintenance cost per MWh
    capacity_factor = 0.90  # typical for nuclear
    annual_generation = electrical_power * 8760 * capacity_factor  # MWh/year
    maintenance_cost_per_mwh = annual_maintenance_cost * 1e6 / annual_generation  # $/MWh
    
    print(f"\nMaintenance Cost Analysis:")
    print(f"Refueling Cost: ${refueling_cost:.2f} million per outage")
    print(f"Major Overhaul Cost: ${major_overhaul_cost:.2f} million per overhaul")
    print(f"Routine Maintenance Cost: ${routine_maintenance_cost:.2f} million per year")
    print(f"Total Lifetime Maintenance Cost: ${total_maintenance_cost:.2f} million")
    print(f"Annual Maintenance Cost: ${annual_maintenance_cost:.2f} million/year")
    print(f"Maintenance Cost per MWh: ${maintenance_cost_per_mwh:.2f}/MWh")
    
    return {
        "annual_maintenance_cost": annual_maintenance_cost,
        "total_maintenance_cost": total_maintenance_cost,
        "maintenance_cost_per_mwh": maintenance_cost_per_mwh
    }

def analyze_component_reliability():
    """Analyze the reliability of key components and systems."""
    # Component reliability data (mean time between failures in hours)
    component_reliability = {
        "Reactor Coolant Pumps": {
            "mtbf": 50000,  # hours
            "repair_time": 168,  # hours (1 week)
            "redundancy": PRIMARY_LOOP_PARAMS.primary_pump_count,
            "manufacturer": "KSB Group",
            "maintenance_interval": 17520  # hours (2 years)
        },
        "Control Rod Drive Mechanisms": {
            "mtbf": 100000,  # hours
            "repair_time": 72,  # hours (3 days)
            "redundancy": "N-2",  # N-2 redundancy
            "manufacturer": "Westinghouse",
            "maintenance_interval": 35040  # hours (4 years)
        },
        "Steam Generator Tubes": {
            "mtbf": 200000,  # hours
            "repair_time": 240,  # hours (10 days)
            "redundancy": "10%",  # 10% margin in heat transfer area
            "manufacturer": "Babcock & Wilcox",
            "maintenance_interval": 35040  # hours (4 years)
        },
        "Turbine Generator": {
            "mtbf": 80000,  # hours
            "repair_time": 336,  # hours (2 weeks)
            "redundancy": "None",
            "manufacturer": "General Electric",
            "maintenance_interval": 26280  # hours (3 years)
        },
        "Emergency Diesel Generators": {
            "mtbf": 30000,  # hours
            "repair_time": 48,  # hours (2 days)
            "redundancy": "2x100%",  # 2 redundant generators
            "manufacturer": "Cummins",
            "maintenance_interval": 8760  # hours (1 year)
        }
    }
    
    print(f"\nComponent Reliability Analysis:")
    
    for component, data in component_reliability.items():
        availability = data["mtbf"] / (data["mtbf"] + data["repair_time"])
        availability_with_redundancy = calculate_redundant_availability(availability, data["redundancy"])
        
        print(f"\n{component}:")
        print(f"  Manufacturer: {data['manufacturer']}")
        print(f"  Mean Time Between Failures: {data['mtbf']} hours ({data['mtbf']/8760:.1f} years)")
        print(f"  Repair Time: {data['repair_time']} hours ({data['repair_time']/24:.1f} days)")
        print(f"  Maintenance Interval: {data['maintenance_interval']} hours ({data['maintenance_interval']/8760:.1f} years)")
        print(f"  Redundancy: {data['redundancy']}")
        print(f"  Component Availability: {availability*100:.4f}%")
        print(f"  System Availability with Redundancy: {availability_with_redundancy*100:.4f}%")
    
    return component_reliability

def calculate_redundant_availability(component_availability, redundancy):
    """Calculate system availability with redundancy."""
    component_unavailability = 1 - component_availability
    
    if redundancy == "None":
        return component_availability
    elif redundancy == "N-2":
        # Simplified N-2 redundancy calculation
        return 1 - (component_unavailability ** 3)
    elif redundancy == "10%":
        # Simplified calculation for margin redundancy
        return 1 - (component_unavailability * 0.9)
    elif isinstance(redundancy, str) and "x100%" in redundancy:
        # N+M redundancy where N=1 and M is the number before x100%
        m = int(redundancy.split("x")[0])
        return 1 - (component_unavailability ** (m + 1))
    else:
        # Default case
        print(f"DEBUG: Using default availability calculation for redundancy type: {type(redundancy)}, value: {redundancy}")
        return component_availability

# Run maintenance simulations
print("\n=== MAINTENANCE SIMULATION RESULTS ===\n")
maintenance_schedule = calculate_maintenance_schedule()
maintenance_costs = estimate_maintenance_costs()
component_reliability = analyze_component_reliability()

print("\n=== MAINTENANCE SIMULATION SUMMARY ===")
print(f"Projected Availability Factor: {maintenance_schedule['availability_factor']:.2f}%")
print(f"Annual Maintenance Cost: ${maintenance_costs['annual_maintenance_cost']:.2f} million/year")
print(f"Maintenance Cost per MWh: ${maintenance_costs['maintenance_cost_per_mwh']:.2f}/MWh")
