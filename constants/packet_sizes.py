from typing import Final

# TODO: rename file

from constants.game_constants import FIELD_SIZE

PACKET_HEADER_LENGTH: Final = 24
CAR_TELEMETRY_DATA_LENGTH: Final = 60
CAR_TELEMETRY_FIELD_DATA_LENGTH: Final = FIELD_SIZE * CAR_TELEMETRY_DATA_LENGTH
# doesn't include packet header size
CAR_TELEMETRY_DATA_PACKET_LENGTH: Final = 3 + CAR_TELEMETRY_FIELD_DATA_LENGTH
