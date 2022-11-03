from typing import Final, Union

FASTEST_LAP: Final = {
  'vehicleIdx': 'uint8',
  'lapTime': 'float',
}

RETIREMENT: Final = {
  'vehicleIdx': 'uint8',
}

TEAM_MATE_IN_PITS: Final = {
  'vehicleIdx': 'uint8',
}

RACE_WINNER: Final = {
  'vehicleIdx': 'uint8',
}

PENALTY: Final = {
  'penaltyType': 'uint8',
  'infringementType': 'uint8',
  'vehicleIdx': 'uint8',
  'otherVehicleIdx': 'uint8',
  'time': 'uint8',
  'lapNum': 'uint8',
  'placesGained': 'uint8',
}

SPEED_TRAP: Final = {
  'vehicleIdx': 'uint8',
  'speed': 'float',
  'isOverallFastestInSession': 'uint8',
  'isDriverFastestInSession': 'uint8',
  'fastestVehicleIdxInSession': 'uint8',
  'fastestSpeedInSession': 'float',
}

START_LIGHTS: Final = {
  'numLights': 'uint8',
}

DRIVE_THROUGH_PENALTY_SERVED: Final = {
  'vehicleIdx': 'uint8',
}

STOP_GO_PENALTY_SERVED: Final = {
  'vehicleIdx': 'uint8',
}

FLASHBACK: Final = {
  'flashbackFrameIdentifier': 'uint32',
  'flashbackSessionTime': 'float',
}

BUTTONS: Final = {
  'buttonStatus': 'uint32',
}

PACKET: Final = {
  'eventStringCode': 4 * ['char'],
  'eventDetails': None,
}

EVENT_MESSAGE_DATA: Final = {
  'SSTA': None,
  'SEND': None,
  'FTLP': FASTEST_LAP,
  'RTMT': RETIREMENT,
  'DRSE': None,
  'DRSD': None,
  'TMPT': TEAM_MATE_IN_PITS,
  'CHQF': None,
  'RCWN': RACE_WINNER,
  'PENA': PENALTY,
  'SPTP': SPEED_TRAP,
  'STLG': START_LIGHTS,
  'LGOT': None,
  'DTSV': DRIVE_THROUGH_PENALTY_SERVED,
  'SGSV': STOP_GO_PENALTY_SERVED,
  'FLBK': FLASHBACK,
  'BUTN': BUTTONS,
}
