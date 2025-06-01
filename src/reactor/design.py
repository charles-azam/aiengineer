"""
High-Temperature Gas-cooled Reactor (HTGR) Design Document
"""
from pyforge.note import (
    Citation, DocumentConfig, Figure, Table, Title, display
)
from reactor.parameters_htgr import HTGR_PARAMS
from reactor.systems_htgr import htgr_system
from reactor.simulation_htgr import get_performance_metrics

print("Loading HTGR design document...")

import pandas as pd
from pathlib import Path

# Document metadata
config = DocumentConfig(
    title="High-Temperature Gas-cooled Reactor (HTGR) Design Report",
    author="AI Engineering Team",
    date="2025-06-02"
)
display(config)

# Title and Introduction
display(Title("# High-Temperature Gas-cooled Reactor (HTGR) Design"))

display("## Introduction")
display(
    "This document presents the design of a modular High-Temperature Gas-cooled Reactor (HTGR) "
    "system intended for decarbonizing industrial heat production. The HTGR utilizes TRISO "
    "fuel particles and helium coolant to achieve high operating temperatures while maintaining "
    "inherent safety characteristics. The modular design allows for scalable deployment at "
    "various industrial sites with thermal power outputs of 10, 15, or 20 MW."
    "\n\n"
    "Key features of this HTGR design include:"
    "\n\n"
    "- Core temperatures up to 600°C for efficient industrial heat applications\n"
    "- TRISO fuel particles providing inherent containment of fission products\n"
    "- Passive safety features for decay heat removal\n"
    "- Helium primary coolant and CO₂ secondary loop for heat transfer\n"
    "- Modular construction for factory fabrication and on-site assembly\n"
    "- 20-year design life with minimal refueling requirements\n"
    "- Compatibility with existing industrial heat systems"
)

# System Overview
display(Title("# System Overview"))
display(htgr_system.display())

# Import the subsystems after displaying the main system
from reactor.systems_htgr import reactor_core, primary_cooling, secondary_cooling, safety_systems, control_systems

# System Diagram (text-based representation)
display("## System Diagram")
diagram = """
    ┌───────────────────────────────────────────────────────────────┐
    │                      HTGR System                              │
    │                                                               │
    │  ┌─────────────────┐         ┌─────────────────────────┐      │
    │  │                 │         │                         │      │
    │  │  Reactor Core   │◄────────┤   Control & Protection  │      │
    │  │  (TRISO Fuel)   │         │        Systems          │      │
    │  │                 │         │                         │      │
    │  └────────┬────────┘         └─────────────────────────┘      │
    │           │                                                   │
    │           │ Helium                                            │
    │           │ (7 MPa, 600°C)                                    │
    │           ▼                                                   │
    │  ┌────────────────┐          ┌─────────────────────────┐      │
    │  │                │          │                         │      │
    │  │  Primary Heat  │◄─────────┤    Passive Safety       │      │
    │  │  Exchanger     │          │      Systems            │      │
    │  │                │          │                         │      │
    │  └────────┬───────┘          └─────────────────────────┘      │
    │           │                                                   │
    │           │ CO₂                                               │
    │           │ (20 MPa, 550°C)                                   │
    │           ▼                                                   │
    │  ┌────────────────┐          ┌─────────────────────────┐      │
    │  │                │          │                         │      │
    │  │  Secondary     │◄─────────┤   Industrial Interface  │      │
    │  │  Heat Transfer │          │   (Steam/Air/Oil)       │      │
    │  │                │          │                         │      │
    │  └────────┬───────┘          └─────────────────────────┘      │
    │           │                                                   │
    │           │                                                   │
    │           ▼                                                   │
    │  ┌────────────────────────────────────────────────────┐       │
    │  │                                                    │       │
    │  │            Industrial Process Heat                 │       │
    │  │                                                    │       │
    │  └────────────────────────────────────────────────────┘       │
    │                                                               │
    └───────────────────────────────────────────────────────────────┘
"""
display(Figure(diagram, "HTGR System Diagram", "fig-system-diagram"))

