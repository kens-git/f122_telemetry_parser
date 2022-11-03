from typing import Final

# TODO: make sure naming is correct
DATA: Final = {
  'speed': 'uint16',
  'throttle': 'float',
  'steer': 'float',
  'brake': 'float',
  'clutch': 'uint8',
  'gear': 'int8',
  'engineRPM': 'uint16',
  'drs': 'uint8',
  'revLightsPercent': 'uint8',
  'revLightsBitValue': 'uint16',
  'brakesTemperature': 4 * ['uint16'],
  'tiresSurfaceTemperature': 4 * ['uint8'],
  'tiresInnerTemperature': 4 * ['uint8'],
  'engineTemperature': 'uint16',
  'tiresPressure': 4 * ['float'],
  'surfaceType': 4 * ['uint8'],
}

PACKET: Final = {
  'carTelemetryData': 22 * [DATA],
  'mfdPanelIndex': 'uint8',
  'mfdPanelIndexSecondaryPlayer': 'uint8',
  'suggestedGear': 'int8',
}
