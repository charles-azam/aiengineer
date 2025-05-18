"""
Licensing analysis tools for the Small Modular Reactor project.
Provides functions to analyze regulatory requirements and licensing timeline.
"""

from reactor.parameters_reactor import REACTOR_PARAMS, CONTAINMENT_PARAMS

def analyze_regulatory_requirements():
    """
    Analyze the regulatory requirements for licensing the SMR.
    Returns a dictionary with key regulatory areas and their status.
    """
    # Key reactor parameters
    thermal_power = REACTOR_PARAMS.thermal_power.magnitude  # MW
    electrical_power = REACTOR_PARAMS.electrical_power.magnitude  # MW
    fuel_enrichment = REACTOR_PARAMS.fuel_enrichment.magnitude  # %
    
    # Define regulatory requirements for different jurisdictions
    regulatory_requirements = {
        "US NRC": {
            "Design Certification": {
                "requirements": [
                    "10 CFR Part 52 Subpart B - Standard Design Certifications",
                    "NUREG-0800 Standard Review Plan",
                    "Regulatory Guide 1.206 - Combined License Applications"
                ],
                "estimated_time": 42,  # months
                "key_challenges": [
                    "First-of-a-kind design review",
                    "Demonstration of passive safety systems",
                    "Digital instrumentation and control qualification"
                ],
                "status": "Ready for application"
            },
            "Environmental Review": {
                "requirements": [
                    "10 CFR Part 51 - Environmental Protection",
                    "NUREG-1555 - Environmental Standard Review Plan"
                ],
                "estimated_time": 24,  # months
                "key_challenges": [
                    "Site-specific environmental impact assessment",
                    "Public consultation process"
                ],
                "status": "Generic Environmental Impact Statement needed"
            },
            "Security Requirements": {
                "requirements": [
                    "10 CFR Part 73 - Physical Protection",
                    "Regulatory Guide 5.76 - Physical Security"
                ],
                "estimated_time": 18,  # months
                "key_challenges": [
                    "Adaptation of security requirements for smaller facility",
                    "Cyber security compliance"
                ],
                "status": "Security design concept developed"
            }
        },
        "IAEA": {
            "Safety Standards": {
                "requirements": [
                    "SSR-2/1 Safety of Nuclear Power Plants: Design",
                    "SSG-30 Safety Classification of Structures, Systems and Components"
                ],
                "estimated_time": 36,  # months
                "key_challenges": [
                    "Demonstration of defense-in-depth",
                    "International harmonization of requirements"
                ],
                "status": "Design aligns with requirements"
            }
        }
    }
    
    # Special considerations for HALEU fuel
    if fuel_enrichment > 5.0:
        regulatory_requirements["US NRC"]["Fuel Qualification"] = {
            "requirements": [
                "NUREG-0800 Section 4.2 - Fuel System Design",
                "ATF-ISG-2020-01 - Licensing of HALEU fuels"
            ],
            "estimated_time": 36,  # months
            "key_challenges": [
                "Limited operational experience with HALEU",
                "Need for additional irradiation testing",
                "Special handling and transportation requirements"
            ],
            "status": "Additional testing required"
        }
    
    print("\n=== REGULATORY REQUIREMENTS ANALYSIS ===")
    
    for jurisdiction, areas in regulatory_requirements.items():
        print(f"\n{jurisdiction} Requirements:")
        for area, details in areas.items():
            print(f"  {area}:")
            print(f"    Status: {details['status']}")
            print(f"    Estimated Time: {details['estimated_time']} months")
            print(f"    Key Challenges:")
            for challenge in details['key_challenges']:
                print(f"      - {challenge}")
    
    return regulatory_requirements

