from abc import ABC
from dataclasses import dataclass
from typing import Any, Final


FLOAT_MIN: Final[float] = -340282346638528859811704183484516925440
FLOAT_MAX: Final[float] = 340282346638528859811704183484516925440
DOUBLE_MIN: Final[float] = -179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368  # noqa
DOUBLE_MAX: Final[float] = 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368  # noqa


class BasicType(ABC):
    def __init__(self, value: Any):
        self.value = value

    def __str__(self):
        return self.value.__str__()


class Char(BasicType):
    def __init__(self, value: str):
        # Note: chars are implementation specific, but these appear to be
        #       unsigned.
        if ord(value) < 0 or ord(value) > 255:
            raise ValueError(
                f'Char value out of range: {ord(value)} ({value})')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Char):
            return False
        return self.value == rhs.value


class Double(BasicType):
    def __init__(self, value: float):
        if value < DOUBLE_MIN or value > DOUBLE_MAX:
            raise ValueError(f'Double value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Double):
            return False
        return self.value == rhs.value


class Float(BasicType):
    def __init__(self, value: float):
        if value < FLOAT_MIN or value > FLOAT_MAX:
            raise ValueError(f'Float value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Float):
            return False
        return self.value == rhs.value


class Int8(BasicType):
    def __init__(self, value: int):
        if value < -128 or value > 127:
            raise ValueError(f'Int8 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int8):
            return False
        return self.value == rhs.value


class UInt8(BasicType):
    def __init__(self, value: int):
        if value < 0 or value > 255:
            raise ValueError(f'UInt8 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt8):
            return False
        return self.value == rhs.value


class Int16(BasicType):
    def __init__(self, value: int):
        if value < -32768 or value > 32767:
            raise ValueError(f'Int16 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int16):
            return False
        return self.value == rhs.value


class UInt16(BasicType):
    def __init__(self, value: int):
        if value < 0 or value > 65535:
            raise ValueError(f'UInt16 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt16):
            return False
        return self.value == rhs.value


class Int32(BasicType):
    def __init__(self, value: int):
        if value < -2147483648 or value > 2147483647:
            raise ValueError(f'Int32 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int32):
            return False
        return self.value == rhs.value


class UInt32(BasicType):
    def __init__(self, value: int):
        if value < 0 or value > 4294967295:
            raise ValueError(f'UInt32 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, UInt32):
            return False
        return self.value == rhs.value


class Int64(BasicType):
    def __init__(self, value: int):
        if value < -9223372036854775808 or value > 9223372036854775807:
            raise ValueError(f'Int64 value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Int64):
            return False
        return self.value == rhs.value


class UInt64(BasicType):
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
    format: str
    size: int


BASIC_TYPE_FORMAT = {
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
