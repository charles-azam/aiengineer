from pyforge import System, Requirement
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS
from reactor.systems_reactor import reactor_system, reactor_core, primary_loop, secondary_loop, safety_systems

# Get the auxiliary_systems from reactor_system.children
# This assumes the auxiliary_systems is the last item in reactor_system.children
auxiliary_systems = None
for child in reactor_system.children:
    if child.name == "Auxiliary Systems":
        auxiliary_systems = child
        break

if auxiliary_systems is None:
    print("Warning: Could not find auxiliary_systems in reactor_system.children")

# Fuel System
fuel_system = System(
    name="Nuclear Fuel System",
    description=(
        f"{REACTOR_PARAMS.fuel_type} fuel at {REACTOR_PARAMS.enrichment}% enrichment in "
        f"{REACTOR_PARAMS.fuel_assemblies} assemblies with {REACTOR_PARAMS.fuel_rods_per_assembly} rods each"
    ),
    requirements=[
        Requirement(
            name="Fuel Integrity",
            description=(
                f"Maintain fuel cladding integrity with <1% failure rate over "
                f"{REACTOR_PARAMS.refueling_interval} year fuel cycle."
            )
        ),
        Requirement(
            name="Burnup",
            description=(
                f"Achieve minimum average burnup of 45 GWd/tU."
            )
        )
    ],
    parent=reactor_core
)

# Initialize children attribute
fuel_system.children = []

# Specific fuel components
fuel_pellets = System(
    name="Fuel Pellets",
    description=(
        f"{REACTOR_PARAMS.fuel_type} ceramic pellets, 8.2 mm diameter, 10 mm height, "
        f"95% theoretical density, manufactured by Westinghouse"
    ),
    parent=fuel_system
)

fuel_cladding = System(
    name="Fuel Cladding",
    description=(
        f"Zircaloy-4 tubes, 9.5 mm outer diameter, 0.57 mm wall thickness, "
        f"manufactured by Sandvik Special Metals using pilgering process"
    ),
    parent=fuel_system
)

fuel_assembly_structure = System(
    name="Fuel Assembly Structure",
    description=(
        f"Zircaloy grid spacers and guide tubes, manufactured by Westinghouse, "
        f"with Inconel top and bottom nozzles, using precision welding and assembly"
    ),
    parent=fuel_system
)

# Control Rod System
control_rod_system = System(
    name="Control Rod System",
    description=(
        f"{REACTOR_PARAMS.control_rods} control rod assemblies with Ag-In-Cd neutron absorber, "
        f"electromagnetic drive mechanisms by Rolls-Royce"
    ),
    requirements=[
        Requirement(
            name="Shutdown Margin",
            description=(
                f"Provide minimum 2% Δk/k shutdown margin with highest worth rod stuck out."
            )
        ),
        Requirement(
            name="Insertion Time",
            description=(
                f"Full insertion in less than 2.5 seconds under all operating conditions."
            )
        )
    ],
    parent=reactor_core
)

# Initialize children attribute
control_rod_system.children = []

# Control rod components
control_rod_absorbers = System(
    name="Control Rod Absorbers",
    description=(
        f"Ag-In-Cd absorber material, 8.0 mm diameter, stainless steel cladding, "
        f"manufactured by Westinghouse using powder metallurgy and extrusion"
    ),
    parent=control_rod_system
)

control_rod_drives = System(
    name="Control Rod Drive Mechanisms",
    description=(
        f"Magnetic jack-type mechanisms by Rolls-Royce, 304 stainless steel construction, "
        f"with position indication accuracy of ±5 mm, manufactured using precision machining"
    ),
    parent=control_rod_system
)

# Reactor Pressure Vessel
pressure_vessel = System(
    name="Reactor Pressure Vessel",
    description=(
        f"SA-508 Grade 3 Class 1 low-alloy steel vessel, 3.5 m height, 2.3 m diameter, "
        f"200 mm wall thickness, manufactured by Japan Steel Works using ring-forging technique"
    ),
    requirements=[
        Requirement(
            name="Pressure Rating",
            description=(
                f"Withstand {THERMAL_PARAMS.primary_pressure.magnitude * 1.25} MPa design pressure "
                f"with 60-year design life."
            )
        ),
        Requirement(
            name="Radiation Resistance",
            description=(
                f"Maintain structural integrity with neutron fluence up to 5×10¹⁹ n/cm²."
            )
        )
    ],
    parent=primary_loop
)

# Initialize children attribute
pressure_vessel.children = []

vessel_internals = System(
    name="Reactor Vessel Internals",
    description=(
        f"304 stainless steel core barrel, lower core plate, and upper guide structure, "
        f"manufactured by Doosan Heavy Industries using precision machining and welding"
    ),
    parent=pressure_vessel
)

vessel_head = System(
    name="Reactor Vessel Head",
    description=(
        f"SA-508 Grade 3 Class 1 low-alloy steel head with penetrations for control rod drives, "
        f"manufactured by Japan Steel Works using forging and precision drilling"
    ),
    parent=pressure_vessel
)

