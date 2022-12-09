import struct
from typing import Tuple, Type
from custom_types.basic import BASIC_TYPE_FORMAT, BasicType, Char


def unpack(data: bytes, start: int,
           data_type: Type[BasicType]) -> BasicType:
    data_format = BASIC_TYPE_FORMAT[data_type]
    return data_type(struct.unpack(f'<{data_format.format}',
                     data[start:start + data_format.size])[0])


def to_string(chars: Tuple[Char, ...]) -> str:
    return (b''.join(x.value for x in chars)).decode('utf-8').rstrip('\u0000')
