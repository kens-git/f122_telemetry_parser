from typing import Final

PACKET: Final = {
  'packetFormat': 'uint16',
  'gameMajorVersion': 'uint8',
  'gameMinorVersion': 'uint8',
  'packetVersion': 'uint8',
  'packetId': 'uint8',
  'sessionUID': 'uint64',
  'sessionTime': 'float',
  'frameIdentifier': 'uint32',
  'playerCarIndex': 'uint8',
  'secondaryPlayerCarIndex': 'uint8',
}
