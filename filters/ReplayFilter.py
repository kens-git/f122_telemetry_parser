from ctypes import Structure
from enum import Enum
import json
import logging
from pathlib import Path
import time
from typing import Any, cast, Dict, List
from constants.constants import (
    GRID_SIZE, EventStringCode, PacketId, TRACK_NAMES, SESSION_TEXT)
from filters.Filter import Filter
from packets.packets import (
    CarDamagePacket, CarSetupsPacket, CarStatusPacket, CarTelemetryPacket,
    EventPacket, FinalClassificationPacket, LapDataPacket, MotionPacket,
    Packet, ParticipantsPacket, SessionPacket)
from packets.packet_data import (
    DriveThroughPenaltyServed, FastestLap, FinalClassificationData, Flashback,
    Penalty, RaceWinner, Retirement, SpeedTrap, StartLights,
    StopGoPenaltyServed)
import utilities.data as du


class DataStorePolicy(Enum):
    """Defines the policy used to determine when to store data."""

    ALL = 0,
    """Store all data."""

    FIRST = 1,
    """Store the first instance of the data but ignore everything else."""

    ON_CHANGE = 2,
    """Store instances of data that are different from the data
    immediately before it.
    """


def set(data: List[Any], timestamp: float, value: Any,
        policy: DataStorePolicy):
    """Adds timestamped data to a list according to the given policy.

    Args:
        data: The list of data to add to.
        timestamp: The timestamp of the data.
        value: The value to consider for addition to the data.
        policy: The data storing policy.
    """

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


