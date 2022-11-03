from typing import Final

class DataType:
  def __init__(self, format: str, size: int):
    self.format = format
    self.size = size

DATA_TYPES: Final = {
  'int8': DataType('b', 1),
  'uint8': DataType('B', 1),
  'char': DataType('c', 1),
  'double': DataType('d', 8),
  'float': DataType('f', 4),
  'int16': DataType('h', 2),
  'uint16': DataType('H', 2),
  'int32': DataType('i', 4),
  'uint32': DataType('I', 4),
  'int64': DataType('q', 8),
  'uint64': DataType('Q', 8),
}
