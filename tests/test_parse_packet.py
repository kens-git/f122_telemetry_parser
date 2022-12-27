from typing import Any, cast, Tuple
from unittest import TestCase
from constants.constants import (
    EventStringCode, GRID_SIZE, MAX_MARSHAL_ZONES, MAX_WEATHER_SAMPLES,
    PacketId)
from packets.packets import (
    CarDamagePacket, CarSetupsPacket, CarStatusPacket, CarTelemetryPacket,
    EventPacket, FinalClassificationPacket, LapDataPacket, LobbyInfoPacket,
    MotionPacket, Packet, ParticipantsPacket, SessionHistoryPacket,
    SessionPacket)
import tests.packet_utilities as pu
import utilities.data as du
from utilities.parse import parse_packet


def assert_packet_header(case: TestCase, packet: Packet, packet_id: PacketId):
    case.assertEqual(packet.packetFormat, 1)
    case.assertEqual(packet.gameMajorVersion, 2)
    case.assertEqual(packet.gameMinorVersion, 3)
    case.assertEqual(packet.packetVersion, 4)
    case.assertEqual(packet.packetId, packet_id.value)
    case.assertEqual(packet.sessionUID, 5)
    case.assertEqual(packet.sessionTime, 6.5)
    case.assertEqual(packet.frameIdentifier, 7)
    case.assertEqual(packet.playerCarIndex, 8)
    case.assertEqual(packet.secondaryPlayerCarIndex, 9)


def assert_car_corner_data(case: TestCase, data: Tuple[Any, ...]):
    case.assertEqual(data[0], 0)
    case.assertEqual(data[1], 1)
    case.assertEqual(data[2], 2)
    case.assertEqual(data[3], 3)


def assert_tire_stint_data(case: TestCase, data: Tuple[Any, ...]):
    case.assertEqual(data[0], 0)
    case.assertEqual(data[1], 1)
    case.assertEqual(data[2], 2)
    case.assertEqual(data[3], 3)
    case.assertEqual(data[4], 4)
    case.assertEqual(data[5], 5)
    case.assertEqual(data[6], 6)
    case.assertEqual(data[7], 7)


