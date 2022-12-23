from struct import pack
from constants.constants import (
    EventStringCode, EVENT_PACKET_LENGTH, GRID_SIZE, MAX_LAP_HISTORIES,
    MAX_MARSHAL_ZONES, MAX_TYRE_STINTS, MAX_WEATHER_SAMPLES, NAME_SIZE,
    PacketId, TIRE_COUNT)


def create_packet_header_data(id: PacketId) -> bytes:
    data: bytes = b''
    data += pack('<H', 1)  # packet format
    data += pack('<B', 2)  # game major version
    data += pack('<B', 3)  # game minor version
    data += pack('<B', 4)  # packet version
    data += pack('<B', id.value)  # packet id
    data += pack('<Q', 5)  # session UID
    data += pack('<f', 6.5)  # session time
    data += pack('<I', 7)  # frame identifier
    data += pack('<B', 8)  # player car index
    data += pack('<B', 9)  # secondary player car index
    return data


def create_event_code_data(code: str) -> bytes:
    byte_code = bytes()
    for c in code:
        byte_code += bytes(c, 'ascii')
    return byte_code


def create_car_corner_data(format: str) -> bytes:
    data = bytes()
    for i in range(TIRE_COUNT):
        data += pack(f'<{format}', i)
    return data


def create_tire_stint_data(format: str) -> bytes:
    data = bytes()
    for i in range(MAX_TYRE_STINTS):
        data += pack(f'<{format}', i)
    return data


def create_string_data(string: str, size: int) -> bytes:
    return pack(f'<{size}s', bytes(f'{string}\0'.ljust(size, ' '), 'utf-8'))


def create_motion_data() -> bytes:
    packet = create_packet_header_data(PacketId.MOTION)
    for _ in range(GRID_SIZE):
        packet += pack('<f', 1.0)
        packet += pack('<f', 2.0)
        packet += pack('<f', 3.0)
        packet += pack('<f', 4.0)
        packet += pack('<f', 5.0)
        packet += pack('<f', 6.0)
        packet += pack('<h', 7)
        packet += pack('<h', 8)
        packet += pack('<h', 9)
        packet += pack('<h', 10)
        packet += pack('<h', 11)
        packet += pack('<h', 12)
        packet += pack('<f', 13.0)
        packet += pack('<f', 14.0)
        packet += pack('<f', 15.0)
        packet += pack('<f', 16.0)
        packet += pack('<f', 17.0)
        packet += pack('<f', 18.0)
    packet += create_car_corner_data('f')
    packet += create_car_corner_data('f')
    packet += create_car_corner_data('f')
    packet += create_car_corner_data('f')
    packet += create_car_corner_data('f')
    packet += pack('<f', 19)
    packet += pack('<f', 20)
    packet += pack('<f', 21)
    packet += pack('<f', 22)
    packet += pack('<f', 23)
    packet += pack('<f', 24)
    packet += pack('<f', 25)
    packet += pack('<f', 26)
    packet += pack('<f', 27)
    packet += pack('<f', 28)
    return packet


def create_session_data() -> bytes:
    packet = create_packet_header_data(PacketId.SESSION)
    packet += pack('<B', 1)
    packet += pack('<b', 2)
    packet += pack('<b', 3)
    packet += pack('<B', 4)
    packet += pack('<H', 5)
    packet += pack('<B', 6)
    packet += pack('<b', 7)
    packet += pack('<B', 8)
    packet += pack('<H', 9)
    packet += pack('<H', 10)
    packet += pack('<B', 11)
    packet += pack('<B', 12)
    packet += pack('<B', 13)
    packet += pack('<B', 14)
    packet += pack('<B', 15)
    packet += pack('<B', 16)
    for _ in range(MAX_MARSHAL_ZONES):
        packet += pack('<f', 1.5)
        packet += pack('<b', 2)
    packet += pack('<B', 17)
    packet += pack('<B', 18)
    packet += pack('<B', 19)
    for _ in range(MAX_WEATHER_SAMPLES):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
        packet += pack('<b', 4)
        packet += pack('<b', 5)
        packet += pack('<b', 6)
        packet += pack('<b', 7)
        packet += pack('<B', 8)
    packet += pack('<B', 20)
    packet += pack('<B', 21)
    packet += pack('<I', 22)
    packet += pack('<I', 23)
    packet += pack('<I', 24)
    packet += pack('<B', 25)
    packet += pack('<B', 26)
    packet += pack('<B', 27)
    packet += pack('<B', 28)
    packet += pack('<B', 29)
    packet += pack('<B', 30)
    packet += pack('<B', 31)
    packet += pack('<B', 32)
    packet += pack('<B', 33)
    packet += pack('<B', 34)
    packet += pack('<B', 35)
    packet += pack('<B', 36)
    packet += pack('<B', 37)
    packet += pack('<B', 38)
    packet += pack('<I', 39)
    packet += pack('<B', 40)
    return packet


