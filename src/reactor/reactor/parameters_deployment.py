"""
Deployment parameters for the High-Temperature Gas-cooled Reactor (HTGR).
Defines key parameters for manufacturing, installation, and site requirements.
"""

from pyforge import Parameters, Quantity
from reactor import UREG

class DeploymentParameters(Parameters):
    """Define all the key parameters for HTGR deployment."""
    
    # Module dimensions
    module_dimensions: str = "Max 5m × 4.5m × 12m"
    max_module_weight: Quantity = Quantity(120, "tonne")
    
    # Construction timeline
    construction_time: Quantity = Quantity(36, "month")
    
    # Site requirements
    site_area: Quantity = Quantity(10000, "m^2")
    small_footprint: Quantity = Quantity(5000, "m^2")
    medium_footprint: Quantity = Quantity(7500, "m^2")
    large_footprint: Quantity = Quantity(10000, "m^2")
    
    # Economic parameters
    capital_cost_per_kw: float = 4500  # $/kW thermal
    annual_om_cost_per_kw: float = 150  # $/kW thermal/year

# Single source of truth
DEPLOYMENT_PARAMS = DeploymentParameters()

# Print key parameters for verification
print(f"Module dimensions: {DEPLOYMENT_PARAMS.module_dimensions}")
print(f"Construction time: {DEPLOYMENT_PARAMS.construction_time}")
print(f"Site area: {DEPLOYMENT_PARAMS.site_area}")
print("Deployment parameters loaded successfully")
