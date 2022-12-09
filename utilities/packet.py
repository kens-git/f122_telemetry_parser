from constants.constants import PACKET_HEADER_ID_INDEX
from custom_types.basic import UInt8
import utilities.data as du


def get_packet_id(data: bytes) -> int:
    return int(du.unpack(data, PACKET_HEADER_ID_INDEX, UInt8).value)
