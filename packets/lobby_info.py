from typing import Final

DATA: Final = {
  'aiControlled': 'uint8',
  'teamId': 'uint8',
  'nationality': 'uint8',
  'name': 48 * ['char'],
  'carNumber': 'uint8',
  'readyStatus': 'uint8',
}

PACKET: Final = {
  'numPlayers': 'uint8',
  'lobbyPlayers': 22 * [DATA],
}
