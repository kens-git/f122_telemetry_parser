from constants.constants import PACKET_HEADER_ID_INDEX
from custom_types.basic import UInt8
import utilities.data as du


def get_packet_id(packet_data: bytes) -> int:
    """Returns the id of a packet from the given packet data.

    Args:
        packet_data: The raw bytes of the packet.

    Returns:
        The packet id.
    """

    return int(du.unpack(packet_data, PACKET_HEADER_ID_INDEX, UInt8).value)
