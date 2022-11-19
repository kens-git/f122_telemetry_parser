import dataclasses
import typing
import custom_types.basic as bt


T = typing.TypeVar('T')


CarCornerData = typing.Tuple[T, T, T, T]


TyreStintData = typing.Tuple[T, T, T, T, T, T, T, T]


Name = typing.Tuple[
    bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char,
    bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char,
    bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char,
    bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char,
    bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char,
    bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char, bt.Char,
]


@dataclasses.dataclass
class CarDamageData:
    tyresWear: CarCornerData[bt.Float]
    tyresDamage: CarCornerData[bt.UInt8]
    brakesDamage: CarCornerData[bt.UInt8]
    frontLeftWingDamage: bt.UInt8
    frontRightWingDamage: bt.UInt8
    rearWingDamage: bt.UInt8
    floorDamage: bt.UInt8
    diffuserDamage: bt.UInt8
    sidepodDamage: bt.UInt8
    drsFault: bt.UInt8
    ersFault: bt.UInt8
    gearBoxDamage: bt.UInt8
    engineDamage: bt.UInt8
    engineMGUHWear: bt.UInt8
    engineESWear: bt.UInt8
    engineCEWear: bt.UInt8
    engineICEWear: bt.UInt8
    engineMGUKWear: bt.UInt8
    engineTCWear: bt.UInt8
    engineBlown: bt.UInt8
    engineSeized: bt.UInt8


@dataclasses.dataclass
class CarSetupsData:
    frontWing: bt.UInt8
    rearWing: bt.UInt8
    onThrottle: bt.UInt8
    offThrottle: bt.UInt8
    frontCamber: bt.Float
    rearCamber: bt.Float
    frontToe: bt.Float
    rearToe: bt.Float
    frontSuspension: bt.UInt8
    rearSuspension: bt.UInt8
    frontAntiRollBar: bt.UInt8
    rearAntiRollBar: bt.UInt8
    frontSuspensionHeight: bt.UInt8
    rearSuspensionHeight: bt.UInt8
    brakePressure: bt.UInt8
    brakeBias: bt.UInt8
    rearLeftTyrePressure: bt.Float
    rearRightTyrePressure: bt.Float
    frontLeftTyrePressure: bt.Float
    frontRightTyrePressure: bt.Float
    ballast: bt.UInt8
    fuelLoad: bt.Float


@dataclasses.dataclass
class CarStatusData:
    tractionControl: bt.UInt8
    antiLockBrakes: bt.UInt8
    fuelMix: bt.UInt8
    frontBrakeBias: bt.UInt8
    pitLimiterStatus: bt.UInt8
    fuelInTank: bt.Float
    fuelCapacity: bt.Float
    fuelRemainingLaps: bt.Float
    maxRPM: bt.UInt16
    idleRPM: bt.UInt16
    maxGears: bt.UInt8
    drsAllowed: bt.UInt8
    drsActivationDistance: bt.UInt16
    actualTypeCompound: bt.UInt8
    visualTyreCompound: bt.UInt8
    tyresAgeLaps: bt.UInt8
    vehicleFiaFlags: bt.Int8
    ersStoreEnergy: bt.Float
    ersDeployMode: bt.UInt8
    ersHarvestedThisLapMGUK: bt.Float
    ersHarvestedThisLapMGUH: bt.Float
    ersDeployedThisLap: bt.Float
    networkPaused: bt.UInt8


@dataclasses.dataclass
class CarTelemetryData:
    speed: bt.UInt16
    throttle: bt.Float
    steer: bt.Float
    brake: bt.Float
    clutch: bt.UInt8
    gear: bt.Int8
    engineRPM: bt.UInt16
    drs: bt.UInt8
    revLightsPercent: bt.UInt8
    revLightsBitValue: bt.UInt16
    brakesTemperature: CarCornerData[bt.UInt16]
    tiresSurfaceTemperature: CarCornerData[bt.UInt8]
    tiresInnerTemperature: CarCornerData[bt.UInt8]
    engineTemperature: bt.UInt16
    tiresPressure: CarCornerData[bt.Float]
    surfaceType: CarCornerData[bt.UInt8]


