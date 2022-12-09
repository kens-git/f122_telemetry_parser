import struct
from typing import Tuple, Type
from custom_types.basic import BASIC_TYPE_FORMAT, BasicType, Char


def unpack(data: bytes, start: int,
           data_type: Type[BasicType]) -> BasicType:
    """Unpacks a specific value from the given bytes.

    Args:
        data: The data to unpack the value from.
        start: The index within data to being unpacking from.
        data_type: The data type to unpack.

    Returns:
        A BasicType containing the unpacked data.
    """

    data_format = BASIC_TYPE_FORMAT[data_type]
    return data_type(struct.unpack(f'<{data_format.format}',
                     data[start:start + data_format.size])[0])


def to_string(chars: Tuple[Char, ...]) -> str:
    """Converts a tuple of Chars to a string by decoding the chars as utf-8.

    Args:
        chars: The chars to convert.

    Returns:
        A plain string containing the non-null characters of the chars.
    """

    return (b''.join(x.value for x in chars)).decode('utf-8').rstrip('\u0000')
