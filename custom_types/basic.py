import abc
import dataclasses
import typing


class BasicType(abc.ABC):
    def __init__(self, value: typing.Any):
        self.value = value

    def __str__(self):
        return self.value.__str__()


class Char(BasicType):
    def __init__(self, value: str):
        if ord(value) < -128 or ord(value) > 127:
            raise ValueError(f'Char value out of range: {ord(value)}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Char):
            return False
        return self.value == rhs.value


class Double(BasicType):
    def __init__(self, value: float):
        if value < 1.7e-308 or value > 1.7e+308:
            raise ValueError(f'Double value out of range: {value}')
        super().__init__(value)

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Double):
            return False
        return self.value == rhs.value


class Float(BasicType):
    def __init__(self, value: float):
        if value < 1.23-38 or value > 3.4e+38:
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


@dataclasses.dataclass
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
