from dataclasses import dataclass
from custom_types.basic import (
    Double, Float, Int8, Int16, UInt8, UInt16, UInt32)
from custom_types.game import CarCornerData, Name, TyreStintData


@dataclass
class CarDamageData:
    tyresWear: CarCornerData[Float]
    tyresDamage: CarCornerData[UInt8]
    brakesDamage: CarCornerData[UInt8]
    frontLeftWingDamage: UInt8
    frontRightWingDamage: UInt8
    rearWingDamage: UInt8
    floorDamage: UInt8
    diffuserDamage: UInt8
    sidepodDamage: UInt8
    drsFault: UInt8
    ersFault: UInt8
    gearBoxDamage: UInt8
    engineDamage: UInt8
    engineMGUHWear: UInt8
    engineESWear: UInt8
    engineCEWear: UInt8
    engineICEWear: UInt8
    engineMGUKWear: UInt8
    engineTCWear: UInt8
    engineBlown: UInt8
    engineSeized: UInt8


@dataclass
class CarSetupsData:
    frontWing: UInt8
    rearWing: UInt8
    onThrottle: UInt8
    offThrottle: UInt8
    frontCamber: Float
    rearCamber: Float
    frontToe: Float
    rearToe: Float
    frontSuspension: UInt8
    rearSuspension: UInt8
    frontAntiRollBar: UInt8
    rearAntiRollBar: UInt8
    frontSuspensionHeight: UInt8
    rearSuspensionHeight: UInt8
    brakePressure: UInt8
    brakeBias: UInt8
    rearLeftTyrePressure: Float
    rearRightTyrePressure: Float
    frontLeftTyrePressure: Float
    frontRightTyrePressure: Float
    ballast: UInt8
    fuelLoad: Float


@dataclass
class CarStatusData:
    tractionControl: UInt8
    antiLockBrakes: UInt8
    fuelMix: UInt8
    frontBrakeBias: UInt8
    pitLimiterStatus: UInt8
    fuelInTank: Float
    fuelCapacity: Float
    fuelRemainingLaps: Float
    maxRPM: UInt16
    idleRPM: UInt16
    maxGears: UInt8
    drsAllowed: UInt8
    drsActivationDistance: UInt16
    actualTypeCompound: UInt8
    visualTyreCompound: UInt8
    tyresAgeLaps: UInt8
    vehicleFiaFlags: Int8
    ersStoreEnergy: Float
    ersDeployMode: UInt8
    ersHarvestedThisLapMGUK: Float
    ersHarvestedThisLapMGUH: Float
    ersDeployedThisLap: Float
    networkPaused: UInt8


@dataclass
class CarTelemetryData:
    speed: UInt16
    throttle: Float
    steer: Float
    brake: Float
    clutch: UInt8
    gear: Int8
    engineRPM: UInt16
    drs: UInt8
    revLightsPercent: UInt8
    revLightsBitValue: UInt16
    brakesTemperature: CarCornerData[UInt16]
    tiresSurfaceTemperature: CarCornerData[UInt8]
    tiresInnerTemperature: CarCornerData[UInt8]
    engineTemperature: UInt16
    tiresPressure: CarCornerData[Float]
    surfaceType: CarCornerData[UInt8]


@dataclass
class FinalClassificationData:
    position: UInt8
    numLaps: UInt8
    gridPosition: UInt8
    points: UInt8
    numPitStops: UInt8
    resultStatus: UInt8
    bestLapTimeInMS: UInt32
    totalRaceTime: Double
    penaltiesTime: UInt8
    numPenalties: UInt8
    numTyreStints: UInt8
    tyreStintsActual: TyreStintData[UInt8]
    tyreStintsVisual: TyreStintData[UInt8]
    tyreStintEndLaps: TyreStintData[UInt8]


@dataclass
class LapDataData:
    lastLapTimeInMS: UInt32
    currentLapTimeInMS: UInt32
    sector1TimeInMS: UInt16
    sector2TimeInMS: UInt16
    lapDistance: Float
    totalDistance: Float
    safetyCarDelta: Float
    carPosition: UInt8
    currentLapNum: UInt8
    pitStatus: UInt8
    numPitStops: UInt8
    sector: UInt8
    currentLapInvalid: UInt8
    penalties: UInt8
    warnings: UInt8
    numUnservedDriveThroughPens: UInt8
    numUnservedStopGoPens: UInt8
    gridPosition: UInt8
    driverStatus: UInt8
    resultStatus: UInt8
    pitLaneTimerActive: UInt8
    pitLaneTimeInLaneInMS: UInt16
    pitStopTimerInMS: UInt16
    pitStopShouldServePen: UInt8


@dataclass
class LapHistoryData:
    lapTimeInMS: UInt32
    sector1TimeInMS: UInt16
    sector2TimeInMS: UInt16
    sector3TimeInMS: UInt16
    lapValidBitFlags: UInt8


@dataclass
class LobbyInfoData:
    aiControlled: UInt8
    teamId: UInt8
    nationality: UInt8
    name: Name
    carNumber: UInt8
    readyStatus: UInt8


@dataclass
class MarshalZone:
    zoneStart: Float
    zoneFlag: Int8


@dataclass
class MotionData:
    worldPositionX: Float
    worldPositionY: Float
    worldPositionZ: Float
    worldVelocityX: Float
    worldVelocityY: Float
    worldVelocityZ: Float
    worldForwardDirX: Int16
    worldForwardDirY: Int16
    worldForwardDirZ: Int16
    worldRightDirX: Int16
    worldRightDirY: Int16
    worldRightDirZ: Int16
    gForceLateral: Float
    gForceLongitudinal: Float
    gForceVertical: Float
    yaw: Float
    pitch: Float
    roll: Float


@dataclass
class ParticipantsData:
    aiControlled: UInt8
    driverId: UInt8
    networkId: UInt8
    teamId: UInt8
    myTeam: UInt8
    raceNumber: UInt8
    nationality: UInt8
    name: Name
    yourTelemetry: UInt8


@dataclass
class TyreStintHistoryData:
    endLap: UInt8
    tyreActualCompound: UInt8
    tyreVisualCompound: UInt8


@dataclass
class WeatherForecastSample:
    sessionType: UInt8
    timeOffset: UInt8
    weather: UInt8
    trackTemperature: Int8
    trackTemperatureChange: Int8
    airTemperature: Int8
    airTemperatureChange: Int8
    rainPercentage: UInt8
