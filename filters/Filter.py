from abc import ABC
from typing import cast
from constants.constants import PacketId
from packets.packets import (
    CarDamagePacket, CarSetupsPacket, CarStatusPacket, CarTelemetryPacket,
    EventPacket, FinalClassificationPacket, LapDataPacket, LobbyInfoPacket,
    MotionPacket, Packet, ParticipantsPacket, SessionHistoryPacket,
    SessionPacket)


class Filter(ABC):
    """Defines a class for managing the filtering of Packets."""

    def cleanup(self):
        """Alerts the Filter that it will no longer receive packets."""

        pass

    def filter(self, packet: Packet):
        """Filters a packet by delegating to the other filter methods.

        This method acts a single source for all packets that should be handled
        by the filter. Subclasses that override this method should call this
        method at the end if they want the other filter methods to be
        automatically called with their respective packet type.

        Args:
            packet: The packet to filter.
        """

        packet_id = packet.packetId
        if packet_id == PacketId.MOTION.value:
            packet = cast(MotionPacket, packet)
            self.filter_motion(packet)
        elif packet_id == PacketId.SESSION.value:
            packet = cast(SessionPacket, packet)
            self.filter_session(packet)
        elif packet_id == PacketId.LAP_DATA.value:
            packet = cast(LapDataPacket, packet)
            self.filter_lap_data(packet)
        elif packet_id == PacketId.EVENT.value:
            packet = cast(EventPacket, packet)
            self.filter_event(packet)
        elif packet_id == PacketId.PARTICIPANTS.value:
            packet = cast(ParticipantsPacket, packet)
            self.filter_participants(packet)
        elif packet_id == PacketId.CAR_SETUPS.value:
            packet = cast(CarSetupsPacket, packet)
            self.filter_car_setups(packet)
        elif packet_id == PacketId.CAR_TELEMETRY.value:
            packet = cast(CarTelemetryPacket, packet)
            self.filter_car_telemetry(packet)
        elif packet_id == PacketId.CAR_STATUS.value:
            packet = cast(CarStatusPacket, packet)
            self.filter_car_status(packet)
        elif packet_id == PacketId.FINAL_CLASSIFICATION.value:
            packet = cast(FinalClassificationPacket, packet)
            self.filter_final_classification(packet)
        elif packet_id == PacketId.LOBBY_INFO.value:
            packet = cast(LobbyInfoPacket, packet)
            self.filter_lobby_info(packet)
        elif packet_id == PacketId.CAR_DAMAGE.value:
            packet = cast(CarDamagePacket, packet)
            self.filter_car_damage(packet)
        elif packet_id == PacketId.SESSION_HISTORY.value:
            packet = cast(SessionHistoryPacket, packet)
            self.filter_session_history(packet)
        else:
            raise ValueError(
                f'Invalid packet id in Filter.filter: {packet_id}')

    def filter_motion(self, packet: MotionPacket):
        pass

    def filter_lap_data(self, packet: LapDataPacket):
        pass

    def filter_session(self, packet: SessionPacket):
        pass

    def filter_event(self, packet: EventPacket):
        pass

    def filter_participants(self, packet: ParticipantsPacket):
        pass

    def filter_car_setups(self, packet: CarSetupsPacket):
        pass

    def filter_car_telemetry(self, packet: CarTelemetryPacket):
        pass

    def filter_car_status(self, packet: CarStatusPacket):
        pass

    def filter_final_classification(
            self, packet: FinalClassificationPacket):
        pass

    def filter_lobby_info(self, packet: LobbyInfoPacket):
        pass

    def filter_car_damage(self, packet: CarDamagePacket):
        pass

    def filter_session_history(self, packet: SessionHistoryPacket):
        pass
