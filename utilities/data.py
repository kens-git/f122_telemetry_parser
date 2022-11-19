import struct
import typing
import custom_types.basic as bt


def unpack(data: bytes, start: int,
           data_type: typing.Type[bt.BasicType]) -> bt.BasicType:
    data_format = bt.BASIC_TYPE_FORMAT[data_type]
    return data_type(struct.unpack(f'<{data_format.format}',
                     data[start:start + data_format.size])[0])


def to_string(chars: typing.Tuple[bt.Char, ...]) -> str:
    return ''.join([x.value.decode() for x in chars])
