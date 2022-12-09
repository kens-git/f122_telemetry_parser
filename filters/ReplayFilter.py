from dataclasses import dataclass
from enum import Enum
import json
import logging
from pathlib import Path
import time
from typing import Any, cast, Dict, List
from constants.constants import (
    GRID_COUNT, EventStringCode, PacketId, TRACK_NAMES, SESSION_TEXT)
from filters.Filter import Filter
from packets.packets import (
    CarDamagePacket, CarSetupsPacket, CarStatusPacket, CarTelemetryPacket,
    DriveThroughPenaltyServedPacket, EventPacket, FastestLapPacket,
    FlashbackPacket, LapDataPacket, MotionPacket, Packet, ParticipantsPacket,
    PenaltyPacket, RaceWinnerPacket, RetirementPacket, SessionPacket,
    SpeedTrapPacket, StartLightsPacket, StopGoPenaltyServedPacket)
import utilities.data as du


class DataStorePolicy(Enum):
    ALL = 0,
    FIRST = 1,
    ON_CHANGE = 2,


def set(data: List[Any], timestamp: float, value: Any,
        policy: DataStorePolicy):
    # Storing timestamps with ms precision cuts down the file size by ~50%.
    timestamp = float('%.3f' % (timestamp))
    if policy == DataStorePolicy.ALL:
        data.append((timestamp, value))
    elif policy == DataStorePolicy.FIRST:
        if not data:
            data.append((timestamp, value))
    elif policy == DataStorePolicy.ON_CHANGE:
        if not data:
            data.append((timestamp, value))
        else:
            previous = data[-1][1]
            if previous != value:
                data.append((timestamp, value))
    else:
        raise ValueError('No matching UpdatePolicy.')


@dataclass
class DataPoint():
    timestamp: float
    value: Any


@dataclass
class DataField:
    field: str
    policy: DataStorePolicy


