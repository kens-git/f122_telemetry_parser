import struct
from constants.data_types import DataType, DATA_TYPES

def unpack(data: bytearray, start: int, type: str) -> str:
  data_type = DATA_TYPES[type]
  return struct.unpack(f'<{data_type.format}',
    data[start:start + data_type.size])[0]
