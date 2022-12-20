from ctypes import c_char, c_uint8, LittleEndianStructure


class F1PacketStructure(LittleEndianStructure):
    """Base class that defines the endianness and data packing for packets."""

    _pack_ = 1


EventCode = c_uint8 * 4
"""Defines a 4 character event code."""


Name = c_char * 48
"""Defines a type for names contained in the packets (UTF-8)."""
