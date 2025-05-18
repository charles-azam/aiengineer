"""
Maintenance planning and operational tools for the small modular reactor.
"""
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
import math
import numpy as np

def calculate_refueling_outage_schedule():
    """
    Calculate the refueling outage schedule and critical path activities.
    
    Returns:
        Dictionary with outage schedule information
    """
    # Key activities and their durations (days)
    activities = {
        "Plant cooldown": 2,
        "Reactor disassembly": 3,
        "Fuel unloading": 4,
        "Fuel loading": 4,
        "Reactor reassembly": 3,
        "Leak testing": 2,
        "Plant heatup": 2,
        "Physics testing": 3,
        "Power ascension": 3
    }
    
    # Calculate critical path duration
    critical_path_duration = sum(activities.values())
    
    # Calculate parallel activities efficiency
    # Some activities can be performed in parallel, reducing total outage time
    parallel_efficiency = 0.8
    
    # Calculate expected outage duration
    expected_outage_duration = critical_path_duration * parallel_efficiency
    
    # Calculate refueling frequency
    refueling_interval_years = REACTOR_PARAMS.refueling_interval
    refueling_interval_days = refueling_interval_years * 365
    
    # Calculate lifetime number of refuelings
    design_life = REACTOR_PARAMS.design_life
    num_refuelings = math.floor(design_life / refueling_interval_years)
    
    # Calculate total downtime for refueling over plant life
    total_refueling_downtime = num_refuelings * expected_outage_duration
    
    return {
        "critical_path_duration": critical_path_duration,
        "expected_outage_duration": expected_outage_duration,
        "refueling_interval_days": refueling_interval_days,
        "lifetime_refuelings": num_refuelings,
        "total_refueling_downtime": total_refueling_downtime
    }

def calculate_maintenance_costs(
    annual_maintenance_cost_percentage: float = 0.02,  # 2% of capital cost
    major_overhaul_frequency_years: int = 10,
    major_overhaul_cost_percentage: float = 0.1,  # 10% of capital cost
    capital_cost_per_kw: float = 5000  # $/kW
):
    """
    Calculate maintenance costs over the plant lifetime.
    
    Args:
        annual_maintenance_cost_percentage: Annual maintenance cost as percentage of capital cost
        major_overhaul_frequency_years: Frequency of major overhauls in years
        major_overhaul_cost_percentage: Cost of major overhaul as percentage of capital cost
        capital_cost_per_kw: Capital cost per kW installed
        
    Returns:
        Dictionary with maintenance cost information
    """
    # Plant parameters
    power_kw = REACTOR_PARAMS.electrical_power.magnitude * 1000  # kW
    lifetime_years = REACTOR_PARAMS.design_life  # years
    
    # Capital cost
    capital_cost = capital_cost_per_kw * power_kw  # $
    
    # Annual maintenance cost
    annual_maintenance = capital_cost * annual_maintenance_cost_percentage  # $/year
    
    # Number of major overhauls
    num_overhauls = math.floor(lifetime_years / major_overhaul_frequency_years)
    
    # Cost per major overhaul
    overhaul_cost = capital_cost * major_overhaul_cost_percentage  # $
    
    # Total maintenance cost over lifetime
    total_maintenance = annual_maintenance * lifetime_years + overhaul_cost * num_overhauls
    
    # Average annual maintenance cost
    average_annual = total_maintenance / lifetime_years
    
    # Maintenance cost per MWh
    capacity_factor = 0.9
    annual_mwh = power_kw * 8760 * capacity_factor / 1000  # MWh
    maintenance_per_mwh = average_annual / annual_mwh  # $/MWh
    
    return {
        "annual_routine_maintenance": annual_maintenance,
        "major_overhaul_cost": overhaul_cost,
        "number_of_overhauls": num_overhauls,
        "total_lifetime_maintenance": total_maintenance,
        "average_annual_maintenance": average_annual,
        "maintenance_cost_per_mwh": maintenance_per_mwh
    }

