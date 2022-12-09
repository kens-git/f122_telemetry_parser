from typing import Tuple
from custom_types.basic import Char
from custom_types.generic import T


GridData = Tuple[
    T, T, T, T, T, T, T, T, T, T,
    T, T, T, T, T, T, T, T, T, T,
    T, T,
]
"""Defines a type to represent data for all drivers/vehicles on the grid."""

EventCode = Tuple[Char, Char, Char, Char]
"""Defines a 4 character event code."""


CarCornerData = Tuple[T, T, T, T]
"""Defines a type to hold the data for the 4 corners of car.

Typically used for tire and brake data.

The data is defined in this order:
0: Rear Left (RL)
1: Rear Right (RR)
2: Front Left (FL)
3: Front Right (FR)
"""


TyreStintData = Tuple[T, T, T, T, T, T, T, T]
"""Stores data for up to 8 tire stints."""


Name = Tuple[
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
    Char, Char, Char, Char, Char, Char, Char, Char,
]
"""Defines a type for names contained in the packets.

Can be up to 48 characters.
"""
