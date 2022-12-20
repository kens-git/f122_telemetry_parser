from packets.packets import Packet, PACKET_TYPE
from utilities.packet import get_packet_id


def parse_packet(data: bytes) -> Packet:
    """Parses a Packet from the given bytes.

    Args:
        data: The bytes to parse the packet from.

    Returns:
        An instance of a Packet subclass, determined by the packet's id.
    """

    return PACKET_TYPE[get_packet_id(data)].from_buffer_copy(data)
