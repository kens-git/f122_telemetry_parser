from typing import cast, Tuple
from unittest import TestCase
from constants.constants import EventStringCode, PacketId
from packets.packets import (
    EventPacket, MotionPacket, Packet)
import tests.packet_utilities as pu
import utilities.data as du
from utilities.parse import parse_packet


def assert_packet_header(case: TestCase, packet: Packet, packet_id: PacketId):
    case.assertEqual(packet.packetFormat.value, 1)
    case.assertEqual(packet.gameMajorVersion.value, 2)
    case.assertEqual(packet.gameMinorVersion.value, 3)
    case.assertEqual(packet.packetVersion.value, 4)
    case.assertEqual(packet.packetId.value, packet_id.value)
    case.assertEqual(packet.sessionUID.value, 5)
    case.assertEqual(packet.sessionTime.value, 6.5)
    case.assertEqual(packet.frameIdentifier.value, 7)
    case.assertEqual(packet.playerCarIndex.value, 8)
    case.assertEqual(packet.secondaryPlayerCarIndex.value, 9)


def assert_car_corner_data(case: TestCase, data: Tuple[BasicType, ...]):
    case.assertEqual(data[0].value, 0)
    case.assertEqual(data[1].value, 1)
    case.assertEqual(data[2].value, 2)
    case.assertEqual(data[3].value, 3)


class TestParsePacket(TestCase):
    def test_motion(self):
        packet = cast(MotionPacket,
                      parse_packet(pu.create_motion_data()))
        assert_packet_header(self, packet, PacketId.MOTION)
        for data in packet.carMotionData:
            self.assertEqual(data.worldPositionX.value, 1)
            self.assertEqual(data.worldPositionY.value, 2)
            self.assertEqual(data.worldPositionZ.value, 3)
            self.assertEqual(data.worldVelocityX.value, 4)
            self.assertEqual(data.worldVelocityY.value, 5)
            self.assertEqual(data.worldVelocityZ.value, 6)
            self.assertEqual(data.worldForwardDirX.value, 7)
            self.assertEqual(data.worldForwardDirY.value, 8)
            self.assertEqual(data.worldForwardDirZ.value, 9)
            self.assertEqual(data.worldRightDirX.value, 10)
            self.assertEqual(data.worldRightDirY.value, 11)
            self.assertEqual(data.worldRightDirZ.value, 12)
            self.assertEqual(data.gForceLateral.value, 13)
            self.assertEqual(data.gForceLongitudinal.value, 14)
            self.assertEqual(data.gForceVertical.value, 15)
            self.assertEqual(data.yaw.value, 16)
            self.assertEqual(data.pitch.value, 17)
            self.assertEqual(data.roll.value, 18)
        assert_car_corner_data(self, packet.suspensionPosition)
        assert_car_corner_data(self, packet.suspensionVelocity)
        assert_car_corner_data(self, packet.suspensionAcceleration)
        assert_car_corner_data(self, packet.wheelSpeed)
        assert_car_corner_data(self, packet.wheelSlip)
        self.assertEqual(packet.localVelocityX.value, 19)
        self.assertEqual(packet.localVelocityY.value, 20)
        self.assertEqual(packet.localVelocityZ.value, 21)
        self.assertEqual(packet.angularVelocityX.value, 22)
        self.assertEqual(packet.angularVelocityY.value, 23)
        self.assertEqual(packet.angularVelocityZ.value, 24)
        self.assertEqual(packet.angularAccelerationX.value, 25)
        self.assertEqual(packet.angularAccelerationY.value, 26)
        self.assertEqual(packet.angularAccelerationZ.value, 27)
        self.assertEqual(packet.frontWheelsAngle.value, 28)

    def test_session(self):
        pass

    def test_lap_data(self):
        pass

    def test_event_session_started(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('SSTA')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.SESSION_START.value)

    def test_event_session_ended(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('SEND')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.SESSION_END.value)

    def test_event_fastest_lap(self):
        packet = cast(FastestLapPacket,
                      parse_packet(pu.create_fastest_lap_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.FASTEST_LAP.value)
        self.assertEqual(packet.vehicleIdx.value, 1)
        self.assertEqual(packet.lapTime.value, 1.5)

    def test_event_retirement(self):
        pass

    def test_event_drs_enabled(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('DRSE')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.DRS_ENABLED.value)

    def test_event_drs_disabled(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('DRSD')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.DRS_DISABLED.value)

    def test_event_team_mate_in_pits(self):
        pass

    def test_event_chequered_flag(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('CHQF')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.CHEQUERED_FLAG.value)

    def test_event_race_winner(self):
        pass

    def test_event_penalty_issued(self):
        pass

    def test_event_speed_trap_triggered(self):
        pass

    def test_event_start_lights(self):
        pass

    def test_event_lights_out(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('LGOT')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.LIGHTS_OUT.value)

    def test_event_drive_through_served(self):
        pass

    def test_event_stop_go_served(self):
        pass

    def test_event_flashback(self):
        pass

    def test_event_button_status(self):
        pass

    def test_participants(self):
        pass

    def test_car_setups(self):
        pass

    def test_car_telemetry(self):
        pass

    def test_car_status(self):
        pass

    def test_final_classification(self):
        pass

    def test_lobby_info(self):
        pass

    def test_car_damage(self):
        pass

    def test_session_history(self):
        pass
