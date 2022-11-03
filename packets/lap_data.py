from typing import Final

DATA: Final = {
  'lastLapTimeInMS': 'uint32',
  'currentLapTimeInMS': 'uint32',
  'sector1TimeInMS': 'uint16',
  'sector2TimeInMS': 'uint16',
  'lapDistance': 'float',
  'totalDistance': 'float',
  'safetyCarDelta': 'float',
  'carPosition': 'uint8',
  'currentLapNum': 'uint8',
  'pitStatus': 'uint8',
  'numPitStops': 'uint8',
  'sector': 'uint8',
  'currentLapInvalid': 'uint8',
  'penalties': 'uint8',
  'warnings': 'uint8',
  'numUnservedDriveThroughPens': 'uint8',
  'numUnservedStopGoPens': 'uint8',
  'gridPosition': 'uint8',
  'driverStatus': 'uint8',
  'resultStatus': 'uint8',
  'pitLaneTimerActive': 'uint8',
  'pitLaneTimeInLaneInMS': 'uint16',
  'pitStopTimerInMS': 'uint16',
  'pitStopShouldServePen': 'uint8',
}

PACKET: Final = {
  'lapData': 22 * [DATA],
  'timeTrialPBCarIdx': 'uint8',
  'timeTrialRivalCarIdx': 'uint8',
}
