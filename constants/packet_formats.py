from typing import Final
from constants import packet_ids
from packets import (car_damage, car_setups, car_status, car_telemetry,
  event, final_classification, header, lap_data, lobby_info, motion,
  participants, session, session_history)

PACKET_FORMATS: Final = {
  packet_ids.MOTION: motion.PACKET,
  packet_ids.SESSION: session.PACKET,
  packet_ids.LAP_DATA: lap_data.PACKET,
  packet_ids.EVENT: event.PACKET,
  packet_ids.PARTICIPANTS: participants.PACKET,
  packet_ids.CAR_SETUPS: car_setups.PACKET,
  packet_ids.CAR_TELEMETRY: car_telemetry.PACKET,
  packet_ids.CAR_STATUS: car_status.PACKET,
  packet_ids.FINAL_CLASSIFICATION: final_classification.PACKET,
  packet_ids.LOBBY_INFO: lobby_info.PACKET,
  packet_ids.CAR_DAMAGE: car_damage.PACKET,
  packet_ids.SESSION_HISTORY: session_history.PACKET,
}
