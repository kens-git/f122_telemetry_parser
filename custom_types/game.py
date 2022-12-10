from ctypes import c_char, LittleEndianStructure
from typing import Generic
from custom_types.generic import CT


EventCode = c_char * 4
"""Defines a 4 character event code."""


Name = c_char * 48
"""Defines a type for names contained in the packets."""


TyreStintData = [CT, CT, CT, CT, CT, CT, CT, CT]
"""Stores data for up to 8 tire stints."""


class CarCornerData(LittleEndianStructure, Generic[CT]):
    _fields_ = [
        ('rearLeft', CT),
        ('rearRight', CT),
        ('frontLeft', CT),
        ('frontRight', CT),
    ]