def calculate_staff_requirements():
    """
    Calculate staffing requirements for plant operation.
    
    Returns:
        Dictionary with staffing information
    """
    # Base staffing for a small modular reactor
    # These numbers are based on industry estimates for SMRs
    
    # Operations staff (5 shifts for 24/7 coverage)
    operators_per_shift = 3
    shifts = 5
    total_operators = operators_per_shift * shifts
    
    # Maintenance staff
    mechanical_maintenance = 8
    electrical_maintenance = 6
    i_and_c_maintenance = 4
    
    # Technical support
    engineering = 10
    radiation_protection = 6
    chemistry = 4
    
    # Administration and management
    management = 5
    administrative = 6
    security = 15
    
    # Total staff
    total_staff = (total_operators + mechanical_maintenance + electrical_maintenance +
                  i_and_c_maintenance + engineering + radiation_protection +
                  chemistry + management + administrative + security)
    
    # Staff cost (assuming average annual salary of $100,000 including benefits)
    annual_staff_cost = total_staff * 100000  # $
    
    # Staff cost per MWh
    power_kw = REACTOR_PARAMS.electrical_power.magnitude * 1000  # kW
    capacity_factor = 0.9
    annual_mwh = power_kw * 8760 * capacity_factor / 1000  # MWh
    staff_cost_per_mwh = annual_staff_cost / annual_mwh  # $/MWh
    
    return {
        "operations_staff": total_operators,
        "maintenance_staff": mechanical_maintenance + electrical_maintenance + i_and_c_maintenance,
        "technical_staff": engineering + radiation_protection + chemistry,
        "admin_and_security": management + administrative + security,
        "total_staff": total_staff,
        "annual_staff_cost": annual_staff_cost,
        "staff_cost_per_mwh": staff_cost_per_mwh
    }

def calculate_availability_and_reliability():
    """
    Calculate plant availability and reliability metrics.
    
    Returns:
        Dictionary with availability and reliability information
    """
    # Typical values for advanced SMRs
    planned_outage_days_per_year = REACTOR_PARAMS.refueling_interval * 20 / 365  # days/year
    unplanned_outage_rate = 0.02  # 2% unplanned outage rate
    
    # Calculate availability
    planned_availability = (365 - planned_outage_days_per_year) / 365
    unplanned_availability = 1 - unplanned_outage_rate
    total_availability = planned_availability * unplanned_availability
    
    # Calculate capacity factor (availability * performance factor)
    performance_factor = 0.98  # 98% of rated power when operating
    capacity_factor = total_availability * performance_factor
    
    # Calculate reliability metrics
    forced_outage_rate = unplanned_outage_rate
    mean_time_between_forced_outages = 365 / (forced_outage_rate * 365 / 7)  # weeks
    
    return {
        "planned_outage_days_per_year": planned_outage_days_per_year,
        "planned_availability": planned_availability * 100,
        "unplanned_availability": unplanned_availability * 100,
        "total_availability": total_availability * 100,
        "capacity_factor": capacity_factor * 100,
        "forced_outage_rate": forced_outage_rate * 100,
        "mtbfo_weeks": mean_time_between_forced_outages
    }

# Run calculations
refueling_schedule = calculate_refueling_outage_schedule()
maintenance_costs = calculate_maintenance_costs()
staffing = calculate_staff_requirements()
availability = calculate_availability_and_reliability()

print(f"Refueling outage duration: {refueling_schedule['expected_outage_duration']:.2f} days")
print(f"Lifetime number of refuelings: {refueling_schedule['lifetime_refuelings']}")
print(f"Annual maintenance cost: ${maintenance_costs['annual_routine_maintenance']:,.2f}")
print(f"Maintenance cost per MWh: ${maintenance_costs['maintenance_cost_per_mwh']:.2f}/MWh")
print(f"Total staff requirement: {staffing['total_staff']} personnel")
print(f"Expected capacity factor: {availability['capacity_factor']:.2f}%")
