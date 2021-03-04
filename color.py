from enum import IntEnum

# Defines the way of coloring the forna container
# ABSOLUTE - uses the absolut values
# LOG - calculate a new logarithmic color scale to see little differences more clearly
# REGION - UTR / CDS / Introns coloring


class Color(IntEnum):
    ABSOLUTE = 1
    LOG = 2
    REGION = 3