class TestParsePacket(TestCase):
    def test_motion(self):
        packet = cast(MotionPacket,
                      parse_packet(pu.create_motion_data()))
        assert_packet_header(self, packet, PacketId.MOTION)
        self.assertEqual(len(packet.carMotionData), GRID_SIZE)
        for data in packet.carMotionData:
            self.assertEqual(data.worldPositionX, 1)
            self.assertEqual(data.worldPositionY, 2)
            self.assertEqual(data.worldPositionZ, 3)
            self.assertEqual(data.worldVelocityX, 4)
            self.assertEqual(data.worldVelocityY, 5)
            self.assertEqual(data.worldVelocityZ, 6)
            self.assertEqual(data.worldForwardDirX, 7)
            self.assertEqual(data.worldForwardDirY, 8)
            self.assertEqual(data.worldForwardDirZ, 9)
            self.assertEqual(data.worldRightDirX, 10)
            self.assertEqual(data.worldRightDirY, 11)
            self.assertEqual(data.worldRightDirZ, 12)
            self.assertEqual(data.gForceLateral, 13)
            self.assertEqual(data.gForceLongitudinal, 14)
            self.assertEqual(data.gForceVertical, 15)
            self.assertEqual(data.yaw, 16)
            self.assertEqual(data.pitch, 17)
            self.assertEqual(data.roll, 18)
        assert_car_corner_data(self, packet.suspensionPosition)
        assert_car_corner_data(self, packet.suspensionVelocity)
        assert_car_corner_data(self, packet.suspensionAcceleration)
        assert_car_corner_data(self, packet.wheelSpeed)
        assert_car_corner_data(self, packet.wheelSlip)
        self.assertEqual(packet.localVelocityX, 19)
        self.assertEqual(packet.localVelocityY, 20)
        self.assertEqual(packet.localVelocityZ, 21)
        self.assertEqual(packet.angularVelocityX, 22)
        self.assertEqual(packet.angularVelocityY, 23)
        self.assertEqual(packet.angularVelocityZ, 24)
        self.assertEqual(packet.angularAccelerationX, 25)
        self.assertEqual(packet.angularAccelerationY, 26)
        self.assertEqual(packet.angularAccelerationZ, 27)
        self.assertEqual(packet.frontWheelsAngle, 28)

    def test_session(self):
        packet = cast(SessionPacket,
                      parse_packet(pu.create_session_data()))
        assert_packet_header(self, packet, PacketId.SESSION)
        self.assertEqual(packet.weather, 1)
        self.assertEqual(packet.trackTemperature, 2)
        self.assertEqual(packet.airTemperature, 3)
        self.assertEqual(packet.totalLaps, 4)
        self.assertEqual(packet.trackLength, 5)
        self.assertEqual(packet.sessionType, 6)
        self.assertEqual(packet.trackId, 7)
        self.assertEqual(packet.formula, 8)
        self.assertEqual(packet.sessionTimeLeft, 9)
        self.assertEqual(packet.sessionDuration, 10)
        self.assertEqual(packet.pitSpeedLimit, 11)
        self.assertEqual(packet.gamePaused, 12)
        self.assertEqual(packet.isSpectating, 13)
        self.assertEqual(packet.spectatorCarIndex, 14)
        self.assertEqual(packet.sliProNativeSupport, 15)
        self.assertEqual(packet.numMarshalZones, 16)
        self.assertEqual(len(packet.marshalZones), MAX_MARSHAL_ZONES)
        for zone in packet.marshalZones:
            self.assertEqual(zone.zoneStart, 1.5)
            self.assertEqual(zone.zoneFlag, 2)
        self.assertEqual(packet.safetyCarStatus, 17)
        self.assertEqual(packet.networkGame, 18)
        self.assertEqual(packet.numWeatherForecastSamples, 19)
        self.assertEqual(len(packet.weatherForecastSamples),
                         MAX_WEATHER_SAMPLES)
        for sample in packet.weatherForecastSamples:
            self.assertEqual(sample.sessionType, 1)
            self.assertEqual(sample.timeOffset, 2)
            self.assertEqual(sample.weather, 3)
            self.assertEqual(sample.trackTemperature, 4)
            self.assertEqual(sample.trackTemperatureChange, 5)
            self.assertEqual(sample.airTemperature, 6)
            self.assertEqual(sample.airTemperatureChange, 7)
            self.assertEqual(sample.rainPercentage, 8)
        self.assertEqual(packet.forecastAccuracy, 20)
        self.assertEqual(packet.aiDifficulty, 21)
        self.assertEqual(packet.seasonLinkIdentifier, 22)
        self.assertEqual(packet.weekendLinkIdentifier, 23)
        self.assertEqual(packet.sessionLinkIdentifier, 24)
        self.assertEqual(packet.pitStopWindowIdealLap, 25)
        self.assertEqual(packet.pitStopWindowLatestLap, 26)
        self.assertEqual(packet.pitStopRejoinPosition, 27)
        self.assertEqual(packet.steeringAssist, 28)
        self.assertEqual(packet.brakingAssist, 29)
        self.assertEqual(packet.gearboxAssist, 30)
        self.assertEqual(packet.pitAssist, 31)
        self.assertEqual(packet.pitReleaseAssist, 32)
        self.assertEqual(packet.ERSAssist, 33)
        self.assertEqual(packet.DRSAssist, 34)
        self.assertEqual(packet.dynamicRacingLine, 35)
        self.assertEqual(packet.dynamicRacingLineType, 36)
        self.assertEqual(packet.gameMode, 37)
        self.assertEqual(packet.ruleSet, 38)
        self.assertEqual(packet.timeOfDay, 39)
        self.assertEqual(packet.sessionLength, 40)

    def test_lap_data(self):
        packet = cast(LapDataPacket,
                      parse_packet(pu.create_lap_data()))
        assert_packet_header(self, packet, PacketId.LAP_DATA)
        self.assertEqual(len(packet.lapData), GRID_SIZE)
        for lap in packet.lapData:
            self.assertEqual(lap.lastLapTimeInMS, 1)
            self.assertEqual(lap.currentLapTimeInMS, 2)
            self.assertEqual(lap.sector1TimeInMS, 3)
            self.assertEqual(lap.sector2TimeInMS, 4)
            self.assertEqual(lap.lapDistance, 5)
            self.assertEqual(lap.totalDistance, 6)
            self.assertEqual(lap.safetyCarDelta, 7)
            self.assertEqual(lap.carPosition, 8)
            self.assertEqual(lap.currentLapNum, 9)
            self.assertEqual(lap.pitStatus, 10)
            self.assertEqual(lap.numPitStops, 11)
            self.assertEqual(lap.sector, 12)
            self.assertEqual(lap.currentLapInvalid, 13)
            self.assertEqual(lap.penalties, 14)
            self.assertEqual(lap.warnings, 15)
            self.assertEqual(lap.numUnservedDriveThroughPens, 16)
            self.assertEqual(lap.numUnservedStopGoPens, 17)
            self.assertEqual(lap.gridPosition, 18)
            self.assertEqual(lap.driverStatus, 19)
            self.assertEqual(lap.resultStatus, 20)
            self.assertEqual(lap.pitLaneTimerActive, 21)
            self.assertEqual(lap.pitLaneTimeInLaneInMS, 22)
            self.assertEqual(lap.pitStopTimerInMS, 23)
            self.assertEqual(lap.pitStopShouldServePen, 24)
        self.assertEqual(packet.timeTrialPBCarIdx, 1)
        self.assertEqual(packet.timeTrialRivalCarIdx, 2)

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
        packet = cast(EventPacket,
                      parse_packet(pu.create_fastest_lap_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.FASTEST_LAP.value)
        self.assertEqual(packet.eventDetails.FastestLap.vehicleIdx, 1)
        self.assertEqual(packet.eventDetails.FastestLap.lapTime, 1.5)

    def test_event_retirement(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_retirement_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.RETIREMENT.value)
        self.assertEqual(packet.eventDetails.Retirement.vehicleIdx, 1)

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
        packet = cast(EventPacket,
                      parse_packet(pu.create_team_mate_in_pits_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.TEAM_MATE_IN_PITS.value)
        self.assertEqual(packet.eventDetails.TeamMateInPits.vehicleIdx, 1)

    def test_event_chequered_flag(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('CHQF')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.CHEQUERED_FLAG.value)

    def test_event_race_winner(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_race_winner_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.RACE_WINNER.value)
        self.assertEqual(packet.eventDetails.RaceWinner.vehicleIdx, 1)

    def test_event_penalty_issued(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_penalty_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.PENALTY.value)
        self.assertEqual(packet.eventDetails.Penalty.penaltyType, 1)
        self.assertEqual(packet.eventDetails.Penalty.infringementType, 2)
        self.assertEqual(packet.eventDetails.Penalty.vehicleIdx, 3)
        self.assertEqual(packet.eventDetails.Penalty.otherVehicleIdx, 4)
        self.assertEqual(packet.eventDetails.Penalty.time, 5)
        self.assertEqual(packet.eventDetails.Penalty.lapNum, 6)
        self.assertEqual(packet.eventDetails.Penalty.placesGained, 7)

    def test_event_speed_trap_triggered(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_speed_trap_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.SPEED_TRAP.value)
        self.assertEqual(packet.eventDetails.SpeedTrap.vehicleIdx, 1)
        self.assertEqual(packet.eventDetails.SpeedTrap.speed, 2.5)
        self.assertEqual(
            packet.eventDetails.SpeedTrap.isOverallFastestInSession, 3)
        self.assertEqual(
            packet.eventDetails.SpeedTrap.isDriverFastestInSession, 4)
        self.assertEqual(
            packet.eventDetails.SpeedTrap.fastestVehicleIdxInSession, 5)
        self.assertEqual(
            packet.eventDetails.SpeedTrap.fastestSpeedInSession, 6.5)

    def test_event_start_lights(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_start_lights_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.START_LIGHTS.value)
        self.assertEqual(packet.eventDetails.StartLights.numLights, 1)

    def test_event_lights_out(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_generic_event_data('LGOT')))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.LIGHTS_OUT.value)

    def test_event_drive_through_served(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_drive_through_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.DRIVE_THROUGH_SERVED.value)
        self.assertEqual(
            packet.eventDetails.DriveThroughPenaltyServed.vehicleIdx, 1)

    def test_event_stop_go_served(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_stop_go_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.STOP_GO_SERVED.value)
        self.assertEqual(packet.eventDetails.StartLights.numLights, 1)

    def test_event_flashback(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_stop_go_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.STOP_GO_SERVED.value)
        self.assertEqual(packet.eventDetails.StopGoPenaltyServed.vehicleIdx, 1)

    def test_event_button_status(self):
        packet = cast(EventPacket,
                      parse_packet(pu.create_button_data()))
        assert_packet_header(self, packet, PacketId.EVENT)
        self.assertEqual(du.to_string(packet.eventStringCode),
                         EventStringCode.BUTTON.value)
        self.assertEqual(packet.eventDetails.Buttons.buttonStatus, 1)

    def test_participants(self):
        packet = cast(ParticipantsPacket,
                      parse_packet(pu.create_participants_data()))
        assert_packet_header(self, packet, PacketId.PARTICIPANTS)
        self.assertEqual(packet.numActiveCars, 1)
        for data in packet.participants:
            self.assertEqual(data.aiControlled, 1)
            self.assertEqual(data.driverId, 2)
            self.assertEqual(data.networkId, 3)
            self.assertEqual(data.teamId, 4)
            self.assertEqual(data.myTeam, 5)
            self.assertEqual(data.raceNumber, 6)
            self.assertEqual(data.nationality, 7)
            self.assertEqual(data.name, bytes('Pérez', 'utf-8'))
            self.assertEqual(data.yourTelemetry, 8)

    def test_car_setups(self):
        packet = cast(CarSetupsPacket,
                      parse_packet(pu.create_car_setups_data()))
        assert_packet_header(self, packet, PacketId.CAR_SETUPS)
        for setup in packet.carSetups:
            self.assertEqual(setup.frontWing, 1)
            self.assertEqual(setup.rearWing, 2)
            self.assertEqual(setup.onThrottle, 3)
            self.assertEqual(setup.offThrottle, 4)
            self.assertEqual(setup.frontCamber, 5.5)
            self.assertEqual(setup.rearCamber, 6.5)
            self.assertEqual(setup.frontToe, 7.5)
            self.assertEqual(setup.rearToe, 8.5)
            self.assertEqual(setup.frontSuspension, 9)
            self.assertEqual(setup.rearSuspension, 10)
            self.assertEqual(setup.frontAntiRollBar, 11)
            self.assertEqual(setup.rearAntiRollBar, 12)
            self.assertEqual(setup.frontSuspensionHeight, 13)
            self.assertEqual(setup.rearSuspensionHeight, 14)
            self.assertEqual(setup.brakePressure, 15)
            self.assertEqual(setup.brakeBias, 16)
            self.assertEqual(setup.rearLeftTyrePressure, 17.5)
            self.assertEqual(setup.rearRightTyrePressure, 18.5)
            self.assertEqual(setup.frontLeftTyrePressure, 19.5)
            self.assertEqual(setup.frontRightTyrePressure, 20.5)
            self.assertEqual(setup.ballast, 21)
            self.assertEqual(setup.fuelLoad, 22.5)

    def test_car_telemetry(self):
        packet = cast(CarTelemetryPacket,
                      parse_packet(pu.create_car_telemetry_data()))
        assert_packet_header(self, packet, PacketId.CAR_TELEMETRY)
        for data in packet.carTelemetryData:
            self.assertEqual(data.speed, 1)
            self.assertEqual(data.throttle, 2.5)
            self.assertEqual(data.steer, 3.5)
            self.assertEqual(data.brake, 4.5)
            self.assertEqual(data.clutch, 5)
            self.assertEqual(data.gear, 6)
            self.assertEqual(data.engineRPM, 7)
            self.assertEqual(data.drs, 8)
            self.assertEqual(data.revLightsPercent, 9)
            self.assertEqual(data.revLightsBitValue, 10)
            assert_car_corner_data(self, data.brakesTemperature)
            assert_car_corner_data(self, data.tiresSurfaceTemperature)
            assert_car_corner_data(self, data.tiresInnerTemperature)
            self.assertEqual(data.engineTemperature, 11)
            assert_car_corner_data(self, data.tiresPressure)
            assert_car_corner_data(self, data.surfaceType)
        self.assertEqual(packet.mfdPanelIndex, 1)
        self.assertEqual(packet.mfdPanelIndexSecondaryPlayer, 2)
        self.assertEqual(packet.suggestedGear, 3)

    def test_car_status(self):
        packet = cast(CarStatusPacket,
                      parse_packet(pu.create_car_status_data()))
        assert_packet_header(self, packet, PacketId.CAR_STATUS)
        for status in packet.carStatusData:
            self.assertEqual(status.tractionControl, 1)
            self.assertEqual(status.antiLockBrakes, 2)
            self.assertEqual(status.fuelMix, 3)
            self.assertEqual(status.frontBrakeBias, 4)
            self.assertEqual(status.pitLimiterStatus, 5)
            self.assertEqual(status.fuelInTank, 6.5)
            self.assertEqual(status.fuelCapacity, 7.5)
            self.assertEqual(status.fuelRemainingLaps, 8.5)
            self.assertEqual(status.maxRPM, 9)
            self.assertEqual(status.idleRPM, 10)
            self.assertEqual(status.maxGears, 11)
            self.assertEqual(status.drsAllowed, 12)
            self.assertEqual(status.drsActivationDistance, 13)
            self.assertEqual(status.actualTypeCompound, 14)
            self.assertEqual(status.visualTyreCompound, 15)
            self.assertEqual(status.tyresAgeLaps, 16)
            self.assertEqual(status.vehicleFiaFlags, 17)
            self.assertEqual(status.ersStoreEnergy, 18.5)
            self.assertEqual(status.ersDeployMode, 19)
            self.assertEqual(status.ersHarvestedThisLapMGUK, 20.5)
            self.assertEqual(status.ersHarvestedThisLapMGUH, 21.5)
            self.assertEqual(status.ersDeployedThisLap, 22.5)
            self.assertEqual(status.networkPaused, 23)

    def test_final_classification(self):
        packet = cast(FinalClassificationPacket,
                      parse_packet(pu.create_final_classification_data()))
        assert_packet_header(self, packet, PacketId.FINAL_CLASSIFICATION)
        self.assertEqual(packet.numCars, 1)
        for data in packet.classificationData:
            self.assertEqual(data.position, 1)
            self.assertEqual(data.numLaps, 2)
            self.assertEqual(data.gridPosition, 3)
            self.assertEqual(data.points, 4)
            self.assertEqual(data.numPitStops, 5)
            self.assertEqual(data.resultStatus, 6)
            self.assertEqual(data.bestLapTimeInMS, 7)
            self.assertEqual(data.totalRaceTime, 8)
            self.assertEqual(data.penaltiesTime, 9)
            self.assertEqual(data.numPenalties, 10)
            self.assertEqual(data.numTyreStints, 11)
            assert_tire_stint_data(self, data.tyreStintsActual)
            assert_tire_stint_data(self, data.tyreStintsVisual)
            assert_tire_stint_data(self, data.tyreStintEndLaps)

    def test_lobby_info(self):
        packet = cast(LobbyInfoPacket,
                      parse_packet(pu.create_lobby_info_data()))
        assert_packet_header(self, packet, PacketId.LOBBY_INFO)
        self.assertEqual(packet.numPlayers, 1)
        for player in packet.lobbyPlayers:
            self.assertEqual(player.aiControlled, 1)
            self.assertEqual(player.teamId, 2)
            self.assertEqual(player.nationality, 3)
            self.assertEqual(player.name, bytes('Driver', 'utf-8'))
            self.assertEqual(player.carNumber, 4)
            self.assertEqual(player.readyStatus, 5)

    def test_car_damage(self):
        packet = cast(CarDamagePacket,
                      parse_packet(pu.create_car_damage_data()))
        assert_packet_header(self, packet, PacketId.CAR_DAMAGE)
        for damage in packet.carDamageData:
            assert_car_corner_data(self, damage.tyresWear)
            assert_car_corner_data(self, damage.tyresDamage)
            assert_car_corner_data(self, damage.brakesDamage)
            self.assertEqual(damage.frontLeftWingDamage, 4)
            self.assertEqual(damage.frontRightWingDamage, 5)
            self.assertEqual(damage.rearWingDamage, 6)
            self.assertEqual(damage.floorDamage, 7)
            self.assertEqual(damage.diffuserDamage, 8)
            self.assertEqual(damage.sidepodDamage, 9)
            self.assertEqual(damage.drsFault, 10)
            self.assertEqual(damage.ersFault, 11)
            self.assertEqual(damage.gearBoxDamage, 12)
            self.assertEqual(damage.engineDamage, 13)
            self.assertEqual(damage.engineMGUHWear, 14)
            self.assertEqual(damage.engineESWear, 15)
            self.assertEqual(damage.engineCEWear, 16)
            self.assertEqual(damage.engineICEWear, 17)
            self.assertEqual(damage.engineMGUKWear, 18)
            self.assertEqual(damage.engineTCWear, 19)
            self.assertEqual(damage.engineBlown, 20)
            self.assertEqual(damage.engineSeized, 21)

    def test_session_history(self):
        packet = cast(SessionHistoryPacket,
                      parse_packet(pu.create_session_history_data()))
        assert_packet_header(self, packet, PacketId.SESSION_HISTORY)
        self.assertEqual(packet.carIdx, 1)
        self.assertEqual(packet.numLaps, 2)
        self.assertEqual(packet.numTyreStints, 3)
        self.assertEqual(packet.bestLapTimeLapNum, 4)
        self.assertEqual(packet.bestSector1LapNum, 5)
        self.assertEqual(packet.bestSector2LapNum, 6)
        self.assertEqual(packet.bestSector3LapNum, 7)
        for history in packet.lapHistoryData:
            self.assertEqual(history.lapTimeInMS, 1)
            self.assertEqual(history.sector1TimeInMS, 2)
            self.assertEqual(history.sector2TimeInMS, 3)
            self.assertEqual(history.sector3TimeInMS, 4)
            self.assertEqual(history.lapValidBitFlags, 5)
        for stint in packet.tyreStintHistoryData:
            self.assertEqual(stint.endLap, 1)
            self.assertEqual(stint.tyreActualCompound, 2)
            self.assertEqual(stint.tyreVisualCompound, 3)
