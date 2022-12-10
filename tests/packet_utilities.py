from struct import pack
from typing import get_origin, Type
from constants.constants import GRID_SIZE, PacketId
from custom_types.generic import T


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
    for i in range(4):
        data += pack(f'<{format}', i)
    return data


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


def create_generic_event_data(event_code: str) -> bytes:
    packet = create_packet_header_data(PacketId.EVENT)
    packet += create_event_code_data(event_code)
    return packet


def create_fastest_lap_data() -> bytes:
    packet = create_generic_event_data('FTLP')
    packet += pack('<B', 1)
    packet += pack('<f', 1.5)
    return packet
