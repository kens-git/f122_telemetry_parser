import packets.packets as pk
import parsers.UDPParser as udp


def c(a: pk.Packet):
    print(a.packetId)  # type: ignore


if __name__ == '__main__':
    parser = udp.UDPParser(c, 20777)
    parser.start()
