# Reactor design package initialization
print("Initializing reactor package")

# Import key components for easy access
from reactor.parameters_reactor import REACTOR_PARAMS
from reactor.parameters_thermal import THERMAL_PARAMS
from reactor.parameters_safety import SAFETY_PARAMS

# Avoid circular imports by not importing reactor_system here
# The modules that need it should import it directly
