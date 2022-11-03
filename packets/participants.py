from typing import Final

DATA: Final = {
  'aiControlled': 'uint8',
  'driverId': 'uint8',
  'networkId': 'uint8',
  'teamId': 'uint8',
  'myTeam': 'uint8',
  'raceNumber': 'uint8',
  'nationality': 'uint8',
  'name': 48 * ['char'],
  'yourTelemetry': 'uint8',
}

PACKET: Final = {
  'numActiveCars': 'uint8',
  'participants': 22 * [DATA],
}
