from abc import ABC
from dataclasses import dataclass
from typing import Dict, Final, Tuple, Type
from constants.constants import EventStringCode, PacketId
from custom_types.basic import Float, Int8, UInt8, UInt16, UInt32, UInt64
from custom_types.game import CarCornerData, EventCode, GridData
from packets.packet_data import (
    CarDamageData, CarSetupsData, CarStatusData,
    CarTelemetryData, FinalClassificationData, LapDataData, LapHistoryData,
    LobbyInfoData, MarshalZone, MotionData, ParticipantsData,
    TyreStintHistoryData, WeatherForecastSample)

"""This module contains classes that correspond with the packets
output by the game.
"""


@dataclass
class Packet(ABC):
    packetFormat: UInt16
    gameMajorVersion: UInt8
    gameMinorVersion: UInt8
    packetVersion: UInt8
    packetId: UInt8
    sessionUID: UInt64
    sessionTime: Float
    frameIdentifier: UInt32
    playerCarIndex: UInt8
    secondaryPlayerCarIndex: UInt8


@dataclass
class CarDamagePacket(Packet):
    carDamageData: GridData[CarDamageData]


@dataclass
class CarSetupsPacket(Packet):
    carSetups: GridData[CarSetupsData]


@dataclass
class CarStatusPacket(Packet):
    carStatusData: GridData[CarStatusData]


@dataclass
class CarTelemetryPacket(Packet):
    carTelemetryData: GridData[CarTelemetryData]
    mfdPanelIndex: UInt8
    mfdPanelIndexSecondaryPlayer: UInt8
    suggestedGear: Int8


@dataclass
class EventPacket(Packet):
    eventStringCode: EventCode


@dataclass
class FastestLapPacket(EventPacket):
    vehicleIdx: UInt8
    lapTime: Float


@dataclass
class RetirementPacket(EventPacket):
    vehicleIdx: UInt8


@dataclass
class TeamMateInPitsPacket(EventPacket):
    vehicleIdx: UInt8


@dataclass
class RaceWinnerPacket(EventPacket):
    vehicleIdx: UInt8


@dataclass
class PenaltyPacket(EventPacket):
    penaltyType: UInt8
    infringementType: UInt8
    vehicleIdx: UInt8
    otherVehicleIdx: UInt8
    time: UInt8
    lapNum: UInt8
    placesGained: UInt8


@dataclass
class SpeedTrapPacket(EventPacket):
    vehicleIdx: UInt8
    speed: Float
    isOverallFastestInSession: UInt8
    isDriverFastestInSession: UInt8
    fastestVehicleIdxInSession: UInt8
    fastestSpeedInSession: Float


@dataclass
class StartLightsPacket(EventPacket):
    numLights: UInt8


@dataclass
class DriveThroughPenaltyServedPacket(EventPacket):
    vehicleIdx: UInt8


@dataclass
class StopGoPenaltyServedPacket(EventPacket):
    vehicleIdx: UInt8


@dataclass
class FlashbackPacket(EventPacket):
    flashbackFrameIdentifier: UInt32
    flashbackSessionTime: Float


@dataclass
class ButtonsPacket(EventPacket):
    buttonStatus: UInt32


@dataclass
class FinalClassificationPacket(Packet):
    numCars: UInt8
    classificationData: GridData[FinalClassificationData]


@dataclass
class LapDataPacket(Packet):
    lapData: GridData[LapDataData]
    timeTrialPBCarIdx: UInt8
    timeTrialRivalCarIdx: UInt8


@dataclass
class LobbyInfoPacket(Packet):
    numPlayers: UInt8
    lobbyPlayers: GridData[LobbyInfoData]


@dataclass
class MotionPacket(Packet):
    carMotionData: GridData[MotionData]
    suspensionPosition: CarCornerData[Float]
    suspensionVelocity: CarCornerData[Float]
    suspensionAcceleration: CarCornerData[Float]
    wheelSpeed: CarCornerData[Float]
    wheelSlip: CarCornerData[Float]
    localVelocityX: Float
    localVelocityY: Float
    localVelocityZ: Float
    angularVelocityX: Float
    angularVelocityY: Float
    angularVelocityZ: Float
    angularAccelerationX: Float
    angularAccelerationY: Float
    angularAccelerationZ: Float
    frontWheelsAngle: Float


@dataclass
class ParticipantsPacket(Packet):
    numActiveCars: UInt8
    participants: GridData[ParticipantsData]


