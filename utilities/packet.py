import constants.constants as const
import custom_types.basic as bt
import utilities.data as util


def get_packet_id(data: bytes) -> int:
    return int(util.unpack(data, const.PACKET_HEADER_ID_INDEX, bt.UInt8).value)
