from ctypes import (
    c_char, c_double, c_float, c_int8, c_int16, c_int32, c_int64, c_uint8,
    c_uint16, c_uint32, c_uint64)
from typing import TypeVar


T = TypeVar('T')
"""Generic type used as a placeholder for some other type."""

C_TYPES = (c_char | c_double | c_float | c_int8 | c_int16 | c_int32 |
           c_int64 | c_uint8 | c_uint16 | c_uint32 | c_uint64)

CT = TypeVar('CT', bound=C_TYPES)
"""Generic type bound to a LittleEndianStructure."""
