import custom_types.basic as bt
import packets.packets as pk
import utilities.data as util


def get_packet_id(data: bytearray) -> int:
    return int(util.unpack(data, pk.PACKET_HEADER_ID_INDEX, bt.UInt8).value)