# Core Design and TRISO Fuel
display(Title("# Core Design and TRISO Fuel Configuration"))
display(
    "The HTGR core utilizes TRISO (TRIstructural-ISOtropic) fuel particles, which consist "
    "of uranium kernels encapsulated within multiple layers of carbon and silicon carbide. "
    "This design provides inherent containment of fission products and allows for high "
    "temperature operation."
    "\n\n"
    "### TRISO Fuel Structure"
    "\n\n"
    "Each TRISO particle consists of:"
    "\n\n"
    f"- Uranium kernel ({HTGR_PARAMS.fuel_kernel_diameter} diameter, {HTGR_PARAMS.fuel_enrichment} enriched)\n"
    "- Porous carbon buffer layer\n"
    "- Inner pyrolytic carbon layer\n"
    "- Silicon carbide barrier layer\n"
    "- Outer pyrolytic carbon layer"
    "\n\n"
    "These particles are embedded in a graphite matrix to form fuel compacts, which are "
    "then arranged in the core to achieve the desired power distribution and neutron economy."
)

# TRISO fuel diagram
triso_diagram = """
    ┌─────────────────────────────────────────────────────┐
    │                 TRISO Fuel Particle                 │
    │                                                     │
    │                  ┌───────────────┐                  │
    │                  │   Uranium     │                  │
    │                  │    Kernel     │                  │
    │                  │  (500 μm)     │                  │
    │                  └───────────────┘                  │
    │                        │                            │
    │           ┌────────────┴────────────┐               │
    │           │     Buffer Layer        │               │
    │           │  (Porous Carbon)        │               │
    │           └────────────┬────────────┘               │
    │                        │                            │
    │           ┌────────────┴────────────┐               │
    │           │  Inner PyC Layer        │               │
    │           │  (Pyrolytic Carbon)     │               │
    │           └────────────┬────────────┘               │
    │                        │                            │
    │           ┌────────────┴────────────┐               │
    │           │  SiC Barrier Layer      │               │
    │           │  (Silicon Carbide)      │               │
    │           └────────────┬────────────┘               │
    │                        │                            │
    │           ┌────────────┴────────────┐               │
    │           │  Outer PyC Layer        │               │
    │           │  (Pyrolytic Carbon)     │               │
    │           └────────────┬────────────┘               │
    │                        │                            │
    │                        ▼                            │
    │           ┌────────────────────────┐                │
    │           │   Graphite Matrix      │                │
    │           └────────────────────────┘                │
    │                                                     │
    └─────────────────────────────────────────────────────┘
"""
display(Figure(triso_diagram, "TRISO Fuel Particle Structure", "fig-triso"))

# Core parameters table
df_core = pd.DataFrame([
    {"Parameter": "Fuel Type", "Value": HTGR_PARAMS.fuel_type},
    {"Parameter": "Fuel Enrichment", "Value": f"{HTGR_PARAMS.fuel_enrichment}"},
    {"Parameter": "Fuel Kernel Diameter", "Value": f"{HTGR_PARAMS.fuel_kernel_diameter}"},
    {"Parameter": "Core Outlet Temperature", "Value": f"{HTGR_PARAMS.core_outlet_temp}"},
    {"Parameter": "Core Inlet Temperature", "Value": f"{HTGR_PARAMS.core_inlet_temp}"},
    {"Parameter": "Design Life", "Value": f"{HTGR_PARAMS.design_lifetime}"},
    {"Parameter": "Refueling Interval", "Value": f"{HTGR_PARAMS.refueling_interval}"},
])
display(Table(df_core, "Core Design Parameters", "tbl-core"))

# Cooling Loops
display(Title("# Primary and Secondary Cooling Loops"))
display(
    "The HTGR employs a dual-loop cooling system to efficiently transfer heat from the "
    "reactor core to industrial applications while maintaining isolation between the "
    "nuclear and industrial systems."
    "\n\n"
    "### Primary Cooling Loop"
    "\n\n"
    f"The primary cooling loop uses helium gas at {HTGR_PARAMS.helium_pressure} as the coolant. "
    "Helium is chemically inert, which prevents corrosion and eliminates the risk of chemical "
    "reactions with core materials. The helium circulates through the reactor core, entering "
    f"at {HTGR_PARAMS.core_inlet_temp} and exiting at up to {HTGR_PARAMS.core_outlet_temp}."
    "\n\n"
    "### Secondary Cooling Loop"
    "\n\n"
    f"The secondary cooling loop uses {HTGR_PARAMS.secondary_fluid} at {HTGR_PARAMS.secondary_pressure} "
    f"to transfer heat from the primary loop to industrial applications. The {HTGR_PARAMS.secondary_fluid} "
    f"can reach temperatures up to {HTGR_PARAMS.secondary_max_temp}, making it suitable for a wide "
    "range of industrial processes. This loop provides a barrier between the nuclear system and "
    "industrial applications, preventing any potential contamination."
)