@dataclasses.dataclass
class FinalClassificationData:
    position: bt.UInt8
    numLaps: bt.UInt8
    gridPosition: bt.UInt8
    points: bt.UInt8
    numPitStops: bt.UInt8
    resultStatus: bt.UInt8
    bestLapTimeInMS: bt.UInt32
    totalRaceTime: bt.Double
    penaltiesTime: bt.UInt8
    numPenalties: bt.UInt8
    numTyreStints: bt.UInt8
    tyreStintsActual: TyreStintData[bt.UInt8]
    tyreStintsVisual: TyreStintData[bt.UInt8]
    tyreStintEndLaps: TyreStintData[bt.UInt8]


@dataclasses.dataclass
class LapDataData:
    lastLapTimeInMS: bt.UInt32
    currentLapTimeInMS: bt.UInt32
    sector1TimeInMS: bt.UInt16
    sector2TimeInMS: bt.UInt16
    lapDistance: bt.Float
    totalDistance: bt.Float
    safetyCarDelta: bt.Float
    carPosition: bt.UInt8
    currentLapNum: bt.UInt8
    pitStatus: bt.UInt8
    numPitStops: bt.UInt8
    sector: bt.UInt8
    currentLapInvalid: bt.UInt8
    penalties: bt.UInt8
    warnings: bt.UInt8
    numUnservedDriveThroughPens: bt.UInt8
    numUnservedStopGoPens: bt.UInt8
    gridPosition: bt.UInt8
    driverStatus: bt.UInt8
    resultStatus: bt.UInt8
    pitLaneTimerActive: bt.UInt8
    pitLaneTimeInLaneInMS: bt.UInt16
    pitStopTimerInMS: bt.UInt16
    pitStopShouldServePen: bt.UInt8


@dataclasses.dataclass
class LapHistoryData:
    lapTimeInMS: bt.UInt32
    sector1TimeInMS: bt.UInt16
    sector2TimeInMS: bt.UInt16
    sector3TimeInMS: bt.UInt16
    lapValidBitFlags: bt.UInt8


@dataclasses.dataclass
class LobbyInfoData:
    aiControlled: bt.UInt8
    teamId: bt.UInt8
    nationality: bt.UInt8
    name: Name
    carNumber: bt.UInt8
    readyStatus: bt.UInt8


@dataclasses.dataclass
class MarshalZone:
    zoneStart: bt.Float
    zoneFlag: bt.Int8


@dataclasses.dataclass
class MotionData:
    worldPositionX: bt.Float
    worldPositionY: bt.Float
    worldPositionZ: bt.Float
    worldVelocityX: bt.Float
    worldVelocityY: bt.Float
    worldVelocityZ: bt.Float
    worldForwardDirX: bt.Int16
    worldForwardDirY: bt.Int16
    worldForwardDirZ: bt.Int16
    worldRightDirX: bt.Int16
    worldRightDirY: bt.Int16
    worldRightDirZ: bt.Int16
    gForceLateral: bt.Float
    gForceLongitudinal: bt.Float
    gForceVertical: bt.Float
    yaw: bt.Float
    pitch: bt.Float
    roll: bt.Float


@dataclasses.dataclass
class ParticipantsData:
    aiControlled: bt.UInt8
    driverId: bt.UInt8
    networkId: bt.UInt8
    teamId: bt.UInt8
    myTeam: bt.UInt8
    raceNumber: bt.UInt8
    nationality: bt.UInt8
    name: Name
    yourTelemetry: bt.UInt8


@dataclasses.dataclass
class TyreStintHistoryData:
    endLap: bt.UInt8
    tyreActualCompound: bt.UInt8
    tyreVisualCompound: bt.UInt8


@dataclasses.dataclass
class WeatherForecastSample:
    sessionType: bt.UInt8
    timeOffset: bt.UInt8
    weather: bt.UInt8
    trackTemperature: bt.Int8
    trackTemperatureChange: bt.Int8
    airTemperature: bt.Int8
    airTemperatureChange: bt.Int8
    rainPercentage: bt.UInt8
