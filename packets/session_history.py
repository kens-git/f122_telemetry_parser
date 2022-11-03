from typing import Final

LAP_HISTORY_DATA: Final = {
  'lapTimeInMS': 'uint32',
  'sector1TimeInMS': 'uint16',
  'sector2TimeInMS': 'uint16',
  'sector3TimeInMS': 'uint16',
  'lapValidBitFlags': 'uint8',
}

TYRE_STINT_HISTORY_DATA: Final = {
  'endLap': 'uint8',
  'tyreActualCompound': 'uint8',
  'tyreVisualCompound': 'uint8',
}

PACKET: Final = {
  'carIdx': 'uint8',
  'numLaps': 'uint8',
  'numTyreStints': 'uint8',
  'bestLapTimeLapNum': 'uint8',
  'bestSector1LapNum': 'uint8',
  'bestSector2LapNum': 'uint8',
  'bestSector3LapNum': 'uint8',
  'lapHistoryData': 100 * [LAP_HISTORY_DATA],
  'tyreStintHistoryData': 8 * [TYRE_STINT_HISTORY_DATA]
}
