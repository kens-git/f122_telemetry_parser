from filters.Filter import Filter
from packets.packets import Packet


class NullFilter(Filter):

    def filter(self, packet: Packet):
        pass
