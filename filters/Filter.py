from abc import ABC, abstractmethod
import packets.packets as pk


class Filter(ABC):
    def cleanup(self):
        pass

    @abstractmethod
    def filter(self, packet: pk.Packet):
        pass
