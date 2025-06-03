"""
Reactor package for High-Temperature Gas-cooled Reactor (HTGR) designs
focused on industrial heat applications.

This package provides tools for designing, simulating, and analyzing
modular HTGR systems with TRISO fuel particles and helium coolant.
"""

from pyforge import UREG

# Time units
UREG.define('hour = 3600 * second')
UREG.define('day = 24 * hour')
UREG.define('year = 365.25 * day')
UREG.define('EFPD = day')  # Effective Full Power Days
UREG.define('cycle = year')  # Reactor operating cycle

# Nuclear fuel units
UREG.define('gU = gram')  # Grams of uranium
UREG.define('kgU = 1000 * gU')  # Kilograms of uranium
UREG.define('tHM = 1000 * kg')  # Tons of heavy metal
UREG.define('atom_percent = 0.01 * count / count')  # Atomic percent
UREG.define('wt_percent = 0.01 * mass / mass')  # Weight percent
UREG.define('ppm = 1e-6 * count / count')  # Parts per million
UREG.define('ppb = 1e-9 * count / count')  # Parts per billion

# Energy and power units
UREG.define('MWth = 1e6 * watt')  # Megawatt thermal
UREG.define('MWe = 1e6 * watt')  # Megawatt electric
UREG.define('GWd = 1e9 * watt * day')  # Gigawatt-days
UREG.define('GWd_per_tHM = GWd/tHM')  # Burnup unit
UREG.define('kWh = kilowatt * hour')  # Kilowatt-hour
UREG.define('MWh = megawatt * hour')  # Megawatt-hour
UREG.define('GWh = gigawatt * hour')  # Gigawatt-hour

# Reactivity units
UREG.define('pcm = 1e-5 * dimensionless')  # Per cent mille (reactivity)
UREG.define('dollar = dimensionless')  # Reactivity unit (1 dollar = delayed neutron fraction)
UREG.define('beta_eff = dimensionless')  # Effective delayed neutron fraction
UREG.define('inhour = dimensionless')  # Reactor period unit

# Radiation units
UREG.define('Bq = 1/second')  # Becquerel (activity)
UREG.define('Ci = 3.7e10 * Bq')  # Curie (activity)
UREG.define('Gy = joule/kg')  # Gray (absorbed dose)
UREG.define('Sv = joule/kg')  # Sievert (equivalent dose)
UREG.define('rem = 0.01 * Sv')  # Roentgen equivalent man
UREG.define('microsievert = 1e-6 * Sv')  # Microsievert
UREG.define('millisievert = 1e-3 * Sv')  # Millisievert
UREG.define('μSv = microsievert')  # Alias
UREG.define('mSv = millisievert')  # Alias
UREG.define('man_Sv = Sv')  # Collective dose

# Temperature units
UREG.define('delta_degC = kelvin')  # Temperature difference in Celsius
UREG.define('delta_K = kelvin')  # Temperature difference in Kelvin
UREG.define('delta_degF = delta_degC * 9/5')  # Temperature difference in Fahrenheit

# Pressure units
UREG.define('MPa = 1e6 * pascal')  # Megapascal
UREG.define('kPa = 1e3 * pascal')  # Kilopascal
UREG.define('bar = 1e5 * pascal')  # Bar
UREG.define('psi = 6894.76 * pascal')  # Pounds per square inch
UREG.define('atm = 101325 * pascal')  # Standard atmosphere

# Heat transfer units
UREG.define('W_per_m2K = watt / (meter**2 * kelvin)')  # Heat transfer coefficient
UREG.define('W_per_mK = watt / (meter * kelvin)')  # Thermal conductivity
UREG.define('kJ_per_kgK = kilojoule / (kilogram * kelvin)')  # Specific heat capacity
UREG.define('BTU_per_hr_ft2_F = 5.678 * W_per_m2K')  # BTU heat transfer coefficient

# Flow units
UREG.define('kg_per_s = kilogram / second')  # Mass flow rate
UREG.define('m3_per_s = meter**3 / second')  # Volumetric flow rate
UREG.define('kg_per_m2s = kilogram / (meter**2 * second)')  # Mass flux
UREG.define('SCFM = 0.000471947 * m3_per_s')  # Standard cubic feet per minute
UREG.define('ACFM = 0.000471947 * m3_per_s')  # Actual cubic feet per minute

# Safety and monitoring units
UREG.define('Richter = dimensionless')  # Earthquake scale
UREG.define('INES = dimensionless')  # International Nuclear Event Scale
UREG.define('LOCA = dimensionless')  # Loss of Coolant Accident scale
UREG.define('CDF = 1/year')  # Core Damage Frequency
UREG.define('LERF = 1/year')  # Large Early Release Frequency

# Define delta_k for reactivity
UREG.define('delta_k = dimensionless')  # Change in multiplication factor
print("DEBUG: Added delta_k unit definition to unit registry")
UREG.define('k_eff = dimensionless')  # Effective multiplication factor

# TRISO fuel specific units
UREG.define('particles_per_cm3 = count / centimeter**3')  # Particle packing density
UREG.define('FIMA = dimensionless')  # Fissions per Initial Metal Atom
UREG.define('kernel_diameter = micrometer')  # Fuel kernel diameter
UREG.define('packing_fraction = dimensionless')  # TRISO packing fraction
UREG.define('coating_thickness = micrometer')  # TRISO coating layer thickness

# Helium coolant specific units
UREG.define('He_fraction = dimensionless')  # Helium fraction in coolant
UREG.define('void_fraction = dimensionless')  # Void fraction
UREG.define('Reynolds = dimensionless')  # Reynolds number
UREG.define('Prandtl = dimensionless')  # Prandtl number
UREG.define('Nusselt = dimensionless')  # Nusselt number

# Industrial heat application units
UREG.define('steam_quality = dimensionless')  # Steam quality
UREG.define('process_heat_temp = degC')  # Process heat temperature
UREG.define('thermal_efficiency = dimensionless')  # Thermal efficiency
UREG.define('capacity_factor = dimensionless')  # Capacity factor
UREG.define('availability = dimensionless')  # System availability


# Print initialization message
print("HTGR reactor package initialized with nuclear engineering units")
print("Configured for industrial heat applications with TRISO fuel and helium coolant")
print("DEBUG: Unit registry initialized with all required units including reactivity units")