def create_lap_data() -> bytes:
    packet = create_packet_header_data(PacketId.LAP_DATA)
    for _ in range(GRID_SIZE):
        packet += pack('<I', 1)
        packet += pack('<I', 2)
        packet += pack('<H', 3)
        packet += pack('<H', 4)
        packet += pack('<f', 5)
        packet += pack('<f', 6)
        packet += pack('<f', 7)
        packet += pack('<B', 8)
        packet += pack('<B', 9)
        packet += pack('<B', 10)
        packet += pack('<B', 11)
        packet += pack('<B', 12)
        packet += pack('<B', 13)
        packet += pack('<B', 14)
        packet += pack('<B', 15)
        packet += pack('<B', 16)
        packet += pack('<B', 17)
        packet += pack('<B', 18)
        packet += pack('<B', 19)
        packet += pack('<B', 20)
        packet += pack('<B', 21)
        packet += pack('<H', 22)
        packet += pack('<H', 23)
        packet += pack('<B', 24)
    packet += pack('<B', 1)
    packet += pack('<B', 2)
    return packet


def pad_event_data(data: bytes) -> bytes:
    return data + (b'0' * (EVENT_PACKET_LENGTH - len(data)))


def create_generic_event_data(event_code: str) -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(event_code)
    packet += pad_event_data(packet)
    return packet


def create_fastest_lap_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.FASTEST_LAP.value)
    packet += pack('<B', 1)
    packet += pack('<f', 1.5)
    return pad_event_data(packet)


def create_retirement_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.RETIREMENT.value)
    packet += pack('<B', 1)
    return pad_event_data(packet)


def create_team_mate_in_pits_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.TEAM_MATE_IN_PITS.value)
    packet += pack('<B', 1)
    return pad_event_data(packet)


def create_race_winner_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.RACE_WINNER.value)
    packet += pack('<B', 1)
    return pad_event_data(packet)


def create_penalty_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.PENALTY.value)
    packet += pack('<B', 1)
    packet += pack('<B', 2)
    packet += pack('<B', 3)
    packet += pack('<B', 4)
    packet += pack('<B', 5)
    packet += pack('<B', 6)
    packet += pack('<B', 7)
    return pad_event_data(packet)


def create_speed_trap_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.SPEED_TRAP.value)
    packet += pack('<B', 1)
    packet += pack('<f', 2.5)
    packet += pack('<B', 3)
    packet += pack('<B', 4)
    packet += pack('<B', 5)
    packet += pack('<f', 6.5)
    return pad_event_data(packet)


def create_start_lights_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.START_LIGHTS.value)
    packet += pack('<B', 1)
    return pad_event_data(packet)


def create_drive_through_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.DRIVE_THROUGH_SERVED.value)
    packet += pack('<B', 1)
    return pad_event_data(packet)


def create_stop_go_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(
        EventStringCode.STOP_GO_SERVED.value)
    packet += pack('<B', 1)
    return pad_event_data(packet)


def create_button_data() -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(EventStringCode.BUTTON.value)
    packet += pack('<I', 1)
    return pad_event_data(packet)


def create_participants_data() -> bytes:
    packet = create_packet_header_data(PacketId.PARTICIPANTS)
    packet += pack('<B', 1)
    for _ in range(GRID_SIZE):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
        packet += pack('<B', 4)
        packet += pack('<B', 5)
        packet += pack('<B', 6)
        packet += pack('<B', 7)
        packet += create_string_data('Pérez', NAME_SIZE)
        packet += pack('<B', 8)
    return packet


def create_car_setups_data() -> bytes:
    packet = create_packet_header_data(PacketId.CAR_SETUPS)
    for _ in range(GRID_SIZE):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
        packet += pack('<B', 4)
        packet += pack('<f', 5.5)
        packet += pack('<f', 6.5)
        packet += pack('<f', 7.5)
        packet += pack('<f', 8.5)
        packet += pack('<B', 9)
        packet += pack('<B', 10)
        packet += pack('<B', 11)
        packet += pack('<B', 12)
        packet += pack('<B', 13)
        packet += pack('<B', 14)
        packet += pack('<B', 15)
        packet += pack('<B', 16)
        packet += pack('<f', 17.5)
        packet += pack('<f', 18.5)
        packet += pack('<f', 19.5)
        packet += pack('<f', 20.5)
        packet += pack('<B', 21)
        packet += pack('<f', 22.5)
    return packet


