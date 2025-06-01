# Small Modular Reactor (SMR) package
# High-Temperature Gas-cooled Reactor (HTGR) implementation

"""
Reactor package for Small Modular Reactor (SMR) designs
with focus on High-Temperature Gas-cooled Reactor (HTGR) implementation.
"""

import math
from pyforge import UREG

# Register custom units if needed
UREG.define('hour = 3600 * second')
