from struct import unpack
from constants.constants import PACKET_HEADER_ID_INDEX


def get_packet_id(packet_data: bytes) -> int:
    """Returns the id of a packet from the given packet data.

    Args:
        packet_data: The raw bytes of the packet.

    Returns:
        The packet id.
    """

    return unpack(
        '<B',
        packet_data[PACKET_HEADER_ID_INDEX:PACKET_HEADER_ID_INDEX + 1])[0]