# Primary Coolant Pump
primary_pump = System(
    name="Primary Coolant Pump",
    description=(
        f"Canned motor pump by Flowserve, 1200 kg/s flow rate, 0.5 MPa head, "
        f"316 stainless steel construction with ceramic bearings"
    ),
    requirements=[
        Requirement(
            name="Flow Rate",
            description=(
                f"Deliver {THERMAL_PARAMS.primary_flow_rate} flow rate with 15% margin."
            )
        ),
        Requirement(
            name="Reliability",
            description=(
                f"MTBF > 50,000 hours with quarterly maintenance."
            )
        )
    ],
    parent=primary_loop
)

# Pressurizer
pressurizer = System(
    name="Pressurizer",
    description=(
        f"Vertical cylindrical vessel by Babcock & Wilcox, 304 stainless steel construction, "
        f"10 m³ volume with electric heaters and water spray system, manufactured using forging and welding"
    ),
    requirements=[
        Requirement(
            name="Pressure Control",
            description=(
                f"Maintain primary system pressure at {THERMAL_PARAMS.primary_pressure} ±0.2 MPa during normal operation."
            )
        ),
        Requirement(
            name="Transient Response",
            description=(
                f"Limit pressure excursions to ±10% during design basis transients."
            )
        )
    ],
    parent=primary_loop
)

# Steam Generator
steam_generator = System(
    name="Steam Generator",
    description=(
        f"Vertical U-tube heat exchanger by BWXT, Inconel 690 tubes, "
        f"{THERMAL_PARAMS.heat_exchanger_capacity} capacity"
    ),
    requirements=[
        Requirement(
            name="Heat Transfer",
            description=(
                f"Transfer {THERMAL_PARAMS.heat_exchanger_capacity} with "
                f"primary-to-secondary temperature difference < 40°C."
            )
        ),
        Requirement(
            name="Tube Integrity",
            description=(
                f"<0.1% tube failure rate over 10-year operating period."
            )
        )
    ],
    parent=secondary_loop
)

# Initialize children attribute
steam_generator.children = []

steam_generator_tubes = System(
    name="Steam Generator Tubes",
    description=(
        f"Inconel 690 tubes, 17.5 mm outer diameter, 1.0 mm wall thickness, "
        f"manufactured by Sandvik Materials Technology using cold drawing and annealing"
    ),
    parent=steam_generator
)

steam_generator_shell = System(
    name="Steam Generator Shell",
    description=(
        f"SA-508 Grade 3 Class 1 low-alloy steel shell with 304 stainless steel internals, "
        f"manufactured by BWXT using forging and welding"
    ),
    parent=steam_generator
)

# Turbine-Generator
turbine_generator = System(
    name="Turbine-Generator System",
    description=(
        f"Tandem-compound steam turbine by GE Power, 3600 rpm, "
        f"coupled to 25 MVA hydrogen-cooled generator"
    ),
    requirements=[
        Requirement(
            name="Power Output",
            description=(
                f"Generate {REACTOR_PARAMS.electrical_power} at 0.9 power factor."
            )
        ),
        Requirement(
            name="Efficiency",
            description=(
                f"Achieve {THERMAL_PARAMS.turbine_efficiency*100:.1f}% isentropic efficiency at rated conditions."
            )
        )
    ],
    parent=secondary_loop
)

# Initialize children attribute
turbine_generator.children = []

turbine = System(
    name="Steam Turbine",
    description=(
        f"Tandem-compound turbine with high-pressure and low-pressure sections by GE Power, "
        f"12Cr steel rotor and blades, manufactured using precision forging and machining"
    ),
    parent=turbine_generator
)

generator = System(
    name="Electrical Generator",
    description=(
        f"25 MVA hydrogen-cooled synchronous generator by GE Power, 13.8 kV, 3600 rpm, "
        f"with static excitation system, manufactured using precision winding and assembly"
    ),
    parent=turbine_generator
)

condenser = System(
    name="Main Condenser",
    description=(
        f"Shell and tube heat exchanger by SPX Cooling Technologies, titanium tubes, "
        f"40 MW heat rejection capacity, manufactured using tube expansion and rolling"
    ),
    parent=secondary_loop
)

# Containment Structure
containment = System(
    name="Containment Structure",
    description=(
        f"{SAFETY_PARAMS.containment_type}, {SAFETY_PARAMS.containment_thickness} thick, "
        f"designed by Bechtel, constructed using slip-forming technique"
    ),
    requirements=[
        Requirement(
            name="Pressure Capacity",
            description=(
                f"Withstand {SAFETY_PARAMS.containment_design_pressure} internal pressure."
            )
        ),
        Requirement(
            name="Leak Rate",
            description=(
                f"<0.1% volume per day at design pressure."
            )
        ),
        Requirement(
            name="Impact Resistance",
            description=(
                f"Withstand impact of commercial aircraft without loss of function."
            )
        )
    ],
    parent=safety_systems
)