def create_car_telemetry_data() -> bytes:
    packet = create_packet_header_data(PacketId.CAR_TELEMETRY)
    for _ in range(GRID_SIZE):
        packet += pack('<H', 1)
        packet += pack('<f', 2.5)
        packet += pack('<f', 3.5)
        packet += pack('<f', 4.5)
        packet += pack('<B', 5)
        packet += pack('<b', 6)
        packet += pack('<H', 7)
        packet += pack('<B', 8)
        packet += pack('<B', 9)
        packet += pack('<H', 10)
        packet += create_car_corner_data('H')
        packet += create_car_corner_data('B')
        packet += create_car_corner_data('B')
        packet += pack('<H', 11)
        packet += create_car_corner_data('f')
        packet += create_car_corner_data('B')
    packet += pack('<B', 1)
    packet += pack('<B', 2)
    packet += pack('<b', 3)
    return packet


def create_car_status_data() -> bytes:
    packet = create_packet_header_data(PacketId.CAR_STATUS)
    for _ in range(GRID_SIZE):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
        packet += pack('<B', 4)
        packet += pack('<B', 5)
        packet += pack('<f', 6.5)
        packet += pack('<f', 7.5)
        packet += pack('<f', 8.5)
        packet += pack('<H', 9)
        packet += pack('<H', 10)
        packet += pack('<B', 11)
        packet += pack('<B', 12)
        packet += pack('<H', 13)
        packet += pack('<B', 14)
        packet += pack('<B', 15)
        packet += pack('<B', 16)
        packet += pack('<b', 17)
        packet += pack('<f', 18.5)
        packet += pack('<B', 19)
        packet += pack('<f', 20.5)
        packet += pack('<f', 21.5)
        packet += pack('<f', 22.5)
        packet += pack('<B', 23)
    return packet


def create_final_classification_data() -> bytes:
    packet = create_packet_header_data(PacketId.FINAL_CLASSIFICATION)
    packet += pack('<B', 1)
    for _ in range(GRID_SIZE):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
        packet += pack('<B', 4)
        packet += pack('<B', 5)
        packet += pack('<B', 6)
        packet += pack('<I', 7)
        packet += pack('<d', 8)
        packet += pack('<B', 9)
        packet += pack('<B', 10)
        packet += pack('<B', 11)
        packet += create_tire_stint_data('B')
        packet += create_tire_stint_data('B')
        packet += create_tire_stint_data('B')
    return packet


def create_lobby_info_data() -> bytes:
    packet = create_packet_header_data(PacketId.LOBBY_INFO)
    packet += pack('<B', 1)
    for _ in range(GRID_SIZE):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
        packet += create_string_data('Driver', NAME_SIZE)
        packet += pack('<B', 4)
        packet += pack('<B', 5)
    return packet


def create_car_damage_data() -> bytes:
    packet = create_packet_header_data(PacketId.CAR_DAMAGE)
    for _ in range(GRID_SIZE):
        packet += create_car_corner_data('f')
        packet += create_car_corner_data('B')
        packet += create_car_corner_data('B')
        packet += pack('<B', 4)
        packet += pack('<B', 5)
        packet += pack('<B', 6)
        packet += pack('<B', 7)
        packet += pack('<B', 8)
        packet += pack('<B', 9)
        packet += pack('<B', 10)
        packet += pack('<B', 11)
        packet += pack('<B', 12)
        packet += pack('<B', 13)
        packet += pack('<B', 14)
        packet += pack('<B', 15)
        packet += pack('<B', 16)
        packet += pack('<B', 17)
        packet += pack('<B', 18)
        packet += pack('<B', 19)
        packet += pack('<B', 20)
        packet += pack('<B', 21)
    return packet


def create_session_history_data() -> bytes:
    packet = create_packet_header_data(PacketId.SESSION_HISTORY)
    packet += pack('<B', 1)
    packet += pack('<B', 2)
    packet += pack('<B', 3)
    packet += pack('<B', 4)
    packet += pack('<B', 5)
    packet += pack('<B', 6)
    packet += pack('<B', 7)
    for _ in range(MAX_LAP_HISTORIES):
        packet += pack('I', 1)
        packet += pack('H', 2)
        packet += pack('H', 3)
        packet += pack('H', 4)
        packet += pack('B', 5)
    for _ in range(MAX_TYRE_STINTS):
        packet += pack('<B', 1)
        packet += pack('<B', 2)
        packet += pack('<B', 3)
    return packet
