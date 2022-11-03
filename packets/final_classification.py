from typing import Final

DATA: Final = {
  'position': 'uint8',
  'numLaps': 'uint8',
  'gridPosition': 'uint8',
  'points': 'uint8',
  'numPitStops': 'uint8',
  'resultStatus': 'uint8',
  'bestLapTimeInMS': 'uint32',
  'totalRaceTime': 'double',
  'penaltiesTime': 'uint8',
  'numPenalties': 'uint8',
  'numTyreStints': 'uint8',
  'tyreStintsActual': 8 * ['uint8'],
  'tyreStintsVisual': 8 * ['uint8'],
  'tyreStintEndLaps': 8 * ['uint8'],
}

PACKET: Final = {
  'numCars': 'uint8',
  'classificationData': 22 * [DATA]
}
