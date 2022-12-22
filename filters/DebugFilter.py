import logging
from filters.Filter import Filter
from packets.packets import Packet


class DebugFilter(Filter):
    """Implements a Filter for basic debugging of filtering.

    Generally, best to use as a sanity check to ensure the program is
    receiving data from the game and the filter is receiving Packets
    from the parser.
    """

    def filter(self, packet: Packet):
        """Logs the packet id to the console."""

        logging.info(packet.packetId)
        super().filter(packet)
