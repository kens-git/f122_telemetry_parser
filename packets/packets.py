import abc
import dataclasses
import typing
import custom_types.basic as bt
import packets.packet_data as pd


# TODO: type other Finals
PACKET_HEADER_LENGTH: typing.Final[int] = 24
PACKET_HEADER_ID_INDEX: typing.Final[int] = 5

T = typing.TypeVar('T')
GameEntityData = typing.Tuple[
    T, T, T, T, T, T, T, T, T, T,
    T, T, T, T, T, T, T, T, T, T,
    T, T,
]


EventCode = typing.Tuple[bt.Char, bt.Char, bt.Char, bt.Char]


@dataclasses.dataclass
class Packet(abc.ABC):
    packetFormat: bt.UInt16
    gameMajorVersion: bt.UInt8
    gameMinorVersion: bt.UInt8
    packetVersion: bt.UInt8
    packetId: bt.UInt8
    sessionUID: bt.UInt64
    sessionTime: bt.Float
    frameIdentifier: bt.UInt32
    playerCarIndex: bt.UInt8
    secondaryPlayerCarIndex: bt.UInt8


@dataclasses.dataclass
class CarDamagePacket(Packet):
    carDamageData: GameEntityData[pd.CarDamageData]


@dataclasses.dataclass
class CarSetupsPacket(Packet):
    carSetups: GameEntityData[pd.CarSetupsData]


@dataclasses.dataclass
class CarStatusPacket(Packet):
    carStatusData: GameEntityData[pd.CarStatusData]


@dataclasses.dataclass
class CarTelemetryPacket(Packet):
    carTelemetryData: GameEntityData[pd.CarTelemetryData]
    mfdPanelIndex: bt.UInt8
    mfdPanelIndexSecondaryPlayer: bt.UInt8
    suggestedGear: bt.Int8


@dataclasses.dataclass
class EventPacket(Packet):
    eventStringCode: EventCode


@dataclasses.dataclass
class FastestLapPacket(EventPacket):
    vehicleIdx: bt.UInt8
    lapTime: bt.Float


@dataclasses.dataclass
class RetirementPacket(EventPacket):
    vehicleIdx: bt.UInt8


@dataclasses.dataclass
class TeamMateInPitsPacket(EventPacket):
    vehicleIdx: bt.UInt8


@dataclasses.dataclass
class RaceWinnerPacket(EventPacket):
    vehicleIdx: bt.UInt8


@dataclasses.dataclass
class PenaltyPacket(EventPacket):
    penaltyType: bt.UInt8
    infringementType: bt.UInt8
    vehicleIdx: bt.UInt8
    otherVehicleIdx: bt.UInt8
    time: bt.UInt8
    lapNum: bt.UInt8
    placesGained: bt.UInt8


@dataclasses.dataclass
class SpeedTrapPacket(EventPacket):
    vehicleIdx: bt.UInt8
    speed: bt.Float
    isOverallFastestInSession: bt.UInt8
    isDriverFastestInSession: bt.UInt8
    fastestVehicleIdxInSession: bt.UInt8
    fastestSpeedInSession: bt.Float


@dataclasses.dataclass
class StartLightsPacket(EventPacket):
    numLights: bt.UInt8


@dataclasses.dataclass
class DriveThroughPenaltyServedPacket(EventPacket):
    vehicleIdx: bt.UInt8


@dataclasses.dataclass
class StopGoPenaltyServedPacket(EventPacket):
    vehicleIdx: bt.UInt8


@dataclasses.dataclass
class FlashbackPacket(EventPacket):
    flashbackFrameIdentifier: bt.UInt32
    flashbackSessionTime: bt.Float


@dataclasses.dataclass
class ButtonsPacket(EventPacket):
    buttonStatus: bt.UInt32


@dataclasses.dataclass
class FinalClassificationPacket(Packet):
    numCars: bt.UInt8
    classificationData: GameEntityData[pd.FinalClassificationData]


@dataclasses.dataclass
class LapDataPacket(Packet):
    lapData: GameEntityData[pd.LapDataData]
    timeTrialPBCarIdx: bt.UInt8
    timeTrialRivalCarIdx: bt.UInt8


@dataclasses.dataclass
class LobbyInfoPacket(Packet):
    numPlayers: bt.UInt8
    lobbyPlayers: GameEntityData[pd.LobbyInfoData]