def estimate_licensing_timeline():
    """
    Estimate the timeline for obtaining regulatory approvals.
    Returns a dictionary with licensing milestones and their estimated completion times.
    """
    # Base timeline estimates (in months from project start)
    licensing_timeline = {
        "Pre-application Engagement": {
            "start": 0,
            "duration": 12,
            "end": 12,
            "key_activities": [
                "Regulatory framework discussions",
                "Pre-application white papers",
                "Methodology approvals"
            ],
            "responsible_party": "Reactor Vendor & Utility"
        },
        "Design Certification Application": {
            "start": 12,
            "duration": 6,
            "end": 18,
            "key_activities": [
                "Preparation of Design Control Document",
                "Safety analysis report compilation",
                "Application submission"
            ],
            "responsible_party": "Reactor Vendor"
        },
        "Design Certification Review": {
            "start": 18,
            "duration": 36,
            "end": 54,
            "key_activities": [
                "Acceptance review",
                "Requests for additional information",
                "Advisory committee review",
                "Rulemaking"
            ],
            "responsible_party": "Regulatory Body"
        },
        "Combined License Application": {
            "start": 36,
            "duration": 12,
            "end": 48,
            "key_activities": [
                "Site-specific design adaptation",
                "Environmental report",
                "Application submission"
            ],
            "responsible_party": "Utility"
        },
        "Combined License Review": {
            "start": 48,
            "duration": 24,
            "end": 72,
            "key_activities": [
                "Safety evaluation",
                "Environmental impact statement",
                "Public hearings",
                "License issuance"
            ],
            "responsible_party": "Regulatory Body"
        },
        "ITAAC Completion": {
            "start": 72,
            "duration": 36,
            "end": 108,
            "key_activities": [
                "Construction verification",
                "Testing program",
                "Operational programs implementation"
            ],
            "responsible_party": "Utility & Reactor Vendor"
        },
        "Fuel Load Authorization": {
            "start": 108,
            "duration": 3,
            "end": 111,
            "key_activities": [
                "Final safety analysis",
                "Operational readiness review",
                "Authorization issuance"
            ],
            "responsible_party": "Regulatory Body"
        }
    }
    
    # Calculate critical path
    critical_path_end = max(milestone["end"] for milestone in licensing_timeline.values())
    
    print("\n=== LICENSING TIMELINE ANALYSIS ===")
    print(f"Total Licensing Timeline: {critical_path_end} months ({critical_path_end/12:.1f} years)")
    
    print("\nKey Licensing Milestones:")
    for milestone, details in licensing_timeline.items():
        print(f"  {milestone}:")
        print(f"    Timeline: Month {details['start']} to Month {details['end']} ({details['duration']} months)")
        print(f"    Responsible: {details['responsible_party']}")
    
    print("\nCritical Path Activities:")
    for milestone, details in licensing_timeline.items():
        if details["end"] == critical_path_end:
            print(f"  - {milestone} (End: Month {details['end']})")
    
    return {
        "timeline": licensing_timeline,
        "total_duration": critical_path_end
    }

def analyze_licensing_risks():
    """
    Analyze potential licensing risks and mitigation strategies.
    Returns a dictionary with risk areas and their assessment.
    """
    # Define licensing risk areas
    licensing_risks = {
        "Novel Technology Features": {
            "risk_level": "Medium",
            "description": "Passive safety systems may require additional testing and validation",
            "mitigation": "Comprehensive testing program and scaled prototype demonstration",
            "impact_on_timeline": "6-12 months potential delay"
        },
        "HALEU Fuel Qualification": {
            "risk_level": "High",
            "description": "Limited operational experience with HALEU fuel above 5% enrichment",
            "mitigation": "Early engagement with regulators and additional irradiation testing program",
            "impact_on_timeline": "12-24 months potential delay"
        },
        "Digital Instrumentation & Control": {
            "risk_level": "Medium",
            "description": "Regulatory acceptance of digital I&C systems for safety functions",
            "mitigation": "Use of previously approved platforms and defense-in-depth architecture",
            "impact_on_timeline": "3-9 months potential delay"
        },
        "Seismic Design Qualification": {
            "risk_level": "Low",
            "description": "Demonstration of seismic isolation effectiveness",
            "mitigation": "Comprehensive testing and analysis program with margin demonstration",
            "impact_on_timeline": "0-3 months potential delay"
        },
        "Security Requirements": {
            "risk_level": "Medium",
            "description": "Adaptation of security requirements for smaller facility footprint",
            "mitigation": "Early engagement with regulators on alternative security approaches",
            "impact_on_timeline": "3-6 months potential delay"
        }
    }
    
    print("\n=== LICENSING RISK ANALYSIS ===")
    
    high_risks = []
    medium_risks = []
    low_risks = []
    
    for risk, details in licensing_risks.items():
        if details["risk_level"] == "High":
            high_risks.append(risk)
        elif details["risk_level"] == "Medium":
            medium_risks.append(risk)
        else:
            low_risks.append(risk)
    
    print(f"\nHigh Risk Areas ({len(high_risks)}):")
    for risk in high_risks:
        details = licensing_risks[risk]
        print(f"  {risk}:")
        print(f"    Description: {details['description']}")
        print(f"    Mitigation: {details['mitigation']}")
        print(f"    Timeline Impact: {details['impact_on_timeline']}")
    
    print(f"\nMedium Risk Areas ({len(medium_risks)}):")
    for risk in medium_risks:
        details = licensing_risks[risk]
        print(f"  {risk}:")
        print(f"    Description: {details['description']}")
        print(f"    Mitigation: {details['mitigation']}")
    
    print(f"\nLow Risk Areas ({len(low_risks)}):")
    for risk in low_risks:
        print(f"  - {risk}")
    
    # Calculate overall risk assessment
    if len(high_risks) >= 2:
        overall_risk = "High"
    elif len(high_risks) == 1 or len(medium_risks) >= 3:
        overall_risk = "Medium-High"
    elif len(medium_risks) >= 1:
        overall_risk = "Medium"
    else:
        overall_risk = "Low"
    
    print(f"\nOverall Licensing Risk Assessment: {overall_risk}")
    
    return {
        "risks": licensing_risks,
        "high_risks": high_risks,
        "medium_risks": medium_risks,
        "low_risks": low_risks,
        "overall_risk": overall_risk
    }

# Run licensing analysis
if __name__ != "__main__":  # This ensures it runs when imported but not when executed directly
    print("Initializing licensing analysis tools")
    regulatory_requirements = analyze_regulatory_requirements()
    licensing_timeline = estimate_licensing_timeline()
    licensing_risks = analyze_licensing_risks()