# Cooling parameters table
df_cooling = pd.DataFrame([
    {"Parameter": "Primary Coolant", "Value": "Helium"},
    {"Parameter": "Primary Coolant Pressure", "Value": f"{HTGR_PARAMS.helium_pressure}"},
    {"Parameter": "Primary Inlet Temperature", "Value": f"{HTGR_PARAMS.core_inlet_temp}"},
    {"Parameter": "Primary Outlet Temperature", "Value": f"{HTGR_PARAMS.core_outlet_temp}"},
    {"Parameter": "Secondary Coolant", "Value": HTGR_PARAMS.secondary_fluid},
    {"Parameter": "Secondary Coolant Pressure", "Value": f"{HTGR_PARAMS.secondary_pressure}"},
    {"Parameter": "Secondary Maximum Temperature", "Value": f"{HTGR_PARAMS.secondary_max_temp}"},
])
display(Table(df_cooling, "Cooling System Parameters", "tbl-cooling"))

# Safety Systems
display(Title("# Safety Systems and Passive Features"))
display(
    "Safety is a fundamental aspect of the HTGR design, with multiple layers of protection "
    "and inherent safety features that do not rely on active systems or operator intervention."
    "\n\n"
    "### Inherent Safety Features"
    "\n\n"
    "- **TRISO Fuel Containment**: Each fuel particle acts as a miniature containment vessel, "
    "retaining fission products even at extreme temperatures.\n"
    "- **Negative Temperature Coefficient**: The reactor naturally reduces power as temperature increases.\n"
    "- **High Heat Capacity**: The graphite moderator provides thermal inertia, slowing temperature changes.\n"
    "- **Low Power Density**: The core operates at a low power density, preventing rapid temperature excursions."
    "\n\n"
    "### Passive Safety Systems"
    "\n\n"
    "- **Passive Decay Heat Removal**: Natural circulation cooling systems remove decay heat without "
    "requiring pumps or external power.\n"
    "- **Reactor Cavity Cooling System**: A passive system that transfers heat from the reactor vessel "
    "to the environment through natural convection.\n"
    "- **Control Rod Gravity Insertion**: Control rods designed to insert automatically under gravity "
    "in case of power loss."
    "\n\n"
    "### Defense in Depth"
    "\n\n"
    "The HTGR employs multiple barriers to prevent the release of radioactive materials:\n"
    "1. TRISO fuel coatings\n"
    "2. Graphite matrix\n"
    "3. Primary coolant boundary\n"
    "4. Reactor building containment"
)

# Scalability and Modular Design
display(Title("# Scalability and Modular Design Options"))
display(
    "The HTGR is designed with modularity and scalability as core principles, allowing for "
    "flexible deployment across various industrial applications. Three standard power variants "
    "are available to match different heat requirements:"
    "\n\n"
    f"- **Small Variant**: {HTGR_PARAMS.thermal_power_small} thermal output\n"
    f"- **Medium Variant**: {HTGR_PARAMS.thermal_power_medium} thermal output\n"
    f"- **Large Variant**: {HTGR_PARAMS.thermal_power_large} thermal output"
    "\n\n"
    "Multiple modules can be installed at a single site to provide additional capacity or "
    "redundancy. The modular approach offers several advantages:"
    "\n\n"
    "- **Factory Fabrication**: Major components are manufactured in controlled factory settings.\n"
    "- **Simplified Transportation**: Modules are sized for standard transportation methods.\n"
    "- **Reduced On-site Construction**: On-site work is limited to assembly and integration.\n"
    "- **Incremental Capacity Addition**: Additional modules can be added as demand grows.\n"
    "- **Economies of Series Production**: Cost reductions through standardized manufacturing."
)

# Variant comparison table
performance_metrics = get_performance_metrics()
variant_data = []

