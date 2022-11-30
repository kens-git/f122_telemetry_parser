import abc
import packets.packets as pk


class Filter(abc.ABC):
    def cleanup(self):
        pass

    @abc.abstractmethod
    def filter(self, packet: pk.Packet):
        pass
