from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Final, Type

FLOAT_MIN: Final[float] = -340282346638528859811704183484516925440
"""The minimum value a Float can represent."""

FLOAT_MAX: Final[float] = 340282346638528859811704183484516925440
"""The maximum value a Float can represent."""

DOUBLE_MIN: Final[float] = -179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368  # noqa
"""The minimum value a Double can represent."""

DOUBLE_MAX: Final[float] = 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368  # noqa
"""The maximum value a Double can represent."""


class BasicType(ABC):
    """Defines an immutable type analogous to C/C++ fundamental types.

    Provides the semantics of fixed-size types.

    Attributes:
        value: The current value of the BasicType instance.
    """

    def __init__(self, value: Any):
        """
        Args:
            value: The value of the BasicType instance.
        """
        self.value: Final[Any] = value

    def __str__(self):
        """Returns the human-readable string representation of the value."""
        return self.value.__str__()


class Char(BasicType):
    """Defines a 1 byte char type.

    Chars are implementation specific, but the values in the packets
    appear to be unsigned and so this implementation assumes the
    ordinal values are between 0 and 255.
    """

    def __init__(self, value: str):
        if ord(value) < 0 or ord(value) > 255:
            raise ValueError(
                f'Char value out of range: {ord(value)} ({value})')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Char):
            return False
        return self.value == rhs.value


class Double(BasicType):
    """Defines an 8 byte double type."""

    def __init__(self, value: float):
        if value < DOUBLE_MIN or value > DOUBLE_MAX:
            raise ValueError(f'Double value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Double):
            return False
        return self.value == rhs.value


class Float(BasicType):
    """Defines a 4 byte float type."""

    def __init__(self, value: float):
        if value < FLOAT_MIN or value > FLOAT_MAX:
            raise ValueError(f'Float value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Float):
            return False
        return self.value == rhs.value


class Int8(BasicType):
    """Defines a 1 byte int type."""

    def __init__(self, value: int):
        if value < -128 or value > 127:
            raise ValueError(f'Int8 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int8):
            return False
        return self.value == rhs.value


class UInt8(BasicType):
    """Defines a 1 byte unsigned int type."""

    def __init__(self, value: int):
        if value < 0 or value > 255:
            raise ValueError(f'UInt8 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt8):
            return False
        return self.value == rhs.value


class Int16(BasicType):
    """Defines a 2 byte int type."""
    def __init__(self, value: int):
        if value < -32768 or value > 32767:
            raise ValueError(f'Int16 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int16):
            return False
        return self.value == rhs.value


class UInt16(BasicType):
    """Defines a 2 byte unsigned int type."""
    def __init__(self, value: int):
        if value < 0 or value > 65535:
            raise ValueError(f'UInt16 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt16):
            return False
        return self.value == rhs.value


class Int32(BasicType):
    """Defines a 4 byte int type."""

    def __init__(self, value: int):
        if value < -2147483648 or value > 2147483647:
            raise ValueError(f'Int32 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int32):
            return False
        return self.value == rhs.value


class UInt32(BasicType):
    """Defines a 4 byte unsigned int type."""
    def __init__(self, value: int):
        if value < 0 or value > 4294967295:
            raise ValueError(f'UInt32 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt32):
            return False
        return self.value == rhs.value


class Int64(BasicType):
    """Defines an 8 byte int type."""
    def __init__(self, value: int):
        if value < -9223372036854775808 or value > 9223372036854775807:
            raise ValueError(f'Int64 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int64):
            return False
        return self.value == rhs.value


class UInt64(BasicType):
    """Defines an 8 byte unsigned int type."""

    def __init__(self, value: int):
        if value < 0 or value > 18446744073709551615:
            raise ValueError(f'UInt64 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt64):
            return False
        return self.value == rhs.value


@dataclass
class DataFormat:
    """Stores a BasicType's format character and byte size.

    The format character is used when unpacking (converting) bytes/bytestrings
    to a another type and identifies what type is encoded in the bytes.
    """

    format: str
    size: int


BASIC_TYPE_FORMAT: Final[Dict[Type[BasicType], DataFormat]] = {
    BasicType: DataFormat('', 0),
    Char: DataFormat('c', 1),
    Double: DataFormat('d', 8),
    Float: DataFormat('f', 4),
    Int8: DataFormat('b', 1),
    UInt8: DataFormat('B', 1),
    Int16: DataFormat('h', 2),
    UInt16: DataFormat('H', 2),
    Int32: DataFormat('i', 4),
    UInt32: DataFormat('I', 4),
    Int64: DataFormat('q', 8),
    UInt64: DataFormat('Q', 8),
}
"""Associates a BasicType with its DataFormat."""