for variant, metrics in performance_metrics.items():
    if variant == 'small':
        vessel_height = HTGR_PARAMS.vessel_height_small
        vessel_diameter = HTGR_PARAMS.vessel_diameter_small
    elif variant == 'medium':
        vessel_height = HTGR_PARAMS.vessel_height_medium
        vessel_diameter = HTGR_PARAMS.vessel_diameter_medium
    else:  # large
        vessel_height = HTGR_PARAMS.vessel_height_large
        vessel_diameter = HTGR_PARAMS.vessel_diameter_large
        
    variant_data.append({
        "Parameter": f"{variant.capitalize()} Variant",
        "Thermal Power": f"{metrics['thermal_power']}",
        "Vessel Dimensions": f"{vessel_height} × {vessel_diameter} (H×D)",
        "Capital Cost": f"${metrics['capital_cost'].magnitude:,.0f}",
        "Annual Heat": f"{metrics['annual_heat_production'].magnitude:,.0f} MWh"
    })

df_variants = pd.DataFrame(variant_data)
display(Table(df_variants, "HTGR Variant Comparison", "tbl-variants"))

# Industrial Heat Applications
display(Title("# Industrial Heat Applications and Interfacing"))
display(
    "The HTGR is designed to provide heat for a wide range of industrial applications, "
    f"with the secondary {HTGR_PARAMS.secondary_fluid} loop delivering temperatures up to "
    f"{HTGR_PARAMS.secondary_max_temp}. This makes it suitable for various industrial processes "
    "that currently rely on fossil fuels."
    "\n\n"
    "### Compatible Industrial Processes"
    "\n\n"
    "- **Steam Generation**: For process heating, district heating, and desalination\n"
    "- **Chemical Processing**: Including ammonia production and methanol synthesis\n"
    "- **Oil Refining**: Process heat for various refining operations\n"
    "- **Paper Manufacturing**: Drying processes and steam generation\n"
    "- **Food Processing**: Sterilization, drying, and other thermal processes\n"
    "- **Hydrogen Production**: High-temperature electrolysis or thermochemical processes"
    "\n\n"
    "### Interface Systems"
    "\n\n"
    "The HTGR can deliver heat through various mediums depending on the industrial application:"
    "\n\n"
    "- **Steam Systems**: For processes requiring saturated or superheated steam\n"
    "- **Hot Air Systems**: For drying applications and certain chemical processes\n"
    "- **Thermal Oil Loops**: For precise temperature control in sensitive processes\n"
    "- **Direct CO₂ Utilization**: For processes that can use CO₂ directly"
    "\n\n"
    "Each interface is designed with isolation valves, monitoring systems, and heat exchangers "
    "to ensure safe and efficient heat transfer while maintaining separation between the "
    "nuclear and industrial systems."
)

# Manufacturing and Deployment
display(Title("# Manufacturing, Assembly, and Deployment"))
display(
    "The HTGR is designed for efficient manufacturing, transportation, and deployment, "
    "with a focus on minimizing on-site construction time and complexity."
    "\n\n"
    "### Manufacturing"
    "\n\n"
    "- **TRISO Fuel Production**: Specialized facilities for uranium kernel production, coating application, and quality control\n"
    "- **Core Components**: Precision manufacturing of graphite structures and control mechanisms\n"
    "- **Pressure Vessels**: Factory fabrication of reactor pressure vessel and containment structures\n"
    "- **Heat Exchangers**: Specialized manufacturing for high-temperature, high-pressure heat transfer equipment\n"
    "- **Instrumentation and Control**: Assembly and testing of digital control systems"
    "\n\n"
    "### Transportation and Site Requirements"
    "\n\n"
    "- **Module Dimensions**: All components sized for road or rail transportation\n"
    "- **Site Area**: Approximately 1-2 hectares depending on variant and number of modules\n"
    "- **Cooling Requirements**: Minimal cooling water requirements compared to conventional reactors\n"
    "- **Grid Connection**: Optional, as the system can operate in island mode for industrial applications\n"
    "- **Security Perimeter**: Standard nuclear security requirements with appropriate exclusion zones"
    "\n\n"
    "### Deployment Timeline"
    "\n\n"
    "- **Site Preparation**: 6-12 months\n"
    "- **Foundation and Support Structures**: 3-6 months\n"
    "- **Module Installation**: 6-12 months depending on variant\n"
    "- **System Integration and Testing**: 3-6 months\n"
    "- **Commissioning**: 3-4 months\n"
    "- **Total Timeline**: 18-36 months from site preparation to operation"
)