@dataclasses.dataclass
class MotionPacket(Packet):
    carMotionData: GameEntityData[pd.MotionData]
    suspensionPosition: pd.CarCornerData[bt.Float]
    suspensionVelocity: pd.CarCornerData[bt.Float]
    suspensionAcceleration: pd.CarCornerData[bt.Float]
    wheelSpeed: pd.CarCornerData[bt.Float]
    wheelSlip: pd.CarCornerData[bt.Float]
    localVelocityX: bt.Float
    localVelocityY: bt.Float
    localVelocityZ: bt.Float
    angularVelocityX: bt.Float
    angularVelocityY: bt.Float
    angularVelocityZ: bt.Float
    angularAccelerationX: bt.Float
    angularAccelerationY: bt.Float
    angularAccelerationZ: bt.Float
    frontWheelsAngle: bt.Float


@dataclasses.dataclass
class ParticipantsPacket(Packet):
    numActiveCars: bt.UInt8
    participants: GameEntityData[pd.ParticipantsData]


@dataclasses.dataclass
class SessionHistoryPacket(Packet):
    carIdx: bt.UInt8
    numLaps: bt.UInt8
    numTyreStints: bt.UInt8
    bestLapTimeLapNum: bt.UInt8
    bestSector1LapNum: bt.UInt8
    bestSector2LapNum: bt.UInt8
    bestSector3LapNum: bt.UInt8
    lapHistoryData: typing.Tuple[
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData, pd.LapHistoryData, pd.LapHistoryData,
        pd.LapHistoryData,
    ]
    tyreStintHistoryData: typing.Tuple[
        pd.TyreStintHistoryData, pd.TyreStintHistoryData,
        pd.TyreStintHistoryData, pd.TyreStintHistoryData,
        pd.TyreStintHistoryData, pd.TyreStintHistoryData,
        pd.TyreStintHistoryData, pd.TyreStintHistoryData,
    ]


@dataclasses.dataclass
class SessionPacket(Packet):
    weather: bt.UInt8
    trackTemperature: bt.Int8
    airTemperature: bt.Int8
    totalLaps: bt.UInt8
    trackLength: bt.UInt16
    sessionType: bt.UInt8
    trackId: bt.Int8
    formula: bt.UInt8
    sessionTimeLeft: bt.UInt16
    sessionDuration: bt.UInt16
    pitSpeedLimit: bt.UInt8
    gamePaused: bt.UInt8
    isSpectating: bt.UInt8
    spectatorCarIndex: bt.UInt8
    sliProNativeSupport: bt.UInt8
    numMarshalZones: bt.UInt8
    marshalZones: typing.Tuple[
        pd.MarshalZone, pd.MarshalZone, pd.MarshalZone, pd.MarshalZone,
        pd.MarshalZone, pd.MarshalZone, pd.MarshalZone, pd.MarshalZone,
        pd.MarshalZone, pd.MarshalZone, pd.MarshalZone, pd.MarshalZone,
        pd.MarshalZone, pd.MarshalZone, pd.MarshalZone, pd.MarshalZone,
        pd.MarshalZone, pd.MarshalZone, pd.MarshalZone, pd.MarshalZone,
        pd.MarshalZone,
    ]
    safetyCarStatus: bt.UInt8
    networkGame: bt.UInt8
    numWeatherForecastSamples: bt.UInt8
    weatherForecastSamples: typing.Tuple[
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
        pd.WeatherForecastSample, pd.WeatherForecastSample,
    ]
    forecastAccuracy: bt.UInt8
    aiDifficulty: bt.UInt8
    seasonLinkIdentifier: bt.UInt32
    weekendLinkIdentifier: bt.UInt32
    sessionLinkIdentifier: bt.UInt32
    pitStopWindowIdealLap: bt.UInt8
    pitStopWindowLatestLap: bt.UInt8
    pitStopRejoinPosition: bt.UInt8
    steeringAssist: bt.UInt8
    brakingAssist: bt.UInt8
    gearboxAssist: bt.UInt8
    pitAssist: bt.UInt8
    pitReleaseAssist: bt.UInt8
    ERSAssist: bt.UInt8
    DRSAssist: bt.UInt8
    dynamicRacingLine: bt.UInt8
    dynamicRacingLineType: bt.UInt8
    gameMode: bt.UInt8
    ruleSet: bt.UInt8
    timeOfDay: bt.UInt32
    sessionLength: bt.UInt8