class ReplayFilter(Filter):
    """Defines a Filter that stores session data for an external program.

    This class is due for a major refactor and the implementation details of
    it should not be relied on.
    """

    def __init__(self):
        self.format_version = 1
        self.is_session_started = False
        self.session_start_time: float = 0
        self.session_end_time: float = 0
        self.file_start_write_time: float = 0
        self.file_end_write_time: float = 0
        self.data: Dict[str, Any] = {}
        self._reset()

    def filter(self, packet: Packet):
        packet_id = packet.packetId
        if not self.is_session_started:
            if packet_id != PacketId.EVENT.value:
                return
            p = cast(EventPacket, packet)
            event_code = du.to_string(p.eventStringCode)
            if event_code != EventStringCode.SESSION_START.value:
                return
        super().filter(packet)

    def filter_car_damage(self, packet: CarDamagePacket):
        timestamp = packet.sessionTime
        for index, data in enumerate(packet.carDamageData):
            damage_data = self.data['car_damage'][index]
            set(damage_data['tyresWear'], timestamp,
                tuple(x for x in data.tyresWear),
                DataStorePolicy.ON_CHANGE)
            set(damage_data['tyresDamage'], timestamp,
                tuple(x for x in data.tyresDamage),
                DataStorePolicy.ON_CHANGE)
            set(damage_data['brakesDamage'], timestamp,
                tuple(x for x in data.brakesDamage),
                DataStorePolicy.ON_CHANGE)
            set(damage_data['frontLeftWingDamage'], timestamp,
                data.frontLeftWingDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['frontRightWingDamage'], timestamp,
                data.frontRightWingDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['rearWingDamage'], timestamp,
                data.rearWingDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['floorDamage'], timestamp, data.floorDamage,
                DataStorePolicy.ON_CHANGE)
            set(damage_data['diffuserDamage'], timestamp,
                data.diffuserDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['sidepodDamage'], timestamp,
                data.sidepodDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['drsFault'], timestamp, data.drsFault,
                DataStorePolicy.ON_CHANGE)
            set(damage_data['ersFault'], timestamp, data.ersFault,
                DataStorePolicy.ON_CHANGE)
            set(damage_data['gearBoxDamage'], timestamp,
                data.gearBoxDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineDamage'], timestamp,
                data.engineDamage, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineMGUHWear'], timestamp,
                data.engineMGUHWear, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineESWear'], timestamp,
                data.engineESWear, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineCEWear'], timestamp,
                data.engineCEWear, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineICEWear'], timestamp,
                data.engineICEWear, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineMGUKWear'], timestamp,
                data.engineMGUKWear, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineTCWear'], timestamp,
                data.engineTCWear, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineBlown'], timestamp,
                data.engineBlown, DataStorePolicy.ON_CHANGE)
            set(damage_data['engineSeized'], timestamp,
                data.engineSeized, DataStorePolicy.ON_CHANGE)

    def filter_car_setups(self, packet: CarSetupsPacket):
        timestamp = packet.sessionTime
        for index, data in enumerate(packet.carSetups):
            setup_data = self.data['car_setups'][index]
            set(setup_data['frontWing'], timestamp, data.frontWing,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearWing'], timestamp, data.rearWing,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['onThrottle'], timestamp, data.onThrottle,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['offThrottle'], timestamp, data.offThrottle,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['frontCamber'], timestamp, data.frontCamber,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearCamber'], timestamp, data.rearCamber,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['frontToe'], timestamp, data.frontToe,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearToe'], timestamp, data.rearToe,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['frontSuspension'], timestamp,
                data.frontSuspension, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearSuspension'], timestamp,
                data.rearSuspension, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontAntiRollBar'], timestamp,
                data.frontAntiRollBar, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearAntiRollBar'], timestamp,
                data.rearAntiRollBar, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontSuspensionHeight'], timestamp,
                data.frontSuspensionHeight, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearSuspensionHeight'], timestamp,
                data.rearSuspensionHeight, DataStorePolicy.ON_CHANGE)
            set(setup_data['brakePressure'], timestamp,
                data.brakePressure, DataStorePolicy.ON_CHANGE)
            set(setup_data['brakeBias'], timestamp, data.brakeBias,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['rearLeftTyrePressure'], timestamp,
                data.rearLeftTyrePressure, DataStorePolicy.ON_CHANGE)
            set(setup_data['rearRightTyrePressure'], timestamp,
                data.rearRightTyrePressure, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontLeftTyrePressure'], timestamp,
                data.frontLeftTyrePressure, DataStorePolicy.ON_CHANGE)
            set(setup_data['frontRightTyrePressure'], timestamp,
                data.frontRightTyrePressure, DataStorePolicy.ON_CHANGE)
            set(setup_data['ballast'], timestamp, data.ballast,
                DataStorePolicy.ON_CHANGE)
            set(setup_data['fuelLoad'], timestamp, data.fuelLoad,
                DataStorePolicy.ON_CHANGE)

    def filter_car_status(self, packet: CarStatusPacket):
        timestamp = packet.sessionTime
        for index, data in enumerate(packet.carStatusData):
            status_data = self.data['car_status'][index]
            set(status_data['tractionControl'], timestamp,
                data.tractionControl, DataStorePolicy.ON_CHANGE)
            set(status_data['antiLockBrakes'], timestamp,
                data.antiLockBrakes, DataStorePolicy.ON_CHANGE)
            set(status_data['fuelMix'], timestamp, data.fuelMix,
                DataStorePolicy.ON_CHANGE)
            set(status_data['frontBrakeBias'], timestamp,
                data.frontBrakeBias, DataStorePolicy.ON_CHANGE)
            set(status_data['pitLimiterStatus'], timestamp,
                data.pitLimiterStatus, DataStorePolicy.ON_CHANGE)
            set(status_data['fuelInTank'], timestamp, data.fuelInTank,
                DataStorePolicy.ON_CHANGE)
            set(status_data['fuelCapacity'], timestamp,
                data.fuelCapacity, DataStorePolicy.ON_CHANGE)
            set(status_data['fuelRemainingLaps'], timestamp,
                data.fuelRemainingLaps, DataStorePolicy.ON_CHANGE)
            set(status_data['maxRPM'], timestamp, data.maxRPM,
                DataStorePolicy.ON_CHANGE)
            set(status_data['idleRPM'], timestamp, data.idleRPM,
                DataStorePolicy.ON_CHANGE)
            set(status_data['maxGears'], timestamp, data.maxGears,
                DataStorePolicy.ON_CHANGE)
            set(status_data['drsAllowed'], timestamp, data.drsAllowed,
                DataStorePolicy.ON_CHANGE)
            set(status_data['drsActivationDistance'], timestamp,
                data.drsActivationDistance, DataStorePolicy.ON_CHANGE)
            set(status_data['actualTypeCompound'], timestamp,
                data.actualTypeCompound, DataStorePolicy.ON_CHANGE)
            set(status_data['visualTyreCompound'], timestamp,
                data.visualTyreCompound, DataStorePolicy.ON_CHANGE)
            set(status_data['tyresAgeLaps'], timestamp,
                data.tyresAgeLaps, DataStorePolicy.ON_CHANGE)
            set(status_data['vehicleFiaFlags'], timestamp,
                data.vehicleFiaFlags, DataStorePolicy.ON_CHANGE)
            set(status_data['ersStoreEnergy'], timestamp,
                data.ersStoreEnergy, DataStorePolicy.ON_CHANGE)
            set(status_data['ersDeployMode'], timestamp,
                data.ersDeployMode, DataStorePolicy.ON_CHANGE)
            set(status_data['ersHarvestedThisLapMGUK'], timestamp,
                data.ersHarvestedThisLapMGUK, DataStorePolicy.ON_CHANGE)
            set(status_data['ersHarvestedThisLapMGUH'], timestamp,
                data.ersHarvestedThisLapMGUH, DataStorePolicy.ON_CHANGE)
            set(status_data['ersDeployedThisLap'], timestamp,
                data.ersDeployedThisLap, DataStorePolicy.ON_CHANGE)
            set(status_data['networkPaused'], timestamp,
                data.networkPaused, DataStorePolicy.ON_CHANGE)

    def filter_car_telemetry(self, packet: CarTelemetryPacket):
        timestamp = packet.sessionTime
        for index, data in enumerate(packet.carTelemetryData):
            telem_data = self.data['car_telemetry'][index]
            set(telem_data['speed'], timestamp, data.speed,
                DataStorePolicy.ON_CHANGE)
            # Storing this telemetry and motion data (below) with 3 decimal
            # precision shrinks the data file by ~30%.
            set(telem_data['throttle'], timestamp,
                float('%.3f' % (data.throttle)),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['steer'], timestamp,
                float('%.3f' % (data.steer)),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['brake'], timestamp,
                float('%.3f' % (data.brake)),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['clutch'], timestamp, data.clutch,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['gear'], timestamp, data.gear,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['engineRPM'], timestamp, data.engineRPM,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['drs'], timestamp, data.drs,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['revLightsPercent'], timestamp,
                data.revLightsPercent, DataStorePolicy.ON_CHANGE)
            set(telem_data['revLightsBitValue'], timestamp,
                data.revLightsBitValue, DataStorePolicy.ON_CHANGE)
            set(telem_data['brakesTemperature'], timestamp,
                tuple(x for x in data.brakesTemperature),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['tiresSurfaceTemperature'], timestamp,
                tuple(x for x in data.tiresSurfaceTemperature),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['tiresInnerTemperature'], timestamp,
                tuple(x for x in data.tiresInnerTemperature),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['engineTemperature'], timestamp,
                data.engineTemperature,
                DataStorePolicy.ON_CHANGE)
            set(telem_data['tiresPressure'], timestamp,
                tuple(x for x in data.tiresPressure),
                DataStorePolicy.ON_CHANGE)
            set(telem_data['surfaceType'], timestamp,
                tuple(x for x in data.surfaceType),
                DataStorePolicy.ON_CHANGE)

    def filter_event(self, packet: EventPacket):
        event_code = du.to_string(packet.eventStringCode)
        if event_code == EventStringCode.BUTTON.value:
            return
        if event_code == EventStringCode.SESSION_START.value:
            if self.is_session_started:
                logging.info(
                    'Duplicate session start detected: restarting session.')
                self._reset()
                self.filter_event(packet)
            else:
                logging.info('Session start detected.')
                self.is_session_started = True
                self.session_start_time = time.time()
                self.data['event'][event_code] = (
                    packet.sessionTime, event_code)
        elif event_code == EventStringCode.SESSION_END.value:
            logging.info(
                'Session end detected.')
            self.session_end_time = time.time()
            self.data['event'][event_code] = (
                packet.sessionTime, event_code)
        elif event_code == EventStringCode.FASTEST_LAP.value:
            data = cast(FastestLap, packet.eventDetails.FastestLap)
            self.data['event'][event_code].append((
                packet.sessionTime, event_code,
                data.vehicleIdx, data.lapTime))
        elif event_code == EventStringCode.RETIREMENT.value:
            data = cast(Retirement, packet.eventDetails.Retirement)
            self.data['event'][event_code].append((
                packet.sessionTime, event_code, data.vehicleIdx))
        elif event_code == EventStringCode.DRS_ENABLED.value:
            self.data['event'][event_code].append((
                packet.sessionTime, event_code))
        elif event_code == EventStringCode.DRS_DISABLED.value:
            self.data['event'][event_code].append((
                packet.sessionTime, event_code))
        elif event_code == EventStringCode.CHEQUERED_FLAG.value:
            self.data['event'][event_code] = (
                packet.sessionTime, event_code)
        elif event_code == EventStringCode.RACE_WINNER.value:
            data = cast(RaceWinner, packet.eventDetails.RaceWinner)
            self.data['event'][event_code] = (
                packet.sessionTime, event_code,
                data.vehicleIdx)
        elif event_code == EventStringCode.PENALTY.value:
            data = cast(Penalty, packet.eventDetails.Penalty)
            self.data['event'][event_code].append(
                (packet.sessionTime, event_code,
                    data.penaltyType,
                    data.infringementType,
                    data.vehicleIdx,
                    data.otherVehicleIdx,
                    data.time,
                    data.placesGained))
        elif event_code == EventStringCode.SPEED_TRAP.value:
            data = cast(SpeedTrap, packet.eventDetails.SpeedTrap)
            if data.isOverallFastestInSession == 1:
                self.data['event'][event_code].append((
                    packet.sessionTime,
                    event_code,
                    data.vehicleIdx,
                    data.speed))
        elif event_code == EventStringCode.START_LIGHTS.value:
            data = cast(StartLights, packet.eventDetails.StartLights)
            self.data['event'][event_code].append(
                (packet.sessionTime, event_code, data.numLights))
        elif event_code == EventStringCode.LIGHTS_OUT.value:
            self.data['event'][event_code] = (
                packet.sessionTime, event_code)
        elif event_code == EventStringCode.DRIVE_THROUGH_SERVED.value:
            data = cast(DriveThroughPenaltyServed,
                        packet.eventDetails.DriveThroughPenaltyServed)
            self.data['event'][event_code].append((
                packet.sessionTime, event_code,
                data.vehicleIdx))
        elif event_code == EventStringCode.STOP_GO_SERVED.value:
            data = cast(StopGoPenaltyServed,
                        packet.eventDetails.StopGoPenaltyServed)
            self.data['event'][event_code].append((
                packet.sessionTime, event_code,
                data.vehicleIdx))
        elif event_code == EventStringCode.FLASHBACK.value:
            data = cast(Flashback, packet.eventDetails.Flashback)
            self.data['event'][event_code].append(
                (packet.sessionTime, event_code,
                 data.flashbackSessionTime))

    def filter_final_classification(self, packet: FinalClassificationPacket):
        timestamp = packet.sessionTime
        self.data['final_classification']['numCars'] = packet.numCars
        for index, data in enumerate(packet.classificationData):
            data_list = self.data['final_classification']['data'][index]
            set(data_list['position'], timestamp, data.position,
                DataStorePolicy.FIRST)
            set(data_list['numLaps'], timestamp, data.numLaps,
                DataStorePolicy.FIRST)
            set(data_list['gridPosition'], timestamp, data.gridPosition,
                DataStorePolicy.FIRST)
            set(data_list['points'], timestamp, data.points,
                DataStorePolicy.FIRST)
            set(data_list['numPitStops'], timestamp, data.numPitStops,
                DataStorePolicy.FIRST)
            set(data_list['resultStatus'], timestamp, data.resultStatus,
                DataStorePolicy.FIRST)
            set(data_list['bestLapTimeInMS'], timestamp, data.bestLapTimeInMS,
                DataStorePolicy.FIRST)
            set(data_list['totalRaceTime'], timestamp, data.totalRaceTime,
                DataStorePolicy.FIRST)
            set(data_list['penaltiesTime'], timestamp, data.penaltiesTime,
                DataStorePolicy.FIRST)
            set(data_list['numPenalties'], timestamp, data.numPenalties,
                DataStorePolicy.FIRST)
            set(data_list['numTyreStints'], timestamp, data.numTyreStints,
                DataStorePolicy.FIRST)
            set(data_list['tyreStintsActual'], timestamp,
                tuple(x for x in data.tyreStintsActual), DataStorePolicy.FIRST)
            set(data_list['tyreStintsVisual'], timestamp,
                tuple(x for x in data.tyreStintsVisual), DataStorePolicy.FIRST)
            set(data_list['tyreStintEndLaps'], timestamp,
                tuple(x for x in data.tyreStintEndLaps), DataStorePolicy.FIRST)
        logging.info('Final classification received.')
        self._save_data()

    def filter_lap_data(self, packet: LapDataPacket):
        timestamp = packet.sessionTime
        for index, data in enumerate(packet.lapData):
            lap_data = self.data['lap_data'][index]
            set(lap_data['lastLapTimeInMS'], timestamp,
                data.lastLapTimeInMS, DataStorePolicy.ON_CHANGE)
            set(lap_data['currentLapTimeInMS'], timestamp,
                data.currentLapTimeInMS, DataStorePolicy.ON_CHANGE)
            set(lap_data['sector1TimeInMS'], timestamp,
                data.sector1TimeInMS, DataStorePolicy.ON_CHANGE)
            set(lap_data['sector2TimeInMS'], timestamp,
                data.sector2TimeInMS, DataStorePolicy.ON_CHANGE)
            set(lap_data['carPosition'], timestamp, data.carPosition,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['currentLapNum'], timestamp, data.currentLapNum,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['pitStatus'], timestamp, data.pitStatus,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['numPitStops'], timestamp, data.numPitStops,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['sector'], timestamp, data.sector,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['currentLapInvalid'], timestamp,
                data.currentLapInvalid, DataStorePolicy.ON_CHANGE)
            set(lap_data['penalties'], timestamp, data.penalties,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['warnings'], timestamp, data.warnings,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['numUnservedDriveThroughPens'], timestamp,
                data.numUnservedDriveThroughPens,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['numUnservedStopGoPens'], timestamp,
                data.numUnservedStopGoPens, DataStorePolicy.ON_CHANGE)
            set(lap_data['gridPosition'], timestamp, data.gridPosition,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['driverStatus'], timestamp, data.driverStatus,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['resultStatus'], timestamp, data.resultStatus,
                DataStorePolicy.ON_CHANGE)
            set(lap_data['pitLaneTimerActive'], timestamp,
                data.pitLaneTimerActive, DataStorePolicy.ON_CHANGE)
            set(lap_data['pitLaneTimeInLaneInMS'], timestamp,
                data.pitLaneTimeInLaneInMS, DataStorePolicy.ON_CHANGE)
            set(lap_data['pitStopTimerInMS'], timestamp,
                data.pitStopTimerInMS, DataStorePolicy.ON_CHANGE)
            set(lap_data['pitStopShouldServePen'], timestamp,
                data.pitStopShouldServePen, DataStorePolicy.ON_CHANGE)

    def filter_motion(self, packet: MotionPacket):
        for index, data in enumerate(packet.carMotionData):
            data_list = self.data['motion'][index]
            set(data_list['worldPositionX'], packet.sessionTime,
                float('%.3f' % (data.worldPositionX)),
                DataStorePolicy.ON_CHANGE)
            set(data_list['worldPositionY'], packet.sessionTime,
                float('%.3f' % (data.worldPositionY)),
                DataStorePolicy.ON_CHANGE)
            set(data_list['yaw'], packet.sessionTime,
                float('%.3f' % (data.yaw)),
                DataStorePolicy.ON_CHANGE)

    def filter_participants(self, packet: ParticipantsPacket):
        p_data = self.data['participants']
        if p_data['numActiveCars'] is None:
            p_data['numActiveCars'] = packet.numActiveCars
            for index, data in enumerate(packet.participants):
                participant = p_data['participants'][index]
                participant['aiControlled'] = data.aiControlled
                participant['driverId'] = data.driverId
                participant['networkId'] = data.networkId
                participant['teamId'] = data.teamId
                participant['myTeam'] = data.myTeam
                participant['raceNumber'] = data.raceNumber
                participant['nationality'] = data.nationality
                participant['name'] = du.to_string(data.name)
                participant['yourTelemetry'] = data.yourTelemetry

    def filter_session(self, packet: SessionPacket):
        session_data = self.data['session']
        set(session_data['sessionUID'], packet.sessionTime,
            packet.sessionUID, DataStorePolicy.FIRST)
        set(session_data['weather'], packet.sessionTime,
            packet.weather, DataStorePolicy.ON_CHANGE)
        set(session_data['trackTemperature'], packet.sessionTime,
            packet.trackTemperature, DataStorePolicy.ON_CHANGE)
        set(session_data['airTemperature'], packet.sessionTime,
            packet.airTemperature, DataStorePolicy.ON_CHANGE)
        set(session_data['totalLaps'], packet.sessionTime,
            packet.totalLaps, DataStorePolicy.FIRST)
        set(session_data['trackLength'], packet.sessionTime,
            packet.trackLength, DataStorePolicy.FIRST)
        set(session_data['sessionType'], packet.sessionTime,
            packet.sessionType, DataStorePolicy.FIRST)
        set(session_data['trackId'], packet.sessionTime,
            packet.trackId, DataStorePolicy.FIRST)
        set(session_data['formula'], packet.sessionTime,
            packet.formula, DataStorePolicy.FIRST)
        set(session_data['pitSpeedLimit'], packet.sessionTime,
            packet.pitSpeedLimit, DataStorePolicy.FIRST)
        set(session_data['gamePaused'], packet.sessionTime,
            packet.gamePaused, DataStorePolicy.ON_CHANGE)
        set(session_data['numMarshalZones'], packet.sessionTime,
            packet.numMarshalZones, DataStorePolicy.FIRST)
        session_data['marshalZones'].append((
            packet.sessionTime,
            [x.zoneFlag for x in packet.marshalZones]))
        set(session_data['safetyCarStatus'], packet.sessionTime,
            packet.safetyCarStatus, DataStorePolicy.ON_CHANGE)
        set(session_data['networkGame'], packet.sessionTime,
            packet.networkGame, DataStorePolicy.FIRST)
        set(session_data['forecastAccuracy'], packet.sessionTime,
            packet.forecastAccuracy, DataStorePolicy.FIRST)
        set(session_data['aiDifficulty'], packet.sessionTime,
            packet.aiDifficulty, DataStorePolicy.FIRST)
        set(session_data['seasonLinkIdentifier'], packet.sessionTime,
            packet.seasonLinkIdentifier, DataStorePolicy.FIRST)
        set(session_data['weekendLinkIdentifier'], packet.sessionTime,
            packet.weekendLinkIdentifier, DataStorePolicy.FIRST)
        set(session_data['sessionLinkIdentifier'], packet.sessionTime,
            packet.sessionLinkIdentifier, DataStorePolicy.FIRST)
        set(session_data['steeringAssist'], packet.sessionTime,
            packet.steeringAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['brakingAssist'], packet.sessionTime,
            packet.brakingAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['gearboxAssist'], packet.sessionTime,
            packet.gearboxAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['pitAssist'], packet.sessionTime,
            packet.pitAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['pitReleaseAssist'], packet.sessionTime,
            packet.pitReleaseAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['ERSAssist'], packet.sessionTime,
            packet.ERSAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['DRSAssist'], packet.sessionTime,
            packet.DRSAssist, DataStorePolicy.ON_CHANGE)
        set(session_data['dynamicRacingLine'], packet.sessionTime,
            packet.dynamicRacingLine, DataStorePolicy.ON_CHANGE)
        set(session_data['dynamicRacingLineType'], packet.sessionTime,
            packet.dynamicRacingLineType, DataStorePolicy.ON_CHANGE)
        set(session_data['gameMode'], packet.sessionTime,
            packet.gameMode, DataStorePolicy.FIRST)
        set(session_data['ruleSet'], packet.sessionTime,
            packet.ruleSet, DataStorePolicy.FIRST)
        set(session_data['timeOfDay'], packet.sessionTime,
            packet.timeOfDay, DataStorePolicy.ON_CHANGE)
        set(session_data['sessionLength'], packet.sessionTime,
            packet.sessionLength, DataStorePolicy.FIRST)

    def _reset(self):
        self.is_session_started = False
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
                } for _ in range(GRID_SIZE)],
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
                } for _ in range(GRID_SIZE)],
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
                        } for _ in range(GRID_SIZE)]
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
                } for _ in range(GRID_SIZE)],
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
                } for _ in range(GRID_SIZE)],
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
                } for _ in range(GRID_SIZE)],
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
                } for _ in range(GRID_SIZE)],
            'final_classification': {
                    'numCars': 0,
                    'data': [{
                        'position': [],
                        'numLaps': [],
                        'gridPosition': [],
                        'points': [],
                        'numPitStops': [],
                        'resultStatus': [],
                        'bestLapTimeInMS': [],
                        'totalRaceTime': [],
                        'penaltiesTime': [],
                        'numPenalties': [],
                        'numTyreStints': [],
                        'tyreStintsActual': [],
                        'tyreStintsVisual': [],
                        'tyreStintEndLaps': [],
                    } for _ in range(GRID_SIZE)],
                }
        }

    def _save_data(self):
        if self.data['participants']['numActiveCars'] is None:
            logging.info("No participants data: can't write file.")
            self._reset()
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
        filename = f'{track_name}_{session_type}_{session_uid}_fv\
{self.format_version}.json'
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
