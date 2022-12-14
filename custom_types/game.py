from ctypes import c_char, c_uint8, LittleEndianStructure
from typing import Generic
from custom_types.generic import CT


class F1PacketStructure(LittleEndianStructure):
    _pack_ = 1


EventCode = c_uint8 * 4
"""Defines a 4 character event code."""


Name = c_char * 48
"""Defines a type for names contained in the packets (UTF-8)."""


# TODO: make work
# TyreStintData: Array[CT * 8]
"""Stores data for up to 8 tire stints."""


# TODO: make work
# class CarCornerData(LittleEndianStructure, Generic[CT]):
#     _fields_ = [
#         ('rearLeft', CT),
#         ('rearRight', CT),
#         ('frontLeft', CT),
#         ('frontRight', CT),
#     ]