# Emergency Core Cooling System
eccs = System(
    name="Emergency Core Cooling System",
    description=(
        f"{SAFETY_PARAMS.eccs_type} with {SAFETY_PARAMS.eccs_water_volume} water inventory, "
        f"designed by Westinghouse, using nitrogen-pressurized accumulators"
    ),
    requirements=[
        Requirement(
            name="Cooling Capacity",
            description=(
                f"Maintain core temperature below 1200°C during design basis accidents."
            )
        ),
        Requirement(
            name="Activation Time",
            description=(
                f"Begin injection within {SAFETY_PARAMS.eccs_activation_time} of LOCA signal."
            )
        )
    ],
    parent=safety_systems
)

# Initialize children attribute
eccs.children = []

accumulators = System(
    name="Passive Accumulators",
    description=(
        f"Three nitrogen-pressurized accumulators by Westinghouse, 304 stainless steel construction, "
        f"100 m³ total water volume, manufactured using forging and welding"
    ),
    parent=eccs
)

safety_injection_pumps = System(
    name="Safety Injection Pumps",
    description=(
        f"Three high-pressure centrifugal pumps by Flowserve, 50 kg/s capacity each, "
        f"316 stainless steel construction, manufactured using precision casting and machining"
    ),
    parent=eccs
)

# Passive Residual Heat Removal System
passive_heat_removal = System(
    name="Passive Residual Heat Removal System",
    description=(
        f"Natural circulation heat exchangers by Westinghouse, located in in-containment refueling water storage tank, "
        f"304 stainless steel construction, manufactured using tube bending and welding"
    ),
    requirements=[
        Requirement(
            name="Cooling Capacity",
            description=(
                f"Remove decay heat at {SAFETY_PARAMS.passive_cooling_capacity} capacity for "
                f"{SAFETY_PARAMS.passive_cooling_duration} without AC power."
            )
        ),
        Requirement(
            name="Reliability",
            description=(
                f"Achieve 99.99% reliability for passive actuation upon demand."
            )
        )
    ],
    parent=safety_systems
)

# Electrical Systems
electrical_systems = System(
    name="Electrical Systems",
    description=(
        f"Power distribution and backup power systems by ABB, "
        f"including diesel generators and battery backup systems"
    ),
    requirements=[
        Requirement(
            name="Power Reliability",
            description=(
                f"Provide uninterrupted power to safety systems with 99.999% reliability."
            )
        ),
        Requirement(
            name="Backup Duration",
            description=(
                f"Supply backup power for minimum 72 hours during station blackout conditions."
            )
        )
    ],
    parent=auxiliary_systems
)

# Initialize children attribute
electrical_systems.children = []

diesel_generators = System(
    name="Emergency Diesel Generators",
    description=(
        f"Two 2 MW diesel generators by Cummins, with 7-day fuel supply, "
        f"manufactured using precision engine assembly techniques"
    ),
    parent=electrical_systems
)

battery_systems = System(
    name="DC Battery Systems",
    description=(
        f"Four trains of 125V DC batteries by C&D Technologies, valve-regulated lead-acid type, "
        f"with 24-hour capacity, manufactured using controlled grid casting and assembly"
    ),
    parent=electrical_systems
)

# Cooling Water Systems
cooling_water = System(
    name="Component Cooling Water System",
    description=(
        f"Closed-loop cooling system by SPX Cooling Technologies, "
        f"using plate heat exchangers and centrifugal pumps"
    ),
    requirements=[
        Requirement(
            name="Cooling Capacity",
            description=(
                f"Remove heat from auxiliary components with 20% margin above design requirements."
            )
        ),
        Requirement(
            name="Reliability",
            description=(
                f"Achieve 99.9% availability with redundant trains."
            )
        )
    ],
    parent=auxiliary_systems
)

# Waste Management Systems
waste_management = System(
    name="Radioactive Waste Management Systems",
    description=(
        f"Liquid, gaseous, and solid waste processing systems by Studsvik, "
        f"using filtration, ion exchange, and solidification technologies"
    ),
    requirements=[
        Requirement(
            name="Processing Capacity",
            description=(
                f"Process all operational waste with 50% margin above expected generation rates."
            )
        ),
        Requirement(
            name="Release Limits",
            description=(
                f"Maintain releases below 10% of regulatory limits during normal operation."
            )
        )
    ],
    parent=auxiliary_systems
)

# Count children for reporting
fuel_system_children_count = len(fuel_system.children) if hasattr(fuel_system, 'children') and fuel_system.children is not None else 0
safety_systems_children_count = len(safety_systems.children) if hasattr(safety_systems, 'children') and safety_systems.children is not None else 0
auxiliary_systems_children_count = len(auxiliary_systems.children) if hasattr(auxiliary_systems, 'children') and auxiliary_systems.children is not None else 0

print(f"Component systems defined with {fuel_system_children_count} fuel subsystems, {safety_systems_children_count} safety subsystems, and {auxiliary_systems_children_count} auxiliary subsystems")
print("systems_components.py loaded successfully")
