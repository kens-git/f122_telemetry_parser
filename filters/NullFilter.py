import filters.Filter as fil
import packets.packets as pk


class NullFilter(fil.Filter):
    def cleanup(self):
        pass

    def filter(self, packet: pk.Packet):
        pass
