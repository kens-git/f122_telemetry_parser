from typing import Final

DATA: Final = {
  'tractionControl': 'uint8',
  'antiLockBrakes': 'uint8',
  'fuelMix': 'uint8',
  'frontBrakeBias': 'uint8',
  'pitLimiterStatus': 'uint8',
  'fuelInTank': 'float',
  'fuelCapacity': 'float',
  'fuelRemainingLaps': 'float',
  'maxRPM': 'uint16',
  'idleRPM': 'uint16',
  'maxGears': 'uint8',
  'drsAllowed': 'uint8',
  'drsActivationDistance': 'uint16',
  'actualTypeCompound': 'uint8',
  'visualTyreCompound': 'uint8',
  'tyresAgeLaps': 'uint8',
  'vehicleFiaFlags': 'int8',
  'ersStoreEnergy': 'float',
  'ersDeployMode': 'uint8',
  'ersHarvestedThisLapMGUK': 'float',
  'ersHarvestedThisLapMGUH': 'float',
  'ersDeployedThisLap': 'float',
  'networkPaused': 'uint8',
}

PACKET: Final = {
  'carStatusData': 22 * [DATA]
}