@dataclass
class SessionHistoryPacket(Packet):
    carIdx: UInt8
    numLaps: UInt8
    numTyreStints: UInt8
    bestLapTimeLapNum: UInt8
    bestSector1LapNum: UInt8
    bestSector2LapNum: UInt8
    bestSector3LapNum: UInt8
    lapHistoryData: Tuple[
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData, LapHistoryData, LapHistoryData,
        LapHistoryData,
    ]
    tyreStintHistoryData: Tuple[
        TyreStintHistoryData, TyreStintHistoryData,
        TyreStintHistoryData, TyreStintHistoryData,
        TyreStintHistoryData, TyreStintHistoryData,
        TyreStintHistoryData, TyreStintHistoryData,
    ]


@dataclass
class SessionPacket(Packet):
    weather: UInt8
    trackTemperature: Int8
    airTemperature: Int8
    totalLaps: UInt8
    trackLength: UInt16
    sessionType: UInt8
    trackId: Int8
    formula: UInt8
    sessionTimeLeft: UInt16
    sessionDuration: UInt16
    pitSpeedLimit: UInt8
    gamePaused: UInt8
    isSpectating: UInt8
    spectatorCarIndex: UInt8
    sliProNativeSupport: UInt8
    numMarshalZones: UInt8
    marshalZones: Tuple[
        MarshalZone, MarshalZone, MarshalZone, MarshalZone,
        MarshalZone, MarshalZone, MarshalZone, MarshalZone,
        MarshalZone, MarshalZone, MarshalZone, MarshalZone,
        MarshalZone, MarshalZone, MarshalZone, MarshalZone,
        MarshalZone, MarshalZone, MarshalZone, MarshalZone,
        MarshalZone,
    ]
    safetyCarStatus: UInt8
    networkGame: UInt8
    numWeatherForecastSamples: UInt8
    weatherForecastSamples: Tuple[
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
        WeatherForecastSample, WeatherForecastSample,
    ]
    forecastAccuracy: UInt8
    aiDifficulty: UInt8
    seasonLinkIdentifier: UInt32
    weekendLinkIdentifier: UInt32
    sessionLinkIdentifier: UInt32
    pitStopWindowIdealLap: UInt8
    pitStopWindowLatestLap: UInt8
    pitStopRejoinPosition: UInt8
    steeringAssist: UInt8
    brakingAssist: UInt8
    gearboxAssist: UInt8
    pitAssist: UInt8
    pitReleaseAssist: UInt8
    ERSAssist: UInt8
    DRSAssist: UInt8
    dynamicRacingLine: UInt8
    dynamicRacingLineType: UInt8
    gameMode: UInt8
    ruleSet: UInt8
    timeOfDay: UInt32
    sessionLength: UInt8


PACKET_TYPE: Final[Dict[int, Type[Packet]]] = {
    PacketId.MOTION.value: MotionPacket,
    PacketId.SESSION.value: SessionPacket,
    PacketId.LAP_DATA.value: LapDataPacket,
    PacketId.EVENT.value: EventPacket,
    PacketId.PARTICIPANTS.value: ParticipantsPacket,
    PacketId.CAR_SETUPS.value: CarSetupsPacket,
    PacketId.CAR_TELEMETRY.value: CarTelemetryPacket,
    PacketId.CAR_STATUS.value: CarStatusPacket,
    PacketId.FINAL_CLASSIFICATION.value: FinalClassificationPacket,
    PacketId.LOBBY_INFO.value: LobbyInfoPacket,
    PacketId.CAR_DAMAGE.value: CarDamagePacket,
    PacketId.SESSION_HISTORY.value: SessionHistoryPacket,
}


EVENT_DETAILS_TYPE: Final[Dict[str, Type[EventPacket]]] = {
    EventStringCode.SESSION_START.value: EventPacket,
    EventStringCode.SESSION_END.value: EventPacket,
    EventStringCode.FASTEST_LAP.value: FastestLapPacket,
    EventStringCode.RETIREMENT.value: RetirementPacket,
    EventStringCode.DRS_ENABLED.value: EventPacket,
    EventStringCode.DRS_DISABLED.value: EventPacket,
    EventStringCode.TEAM_MATE_IN_PITS.value: TeamMateInPitsPacket,
    EventStringCode.CHEQUERED_FLAG.value: EventPacket,
    EventStringCode.RACE_WINNER.value: RaceWinnerPacket,
    EventStringCode.PENALTY.value: PenaltyPacket,
    EventStringCode.SPEED_TRAP.value: SpeedTrapPacket,
    EventStringCode.START_LIGHTS.value: StartLightsPacket,
    EventStringCode.LIGHTS_OUT.value: EventPacket,
    EventStringCode.DRIVE_THROUGH_SERVED.value:
        DriveThroughPenaltyServedPacket,
    EventStringCode.STOP_GO_SERVED.value: StopGoPenaltyServedPacket,
    EventStringCode.FLASHBACK.value: FlashbackPacket,
    EventStringCode.BUTTON.value: ButtonsPacket,
}
"""Returns the packet type associated with a event string code."""
