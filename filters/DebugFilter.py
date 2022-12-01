import filters.Filter as fil
import packets.packets as pk


class DebugFilter(fil.Filter):

    def filter(self, packet: pk.Packet):
        print(packet.packetId)
