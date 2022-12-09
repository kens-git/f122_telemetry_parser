import logging
from filters.Filter import Filter
from packets.packets import Packet


class DebugFilter(Filter):

    def filter(self, packet: Packet):
        logging.info(packet.packetId)