class ReplayFilter(Filter):
    def __init__(self):
        self.version = 1
        self.session_start_time: float = 0
        self.session_end_time: float = 0
        self.file_start_write_time: float = 0
        self.file_end_write_time: float = 0
        self.data: Dict[str, Any] = {}
        self._reset()

    # TODO: filter final classification to ensure all driver data is available after a finish
    #       (since it's possible the session ends without all drivers finishing before the
    #        user advances to the next screen)
    def filter(self, packet: Packet):
        packet_id = packet.packetId.value
        if packet_id == PacketId.MOTION.value:
            packet = cast(MotionPacket, packet)
            self._filter_motion(packet)
        elif packet_id == PacketId.SESSION.value:
            packet = cast(SessionPacket, packet)
            self._filter_session(packet)
        elif packet_id == PacketId.LAP_DATA.value:
            packet = cast(LapDataPacket, packet)
            self._filter_lap_data(packet)
        elif packet_id == PacketId.EVENT.value:
            packet = cast(EventPacket, packet)
            self._filter_event(packet)
        elif packet_id == PacketId.PARTICIPANTS.value:
            packet = cast(ParticipantsPacket, packet)
            self._filter_participants(packet)
        elif packet_id == PacketId.CAR_SETUPS.value:
            packet = cast(CarSetupsPacket, packet)
            self._filter_car_setups(packet)
        elif packet_id == PacketId.CAR_TELEMETRY.value:
            packet = cast(CarTelemetryPacket, packet)
            self._filter_car_telemetry(packet)
        elif packet_id == PacketId.CAR_STATUS.value:
            packet = cast(CarStatusPacket, packet)
            self._filter_car_status(packet)
        elif packet_id == PacketId.CAR_DAMAGE.value:
            packet = cast(CarDamagePacket, packet)
            self._filter_car_damage(packet)

    def _filter_car_damage(self, packet: CarDamagePacket):
        timestamp = packet.sessionTime.value
        for index, data in enumerate(packet.carDamageData):
            damage_data = self.data['car_damage'][index]
            set(damage_data['tyresWear'], timestamp,
                tuple(x.value for x in data.tyresWear),
                DataStorePolicy.ON_CHANGE)
            set(damage_data['tyresDamage'], timestamp,
                tuple(x.value for x in data.tyresDamage),
                DataStorePolicy.ON_CHANGE)
            set(damage_data['brakesDamage'], timestamp,
                tuple(x.value for x in data.brakesDamage),
                DataStorePolicy.ON_CHANGE)
            set(damage_data['frontLeftWingDamage'], timestamp,
                data.frontLeftWingDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['frontRightWingDamage'], timestamp,
                data.frontRightWingDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['rearWingDamage'], timestamp,
                data.rearWingDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['floorDamage'], timestamp, data.floorDamage.value,
                DataStorePolicy.ON_CHANGE)
            set(damage_data['diffuserDamage'], timestamp,
                data.diffuserDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['sidepodDamage'], timestamp,
                data.sidepodDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['drsFault'], timestamp, data.drsFault.value,
                DataStorePolicy.ON_CHANGE)
            set(damage_data['ersFault'], timestamp, data.ersFault.value,
                DataStorePolicy.ON_CHANGE)
            set(damage_data['gearBoxDamage'], timestamp,
                data.gearBoxDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineDamage'], timestamp,
                data.engineDamage.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineMGUHWear'], timestamp,
                data.engineMGUHWear.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineESWear'], timestamp,
                data.engineESWear.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineCEWear'], timestamp,
                data.engineCEWear.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineICEWear'], timestamp,
                data.engineICEWear.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineMGUKWear'], timestamp,
                data.engineMGUKWear.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineTCWear'], timestamp,
                data.engineTCWear.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineBlown'], timestamp,
                data.engineBlown.value, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineSeized'], timestamp,
                data.engineSeized.value, DataStorePolicy.ON_CHANGE)

    def _filter_car_setups(self, packet: CarSetupsPacket):
        timestamp = packet.sessionTime.value
        for index, data in enumerate(packet.carSetups):
            setup_data = self.data['car_setups'][index]
            set(setup_data['frontWing'], timestamp, data.frontWing.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearWing'], timestamp, data.rearWing.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['onThrottle'], timestamp, data.onThrottle.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['offThrottle'], timestamp, data.offThrottle.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['frontCamber'], timestamp, data.frontCamber.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearCamber'], timestamp, data.rearCamber.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['frontToe'], timestamp, data.frontToe.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearToe'], timestamp, data.rearToe.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['frontSuspension'], timestamp,
                data.frontSuspension.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearSuspension'], timestamp,
                data.rearSuspension.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontAntiRollBar'], timestamp,
                data.frontAntiRollBar.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearAntiRollBar'], timestamp,
                data.rearAntiRollBar.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontSuspensionHeight'], timestamp,
                data.frontSuspensionHeight.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearSuspensionHeight'], timestamp,
                data.rearSuspensionHeight.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['brakePressure'], timestamp,
                data.brakePressure.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['brakeBias'], timestamp, data.brakeBias.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearLeftTyrePressure'], timestamp,
                data.rearLeftTyrePressure.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearRightTyrePressure'], timestamp,
                data.rearRightTyrePressure.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontLeftTyrePressure'], timestamp,
                data.frontLeftTyrePressure.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontRightTyrePressure'], timestamp,
                data.frontRightTyrePressure.value, DataStorePolicy.ON_CHANGE)
            set(setup_data['ballast'], timestamp, data.ballast.value,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['fuelLoad'], timestamp, data.fuelLoad.value,
                DataStorePolicy.ON_CHANGE)

    def _filter_car_status(self, packet: CarStatusPacket):
        timestamp = packet.sessionTime.value
        for index, data in enumerate(packet.carStatusData):
            status_data = self.data['car_status'][index]
            set(status_data['tractionControl'], timestamp,
                data.tractionControl.value, DataStorePolicy.ON_CHANGE)
            set(status_data['antiLockBrakes'], timestamp,
                data.antiLockBrakes.value, DataStorePolicy.ON_CHANGE)
            set(status_data['fuelMix'], timestamp, data.fuelMix.value,
                DataStorePolicy.ON_CHANGE)
            set(status_data['frontBrakeBias'], timestamp,
                data.frontBrakeBias.value, DataStorePolicy.ON_CHANGE)
            set(status_data['pitLimiterStatus'], timestamp,
                data.pitLimiterStatus.value, DataStorePolicy.ON_CHANGE)
            set(status_data['fuelInTank'], timestamp, data.fuelInTank.value,
                DataStorePolicy.ON_CHANGE)
            set(status_data['fuelCapacity'], timestamp,
                data.fuelCapacity.value, DataStorePolicy.ON_CHANGE)
            set(status_data['fuelRemainingLaps'], timestamp,
                data.fuelRemainingLaps.value, DataStorePolicy.ON_CHANGE)
            set(status_data['maxRPM'], timestamp, data.maxRPM.value,
                DataStorePolicy.ON_CHANGE)
            set(status_data['idleRPM'], timestamp, data.idleRPM.value,
                DataStorePolicy.ON_CHANGE)
            set(status_data['maxGears'], timestamp, data.maxGears.value,
                DataStorePolicy.ON_CHANGE)
            set(status_data['drsAllowed'], timestamp, data.drsAllowed.value,
                DataStorePolicy.ON_CHANGE)
            set(status_data['drsActivationDistance'], timestamp,
                data.drsActivationDistance.value, DataStorePolicy.ON_CHANGE)
            set(status_data['actualTypeCompound'], timestamp,
                data.actualTypeCompound.value, DataStorePolicy.ON_CHANGE)
            set(status_data['visualTyreCompound'], timestamp,
                data.visualTyreCompound.value, DataStorePolicy.ON_CHANGE)
            set(status_data['tyresAgeLaps'], timestamp,
                data.tyresAgeLaps.value, DataStorePolicy.ON_CHANGE)
            set(status_data['vehicleFiaFlags'], timestamp,
                data.vehicleFiaFlags.value, DataStorePolicy.ON_CHANGE)
            set(status_data['ersStoreEnergy'], timestamp,
                data.ersStoreEnergy.value, DataStorePolicy.ON_CHANGE)
            set(status_data['ersDeployMode'], timestamp,
                data.ersDeployMode.value, DataStorePolicy.ON_CHANGE)
            set(status_data['ersHarvestedThisLapMGUK'], timestamp,
                data.ersHarvestedThisLapMGUK.value, DataStorePolicy.ON_CHANGE)
            set(status_data['ersHarvestedThisLapMGUH'], timestamp,
                data.ersHarvestedThisLapMGUH.value, DataStorePolicy.ON_CHANGE)
            set(status_data['ersDeployedThisLap'], timestamp,
                data.ersDeployedThisLap.value, DataStorePolicy.ON_CHANGE)
            set(status_data['networkPaused'], timestamp,
                data.networkPaused.value, DataStorePolicy.ON_CHANGE)

    def _filter_car_telemetry(self, packet: CarTelemetryPacket):
        timestamp = packet.sessionTime.value
        for index, data in enumerate(packet.carTelemetryData):
            telem_data = self.data['car_telemetry'][index]
            set(telem_data['speed'], timestamp, data.speed.value,
                DataStorePolicy.ON_CHANGE)
            # Storing this telemetry and motion data (below) with 3 decimal
            # precision shrinks the data file by ~30%.
            set(telem_data['throttle'], timestamp,
                float('%.3f' % (data.throttle.value)),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['steer'], timestamp,
                float('%.3f' % (data.steer.value)),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['brake'], timestamp,
                float('%.3f' % (data.brake.value)),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['clutch'], timestamp, data.clutch.value,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['gear'], timestamp, data.gear.value,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['engineRPM'], timestamp, data.engineRPM.value,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['drs'], timestamp, data.drs.value,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['revLightsPercent'], timestamp,
                data.revLightsPercent.value, DataStorePolicy.ON_CHANGE)
            set(telem_data['revLightsBitValue'], timestamp,
                data.revLightsBitValue.value, DataStorePolicy.ON_CHANGE)
            set(telem_data['brakesTemperature'], timestamp,
                tuple(x.value for x in data.brakesTemperature),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['tiresSurfaceTemperature'], timestamp,
                tuple(x.value for x in data.tiresSurfaceTemperature),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['tiresInnerTemperature'], timestamp,
                tuple(x.value for x in data.tiresInnerTemperature),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['engineTemperature'], timestamp,
                data.engineTemperature.value,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['tiresPressure'], timestamp,
                tuple(x.value for x in data.tiresPressure),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['surfaceType'], timestamp,
                tuple(x.value for x in data.surfaceType),
                DataStorePolicy.ON_CHANGE)

    def _filter_event(self, packet: EventPacket):
        event_code = du.to_string(packet.eventStringCode)
        if event_code == EventStringCode.BUTTON.value:
            return
        if event_code == EventStringCode.SESSION_START.value:
            # TODO: this needs to reset if multiple session starts are detected:
            #       It's possible to open the pause menu while waiting on the grid
            #       and after closing the menu a session start event is sent.
            #       If the user then quits the race no end event is sent, causing
            #       the filter to wait for an end event that isn't coming.
            logging.info('Session start detected.')
            self.session_start_time = time.time()
            self.data['event'][event_code] = (
                packet.sessionTime.value, event_code)
        elif event_code == EventStringCode.SESSION_END.value:
            logging.info('Session end detected.')
            self.session_end_time = time.time()
            self.data['event'][event_code] = (
                packet.sessionTime.value, event_code)
            self._save_data()
        elif event_code == EventStringCode.FASTEST_LAP.value:
            packet = cast(FastestLapPacket, packet)
            self.data['event'][event_code].append((
                packet.sessionTime.value, event_code,
                packet.vehicleIdx.value, packet.lapTime.value))
        elif event_code == EventStringCode.RETIREMENT.value:
            packet = cast(RetirementPacket, packet)
            self.data['event'][event_code].append((
                packet.sessionTime.value, event_code,
                packet.vehicleIdx.value))
        elif event_code == EventStringCode.DRS_ENABLED.value:
            self.data['event'][event_code].append((
                packet.sessionTime.value, event_code))
        elif event_code == EventStringCode.DRS_DISABLED.value:
            self.data['event'][event_code].append((
                packet.sessionTime.value, event_code))
        elif event_code == EventStringCode.CHEQUERED_FLAG.value:
            self.data['event'][event_code] = (
                packet.sessionTime.value, event_code)
        elif event_code == EventStringCode.RACE_WINNER.value:
            packet = cast(RaceWinnerPacket, packet)
            self.data['event'][event_code] = (
                packet.sessionTime.value, event_code,
                packet.vehicleIdx.value)
        elif event_code == EventStringCode.PENALTY.value:
            packet = cast(PenaltyPacket, packet)
            self.data['event'][event_code].append(
                (packet.sessionTime.value, event_code,
                    packet.penaltyType.value,
                    packet.infringementType.value,
                    packet.vehicleIdx.value,
                    packet.otherVehicleIdx.value,
                    packet.time.value,
                    packet.placesGained.value))
        elif event_code == EventStringCode.SPEED_TRAP.value:
            packet = cast(SpeedTrapPacket, packet)
            if packet.isOverallFastestInSession.value == 1:
                self.data['event'][event_code].append((
                    packet.sessionTime.value,
                    event_code,
                    packet.vehicleIdx.value,
                    packet.speed.value))
        elif event_code == EventStringCode.START_LIGHTS.value:
            packet = cast(StartLightsPacket, packet)
            self.data['event'][event_code].append(
                (packet.sessionTime.value, event_code,
                    packet.numLights.value))
        elif event_code == EventStringCode.LIGHTS_OUT.value:
            self.data['event'][event_code] = (
                packet.sessionTime.value, event_code)
        elif event_code == EventStringCode.DRIVE_THROUGH_SERVED.value:
            packet = cast(
                DriveThroughPenaltyServedPacket, packet)
            self.data['event'][event_code].append((
                packet.sessionTime.value, event_code,
                packet.vehicleIdx.value))
        elif event_code == EventStringCode.STOP_GO_SERVED.value:
            packet = cast(StopGoPenaltyServedPacket, packet)
            self.data['event'][event_code].append((
                packet.sessionTime.value, event_code,
                packet.vehicleIdx.value))
        elif event_code == EventStringCode.FLASHBACK.value:
            packet = cast(FlashbackPacket, packet)
            self.data['event'][event_code].append(
                (packet.sessionTime.value, event_code,
                    packet.flashbackSessionTime.value))

    def _filter_lap_data(self, packet: LapDataPacket):
        timestamp = packet.sessionTime.value
        for index, data in enumerate(packet.lapData):
            lap_data = self.data['lap_data'][index]
            set(lap_data['lastLapTimeInMS'], timestamp,
                data.lastLapTimeInMS.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['currentLapTimeInMS'], timestamp,
                data.currentLapTimeInMS.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['sector1TimeInMS'], timestamp,
                data.sector1TimeInMS.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['sector2TimeInMS'], timestamp,
                data.sector2TimeInMS.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['carPosition'], timestamp, data.carPosition.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['currentLapNum'], timestamp, data.currentLapNum.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['pitStatus'], timestamp, data.pitStatus.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['numPitStops'], timestamp, data.numPitStops.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['sector'], timestamp, data.sector.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['currentLapInvalid'], timestamp,
                data.currentLapInvalid.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['penalties'], timestamp, data.penalties.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['warnings'], timestamp, data.warnings.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['numUnservedDriveThroughPens'], timestamp,
                data.numUnservedDriveThroughPens.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['numUnservedStopGoPens'], timestamp,
                data.numUnservedStopGoPens.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['gridPosition'], timestamp, data.gridPosition.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['driverStatus'], timestamp, data.driverStatus.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['resultStatus'], timestamp, data.resultStatus.value,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['pitLaneTimerActive'], timestamp,
                data.pitLaneTimerActive.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['pitLaneTimeInLaneInMS'], timestamp,
                data.pitLaneTimeInLaneInMS.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['pitStopTimerInMS'], timestamp,
                data.pitStopTimerInMS.value, DataStorePolicy.ON_CHANGE)
            set(lap_data['pitStopShouldServePen'], timestamp,
                data.pitStopShouldServePen.value, DataStorePolicy.ON_CHANGE)

    def _filter_motion(self, packet: MotionPacket):
        for index, data in enumerate(packet.carMotionData):
            data_list = self.data['motion'][index]
            set(data_list['worldPositionX'], packet.sessionTime.value,
                float('%.3f' % (data.worldPositionX.value)),
                DataStorePolicy.ON_CHANGE)
            set(data_list['worldPositionY'], packet.sessionTime.value,
                float('%.3f' % (data.worldPositionY.value)),
                DataStorePolicy.ON_CHANGE)
            set(data_list['yaw'], packet.sessionTime.value,
                float('%.3f' % (data.yaw.value)),
                DataStorePolicy.ON_CHANGE)

    def _filter_participants(self, packet: ParticipantsPacket):
        p_data = self.data['participants']
        if p_data['numActiveCars'] is None:
            p_data['numActiveCars'] = packet.numActiveCars.value
            for index, data in enumerate(packet.participants):
                participant = p_data['participants'][index]
                participant['aiControlled'] = data.aiControlled.value
                participant['driverId'] = data.driverId.value
                participant['networkId'] = data.networkId.value
                participant['teamId'] = data.teamId.value
                participant['myTeam'] = data.myTeam.value
                participant['raceNumber'] = data.raceNumber.value
                participant['nationality'] = data.nationality.value
                participant['name'] = du.to_string(data.name)
                participant['yourTelemetry'] = data.yourTelemetry.value

    def _filter_session(self, packet: SessionPacket):
        session_data = self.data['session']
        set(session_data['sessionUID'], packet.sessionTime.value,
            packet.sessionUID.value, DataStorePolicy.FIRST)
        set(session_data['weather'], packet.sessionTime.value,
            packet.weather.value, DataStorePolicy.ON_CHANGE)
        set(session_data['trackTemperature'], packet.sessionTime.value,
            packet.trackTemperature.value, DataStorePolicy.ON_CHANGE)
        set(session_data['airTemperature'], packet.sessionTime.value,
            packet.airTemperature.value, DataStorePolicy.ON_CHANGE)
        set(session_data['totalLaps'], packet.sessionTime.value,
            packet.totalLaps.value, DataStorePolicy.FIRST)
        set(session_data['trackLength'], packet.sessionTime.value,
            packet.trackLength.value, DataStorePolicy.FIRST)
        set(session_data['sessionType'], packet.sessionTime.value,
            packet.sessionType.value, DataStorePolicy.FIRST)
        set(session_data['trackId'], packet.sessionTime.value,
            packet.trackId.value, DataStorePolicy.FIRST)
        set(session_data['formula'], packet.sessionTime.value,
            packet.formula.value, DataStorePolicy.FIRST)
        set(session_data['pitSpeedLimit'], packet.sessionTime.value,
            packet.pitSpeedLimit.value, DataStorePolicy.FIRST)
        set(session_data['gamePaused'], packet.sessionTime.value,
            packet.gamePaused.value, DataStorePolicy.ON_CHANGE)
        set(session_data['numMarshalZones'], packet.sessionTime.value,
            packet.numMarshalZones.value, DataStorePolicy.FIRST)
        session_data['marshalZones'].append((
            packet.sessionTime.value,
            [x.zoneFlag.value for x in packet.marshalZones]))
        set(session_data['safetyCarStatus'], packet.sessionTime.value,
            packet.safetyCarStatus.value, DataStorePolicy.ON_CHANGE)
        set(session_data['networkGame'], packet.sessionTime.value,
            packet.networkGame.value, DataStorePolicy.FIRST)
        set(session_data['forecastAccuracy'], packet.sessionTime.value,
            packet.forecastAccuracy.value, DataStorePolicy.FIRST)
        set(session_data['aiDifficulty'], packet.sessionTime.value,
            packet.aiDifficulty.value, DataStorePolicy.FIRST)
        set(session_data['seasonLinkIdentifier'], packet.sessionTime.value,
            packet.seasonLinkIdentifier.value, DataStorePolicy.FIRST)
        set(session_data['weekendLinkIdentifier'], packet.sessionTime.value,
            packet.weekendLinkIdentifier.value, DataStorePolicy.FIRST)
        set(session_data['sessionLinkIdentifier'], packet.sessionTime.value,
            packet.sessionLinkIdentifier.value, DataStorePolicy.FIRST)
        set(session_data['steeringAssist'], packet.sessionTime.value,
            packet.steeringAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['brakingAssist'], packet.sessionTime.value,
            packet.brakingAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['gearboxAssist'], packet.sessionTime.value,
            packet.gearboxAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['pitAssist'], packet.sessionTime.value,
            packet.pitAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['pitReleaseAssist'], packet.sessionTime.value,
            packet.pitReleaseAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['ERSAssist'], packet.sessionTime.value,
            packet.ERSAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['DRSAssist'], packet.sessionTime.value,
            packet.DRSAssist.value, DataStorePolicy.ON_CHANGE)
        set(session_data['dynamicRacingLine'], packet.sessionTime.value,
            packet.dynamicRacingLine.value, DataStorePolicy.ON_CHANGE)
        set(session_data['dynamicRacingLineType'], packet.sessionTime.value,
            packet.dynamicRacingLineType.value, DataStorePolicy.ON_CHANGE)
        set(session_data['gameMode'], packet.sessionTime.value,
            packet.gameMode.value, DataStorePolicy.FIRST)
        set(session_data['ruleSet'], packet.sessionTime.value,
            packet.ruleSet.value, DataStorePolicy.FIRST)
        set(session_data['timeOfDay'], packet.sessionTime.value,
            packet.timeOfDay.value, DataStorePolicy.ON_CHANGE)
        set(session_data['sessionLength'], packet.sessionTime.value,
            packet.sessionLength.value, DataStorePolicy.FIRST)

    def _reset(self):
        self.session_start_time = 0
        self.session_end_time = 0
        self.file_start_write_time = 0
        self.file_end_write_time = 0
        self.data = {
            'motion':
                [{
                    'worldPositionX': [],
                    'worldPositionY': [],
                    'yaw': []
                } for _ in range(GRID_COUNT)],
            'session': {
                'sessionUID': [],
                'weather': [],
                'trackTemperature': [],
                'airTemperature': [],
                'totalLaps': [],
                'trackLength': [],
                'sessionType': [],
                'trackId': [],
                'formula': [],
                'pitSpeedLimit': [],
                'gamePaused': [],
                'numMarshalZones': [],
                'marshalZones': [],
                'safetyCarStatus': [],
                'networkGame': [],
                'forecastAccuracy': [],
                'aiDifficulty': [],
                'seasonLinkIdentifier': [],
                'weekendLinkIdentifier': [],
                'sessionLinkIdentifier': [],
                'steeringAssist': [],
                'brakingAssist': [],
                'gearboxAssist': [],
                'pitAssist': [],
                'pitReleaseAssist': [],
                'ERSAssist': [],
                'DRSAssist': [],
                'dynamicRacingLine': [],
                'dynamicRacingLineType': [],
                'gameMode': [],
                'ruleSet': [],
                'timeOfDay': [],
                'sessionLength': []},
            'lap_data':
                [{
                    'lastLapTimeInMS': [],
                    'currentLapTimeInMS': [],
                    'sector1TimeInMS': [],
                    'sector2TimeInMS': [],
                    'carPosition': [],
                    'currentLapNum': [],
                    'pitStatus': [],
                    'numPitStops': [],
                    'sector': [],
                    'currentLapInvalid': [],
                    'penalties': [],
                    'warnings': [],
                    'numUnservedDriveThroughPens': [],
                    'numUnservedStopGoPens': [],
                    'gridPosition': [],
                    'driverStatus': [],
                    'resultStatus': [],
                    'pitLaneTimerActive': [],
                    'pitLaneTimeInLaneInMS': [],
                    'pitStopTimerInMS': [],
                    'pitStopShouldServePen': [],
                } for _ in range(GRID_COUNT)],
            'event': {
                EventStringCode.SESSION_START.value: None,
                EventStringCode.SESSION_END.value: None,
                EventStringCode.FASTEST_LAP.value: [],
                EventStringCode.RETIREMENT.value: [],
                EventStringCode.DRS_ENABLED.value: [],
                EventStringCode.DRS_DISABLED.value: [],
                EventStringCode.CHEQUERED_FLAG.value: None,
                EventStringCode.RACE_WINNER.value: None,
                EventStringCode.PENALTY.value: [],
                EventStringCode.SPEED_TRAP.value: [],
                EventStringCode.START_LIGHTS.value: [],
                EventStringCode.LIGHTS_OUT.value: None,
                EventStringCode.DRIVE_THROUGH_SERVED.value: [],
                EventStringCode.STOP_GO_SERVED.value: [],
                EventStringCode.FLASHBACK.value: []},
            'participants': {
                    'numActiveCars': None,
                    'participants':
                        [{
                            'aiControlled': None,
                            'driverId': None,
                            'networkId': None,
                            'teamId': None,
                            'myTeam': None,
                            'raceNumber': None,
                            'nationality': None,
                            'name': None,
                            'yourTelemetry': None,
                        } for _ in range(GRID_COUNT)]
                },
            'car_setups':
                [{
                    'frontWing': [],
                    'rearWing': [],
                    'onThrottle': [],
                    'offThrottle': [],
                    'frontCamber': [],
                    'rearCamber': [],
                    'frontToe': [],
                    'rearToe': [],
                    'frontSuspension': [],
                    'rearSuspension': [],
                    'frontAntiRollBar': [],
                    'rearAntiRollBar': [],
                    'frontSuspensionHeight': [],
                    'rearSuspensionHeight': [],
                    'brakePressure': [],
                    'brakeBias': [],
                    'rearLeftTyrePressure': [],
                    'rearRightTyrePressure': [],
                    'frontLeftTyrePressure': [],
                    'frontRightTyrePressure': [],
                    'ballast': [],
                    'fuelLoad': [],
                } for _ in range(GRID_COUNT)],
            'car_telemetry':
                [{
                    'speed': [],
                    'throttle': [],
                    'steer': [],
                    'brake': [],
                    'clutch': [],
                    'gear': [],
                    'engineRPM': [],
                    'drs': [],
                    'revLightsPercent': [],
                    'revLightsBitValue': [],
                    'brakesTemperature': [],
                    'tiresSurfaceTemperature': [],
                    'tiresInnerTemperature': [],
                    'engineTemperature': [],
                    'tiresPressure': [],
                    'surfaceType': [],
                } for _ in range(GRID_COUNT)],
            'car_status':
                [{
                    'tractionControl': [],
                    'antiLockBrakes': [],
                    'fuelMix': [],
                    'frontBrakeBias': [],
                    'pitLimiterStatus': [],
                    'fuelInTank': [],
                    'fuelCapacity': [],
                    'fuelRemainingLaps': [],
                    'maxRPM': [],
                    'idleRPM': [],
                    'maxGears': [],
                    'drsAllowed': [],
                    'drsActivationDistance': [],
                    'actualTypeCompound': [],
                    'visualTyreCompound': [],
                    'tyresAgeLaps': [],
                    'vehicleFiaFlags': [],
                    'ersStoreEnergy': [],
                    'ersDeployMode': [],
                    'ersHarvestedThisLapMGUK': [],
                    'ersHarvestedThisLapMGUH': [],
                    'ersDeployedThisLap': [],
                    'networkPaused': [],
                } for _ in range(GRID_COUNT)],
            'car_damage':
                [{
                    'tyresWear': [],
                    'tyresDamage': [],
                    'brakesDamage': [],
                    'frontLeftWingDamage': [],
                    'frontRightWingDamage': [],
                    'rearWingDamage': [],
                    'floorDamage': [],
                    'diffuserDamage': [],
                    'sidepodDamage': [],
                    'drsFault': [],
                    'ersFault': [],
                    'gearBoxDamage': [],
                    'engineDamage': [],
                    'engineMGUHWear': [],
                    'engineESWear': [],
                    'engineCEWear': [],
                    'engineICEWear': [],
                    'engineMGUKWear': [],
                    'engineTCWear': [],
                    'engineBlown': [],
                    'engineSeized': [],
                } for _ in range(GRID_COUNT)],
        }

    def _save_data(self):
        if self.data['participants']['numActiveCars'] is None:
            logging.info("No participants data: can't write file.")
            return
        logging.info('Session filtering complete.')
        logging.debug(f'Session filter time: \
{self.session_end_time - self.session_start_time}')
        logging.info('Writing data to file...')
        self.file_start_write_time = time.time()
        track_name = TRACK_NAMES[
            self.data['session']['trackId'][0][1]].replace(' ', '_')[0:12]
        session_type = SESSION_TEXT[
            self.data['session']['sessionType'][0][1]][0:12].replace(
                ' ', '_').replace('-', '_')
        session_uid = str(self.data['session']['sessionUID'][0][1])[-8:]
        filename = f'{track_name}_{session_type}_{session_uid}.json'
        filepath = Path('saved_data')
        filepath.mkdir(exist_ok=True)
        filepath = filepath / filename
        with filepath.open(mode='w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False,
                      separators=(',', ':'))
        logging.info(f'Finished writing file: {filename}\n')
        self.file_end_write_time = time.time()
        logging.debug(f'File write time: \
{self.file_end_write_time - self.file_start_write_time}')
        logging.debug(f'Total time: \
{self.file_end_write_time - self.session_start_time}')
        self._reset()
