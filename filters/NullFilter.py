from filters.Filter import Filter
from packets.packets import Packet


class NullFilter(Filter):
    """Defines a Filter that accepts packets but performs no action."""

    def filter(self, packet: Packet):
        pass
