from abc import ABC, abstractmethod
import packets.packets as pk


class Filter(ABC):
    """Defines a class for managing filtering of Packets."""

    def cleanup(self):
        """Alerts the Filter that it will no longer receive packets."""

        pass

    @abstractmethod
    def filter(self, packet: pk.Packet):
        """Filters a packet.

        Args:
            packet: The packet to filter.
        """

        pass
