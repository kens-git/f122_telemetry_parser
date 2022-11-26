import abc
import dataclasses
import typing

# TODO: investigate ways to just refer to instances as just their name,
#       instead of 'instance.value'.
class BasicType(abc.ABC):
    def __init__(self, value: typing.Any):
        self.value = value

    def __str__(self):
        return self.value.__str__()


class Char(BasicType):
    def __init__(self, value: str):
        super().__init__(value)


class Double(BasicType):
    def __init__(self, value: float):
        super().__init__(value)


class Float(BasicType):
    def __init__(self, value: float):
        super().__init__(value)


class Int8(BasicType):
    def __init__(self, value: int):
        if value < -128 or value > 127:
            raise ValueError('blah')
        super().__init__(value)


class UInt8(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


class Int16(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


class UInt16(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


class Int32(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


class UInt32(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


class Int64(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


class UInt64(BasicType):
    def __init__(self, value: int):
        super().__init__(value)


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
