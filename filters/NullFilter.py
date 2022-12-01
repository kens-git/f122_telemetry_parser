import filters.Filter as fil
import packets.packets as pk


class NullFilter(fil.Filter):

    def filter(self, packet: pk.Packet):
        pass
