from constants.data_types import DATA_TYPES
from utilities.data import unpack

def parse_value(data: bytearray, type: str, index: int) -> tuple[str, int]:
  return (unpack(data, index, type), DATA_TYPES[type].size)

# TODO: refactor, almost duplicate of parse_dict
def parse_list(data: bytearray, format: list, index: int) -> tuple[list, int]:
  parsed_data = []
  total_data_size = 0
  for item in format:
    # TODO: refactor, each statement results in basically the same computation
    if isinstance(item, str):
      (value, data_size) = parse_value(data, item, index + total_data_size)
      parsed_data.append(value)
      total_data_size += data_size
    elif isinstance(item, list):
      (parsed_list, data_size) = parse_list(data, item, index + total_data_size)
      parsed_data.append(parsed_list)
      total_data_size += data_size
    elif isinstance(item, dict):
      (parsed_dict, data_size) = parse_dict(data, item, index + total_data_size)
      parsed_data.append(parsed_dict)
      total_data_size += data_size
    else:
      raise RuntimeError(f'Expected str, list, or dict, got: {type(format)}')
  return (parsed_data, total_data_size)

def parse_dict(data: bytearray, format: dict, index: int) -> tuple[dict, int]:
  parsed_data = {}
  total_data_size = 0
  for key, value in format.items():
    if isinstance(value, str):
      (value, data_size) = parse_value(data, value, index + total_data_size)
      parsed_data[key] = value
      total_data_size += data_size
    elif isinstance(value, list):
      (parsed_list, data_size) = parse_list(data, value, index + total_data_size)
      parsed_data[key] = parsed_list
      total_data_size += data_size
    elif isinstance(value, dict):
      (parsed_dict, data_size) = parse_dict(data, value, index + total_data_size)
      parsed_data[key] = parsed_dict
      total_data_size += data_size
    elif value is None:
      pass
    else:
      raise RuntimeError(f'Expected str, list, or dict, got: {type(format)}')
  return (parsed_data, total_data_size)

def parse(data: bytearray, format: any):
  return parse_dict(data, format, 0)[0]