# Regulatory Compliance
display(Title("# Regulatory Compliance"))
display(
    "The HTGR design addresses regulatory requirements for nuclear facilities while "
    "incorporating features that simplify the licensing process compared to conventional "
    "nuclear plants."
    "\n\n"
    "### Key Regulatory Considerations"
    "\n\n"
    "- **Safety Case**: Based on inherent and passive safety features that eliminate many accident scenarios\n"
    "- **Emergency Planning Zone**: Potential for reduced emergency planning zone due to enhanced safety features\n"
    "- **Security Requirements**: Compliance with physical security regulations for nuclear facilities\n"
    "- **Environmental Impact**: Minimal water usage and no greenhouse gas emissions during operation\n"
    "- **Decommissioning**: Design features to facilitate eventual decommissioning and site restoration"
    "\n\n"
    "### Licensing Approach"
    "\n\n"
    "- **Pre-approved Design**: Standardized design to be pre-approved by regulatory authorities\n"
    "- **Site-specific Adaptations**: Limited to foundation design and industrial interfaces\n"
    "- **Operational Licensing**: Simplified procedures based on inherent safety characteristics\n"
    "- **International Harmonization**: Design compatible with IAEA standards and major national regulations"
)

# Performance Metrics
display(Title("# Performance Metrics and Efficiency Analysis"))

# Create performance metrics tables
metrics_data = []
for variant, metrics in performance_metrics.items():
    metrics_data.append({
        "Metric": f"{variant.capitalize()} Variant",
        "Thermal Power": f"{metrics['thermal_power']}",
        "Thermal Efficiency": f"{metrics['efficiency']:.2%}",
        "Potential Electrical Output": f"{metrics['electrical_potential']:.2f}",
        "Annual Heat Production": f"{metrics['annual_heat_production']:,.0f}",
        "LCOH ($/MWh)": f"${metrics['lcoh']:.2f}"
    })

df_metrics = pd.DataFrame(metrics_data)
display(Table(df_metrics, "HTGR Performance Metrics", "tbl-metrics"))

display(
    "The HTGR design achieves high thermal efficiency due to its elevated operating temperatures. "
    "While primarily designed for industrial heat applications, the system could potentially be "
    "adapted for electrical generation with appropriate power conversion systems."
    "\n\n"
    "### Key Performance Indicators"
    "\n\n"
    "- **Thermal Efficiency**: The high outlet temperature enables thermal efficiency significantly "
    "better than conventional light water reactors.\n"
    "- **Capacity Factor**: Expected to exceed 90% due to simplified design and reduced maintenance requirements.\n"
    "- **Levelized Cost of Heat (LCOH)**: Competitive with natural gas in many markets, especially "
    "with carbon pricing mechanisms.\n"
    "- **Operational Flexibility**: Capable of load following to match industrial demand patterns.\n"
    "- **Carbon Displacement**: Each 10 MW module can displace approximately 15,000-20,000 tons of CO₂ annually "
    "when replacing natural gas heating."
)

# Conclusion
display(Title("# Conclusion"))
display(
    "The modular HTGR design presented in this document offers a viable solution for "
    "decarbonizing industrial heat production across various sectors. By leveraging the "
    "inherent safety characteristics of TRISO fuel and high-temperature gas cooling, "
    "the system provides reliable, carbon-free heat at temperatures suitable for many "
    "industrial processes."
    "\n\n"
    "The scalable, modular approach allows for flexible deployment and incremental capacity "
    "addition, while the standardized design facilitates regulatory approval and reduces "
    "construction timelines. The system's passive safety features and multiple containment "
    "barriers ensure safe operation even under abnormal conditions."
    "\n\n"
    "With its ability to interface with existing industrial heat systems through various "
    "heat transfer mediums, the HTGR can be integrated into industrial facilities with "
    "minimal disruption to existing processes. This makes it an attractive option for "
    "industries seeking to reduce their carbon footprint while maintaining reliable "
    "high-temperature heat supply."
    "\n\n"
    "Further development and demonstration of this technology will be essential to validate "
    "the design concepts and establish a track record of safe, efficient operation in "
    "industrial settings."
)

print("DESIGN_COMPLETE")
print("HTGR design document generated successfully.")
