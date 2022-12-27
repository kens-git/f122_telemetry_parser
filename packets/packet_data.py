from ctypes import (
    c_double, c_float, c_int8, c_int16, c_uint8, c_uint16, c_uint32, Union)
from constants.constants import MAX_TYRE_STINTS, TIRE_COUNT
from custom_types.game import F1PacketStructure, Name

"""This module contains dataclasses for data types contained in
the packets.
"""


class CarDamageData(F1PacketStructure):
    _fields_ = [
        ('tyresWear', c_float * TIRE_COUNT),
        ('tyresDamage', c_uint8 * TIRE_COUNT),
        ('brakesDamage', c_uint8 * TIRE_COUNT),
        ('frontLeftWingDamage', c_uint8),
        ('frontRightWingDamage', c_uint8),
        ('rearWingDamage', c_uint8),
        ('floorDamage', c_uint8),
        ('diffuserDamage', c_uint8),
        ('sidepodDamage', c_uint8),
        ('drsFault', c_uint8),
        ('ersFault', c_uint8),
        ('gearBoxDamage', c_uint8),
        ('engineDamage', c_uint8),
        ('engineMGUHWear', c_uint8),
        ('engineESWear', c_uint8),
        ('engineCEWear', c_uint8),
        ('engineICEWear', c_uint8),
        ('engineMGUKWear', c_uint8),
        ('engineTCWear', c_uint8),
        ('engineBlown', c_uint8),
        ('engineSeized', c_uint8),
    ]


class CarSetupsData(F1PacketStructure):
    _fields_ = [
        ('frontWing', c_uint8),
        ('rearWing', c_uint8),
        ('onThrottle', c_uint8),
        ('offThrottle', c_uint8),
        ('frontCamber', c_float),
        ('rearCamber', c_float),
        ('frontToe', c_float),
        ('rearToe', c_float),
        ('frontSuspension', c_uint8),
        ('rearSuspension', c_uint8),
        ('frontAntiRollBar', c_uint8),
        ('rearAntiRollBar', c_uint8),
        ('frontSuspensionHeight', c_uint8),
        ('rearSuspensionHeight', c_uint8),
        ('brakePressure', c_uint8),
        ('brakeBias', c_uint8),
        ('rearLeftTyrePressure', c_float),
        ('rearRightTyrePressure', c_float),
        ('frontLeftTyrePressure', c_float),
        ('frontRightTyrePressure', c_float),
        ('ballast', c_uint8),
        ('fuelLoad', c_float),
    ]


class CarStatusData(F1PacketStructure):
    _fields_ = [
        ('tractionControl', c_uint8),
        ('antiLockBrakes', c_uint8),
        ('fuelMix', c_uint8),
        ('frontBrakeBias', c_uint8),
        ('pitLimiterStatus', c_uint8),
        ('fuelInTank', c_float),
        ('fuelCapacity', c_float),
        ('fuelRemainingLaps', c_float),
        ('maxRPM', c_uint16),
        ('idleRPM', c_uint16),
        ('maxGears', c_uint8),
        ('drsAllowed', c_uint8),
        ('drsActivationDistance', c_uint16),
        ('actualTypeCompound', c_uint8),
        ('visualTyreCompound', c_uint8),
        ('tyresAgeLaps', c_uint8),
        ('vehicleFiaFlags', c_int8),
        ('ersStoreEnergy', c_float),
        ('ersDeployMode', c_uint8),
        ('ersHarvestedThisLapMGUK', c_float),
        ('ersHarvestedThisLapMGUH', c_float),
        ('ersDeployedThisLap', c_float),
        ('networkPaused', c_uint8),
    ]


class CarTelemetryData(F1PacketStructure):
    _fields_ = [
        ('speed', c_uint16),
        ('throttle', c_float),
        ('steer', c_float),
        ('brake', c_float),
        ('clutch', c_uint8),
        ('gear', c_int8),
        ('engineRPM', c_uint16),
        ('drs', c_uint8),
        ('revLightsPercent', c_uint8),
        ('revLightsBitValue', c_uint16),
        ('brakesTemperature', c_uint16 * TIRE_COUNT),
        ('tiresSurfaceTemperature', c_uint8 * TIRE_COUNT),
        ('tiresInnerTemperature', c_uint8 * TIRE_COUNT),
        ('engineTemperature', c_uint16),
        ('tiresPressure', c_float * TIRE_COUNT),
        ('surfaceType', c_uint8 * TIRE_COUNT),
    ]


class FinalClassificationData(F1PacketStructure):
    _fields_ = [
        ('position', c_uint8),
        ('numLaps', c_uint8),
        ('gridPosition', c_uint8),
        ('points', c_uint8),
        ('numPitStops', c_uint8),
        ('resultStatus', c_uint8),
        ('bestLapTimeInMS', c_uint32),
        ('totalRaceTime', c_double),
        ('penaltiesTime', c_uint8),
        ('numPenalties', c_uint8),
        ('numTyreStints', c_uint8),
        ('tyreStintsActual', c_uint8 * MAX_TYRE_STINTS),
        ('tyreStintsVisual', c_uint8 * MAX_TYRE_STINTS),
        ('tyreStintEndLaps', c_uint8 * MAX_TYRE_STINTS),
    ]


class LapDataData(F1PacketStructure):
    _fields_ = [
        ('lastLapTimeInMS', c_uint32),
        ('currentLapTimeInMS', c_uint32),
        ('sector1TimeInMS', c_uint16),
        ('sector2TimeInMS', c_uint16),
        ('lapDistance', c_float),
        ('totalDistance', c_float),
        ('safetyCarDelta', c_float),
        ('carPosition', c_uint8),
        ('currentLapNum', c_uint8),
        ('pitStatus', c_uint8),
        ('numPitStops', c_uint8),
        ('sector', c_uint8),
        ('currentLapInvalid', c_uint8),
        ('penalties', c_uint8),
        ('warnings', c_uint8),
        ('numUnservedDriveThroughPens', c_uint8),
        ('numUnservedStopGoPens', c_uint8),
        ('gridPosition', c_uint8),
        ('driverStatus', c_uint8),
        ('resultStatus', c_uint8),
        ('pitLaneTimerActive', c_uint8),
        ('pitLaneTimeInLaneInMS', c_uint16),
        ('pitStopTimerInMS', c_uint16),
        ('pitStopShouldServePen', c_uint8),
    ]


class LapHistoryData(F1PacketStructure):
    _fields_ = [
        ('lapTimeInMS', c_uint32),
        ('sector1TimeInMS', c_uint16),
        ('sector2TimeInMS', c_uint16),
        ('sector3TimeInMS', c_uint16),
        ('lapValidBitFlags', c_uint8),
    ]


class LobbyInfoData(F1PacketStructure):
    _fields_ = [
        ('aiControlled', c_uint8),
        ('teamId', c_uint8),
        ('nationality', c_uint8),
        ('name', Name),
        ('carNumber', c_uint8),
        ('readyStatus', c_uint8),
    ]


class MarshalZone(F1PacketStructure):
    _fields_ = [
        ('zoneStart', c_float),
        ('zoneFlag', c_int8),
    ]


class CarMotionData(F1PacketStructure):
    _fields_ = [
        ('worldPositionX', c_float),
        ('worldPositionY', c_float),
        ('worldPositionZ', c_float),
        ('worldVelocityX', c_float),
        ('worldVelocityY', c_float),
        ('worldVelocityZ', c_float),
        ('worldForwardDirX', c_int16),
        ('worldForwardDirY', c_int16),
        ('worldForwardDirZ', c_int16),
        ('worldRightDirX', c_int16),
        ('worldRightDirY', c_int16),
        ('worldRightDirZ', c_int16),
        ('gForceLateral', c_float),
        ('gForceLongitudinal', c_float),
        ('gForceVertical', c_float),
        ('yaw', c_float),
        ('pitch', c_float),
        ('roll', c_float),
    ]


class ParticipantsData(F1PacketStructure):
    _fields_ = [
        ('aiControlled', c_uint8),
        ('driverId', c_uint8),
        ('networkId', c_uint8),
        ('teamId', c_uint8),
        ('myTeam', c_uint8),
        ('raceNumber', c_uint8),
        ('nationality', c_uint8),
        ('name', Name),
        ('yourTelemetry', c_uint8),
    ]


class TyreStintHistoryData(F1PacketStructure):
    _fields_ = [
        ('endLap', c_uint8),
        ('tyreActualCompound', c_uint8),
        ('tyreVisualCompound', c_uint8),
    ]


class WeatherForecastSample(F1PacketStructure):
    _fields_ = [
        ('sessionType', c_uint8),
        ('timeOffset', c_uint8),
        ('weather', c_uint8),
        ('trackTemperature', c_int8),
        ('trackTemperatureChange', c_int8),
        ('airTemperature', c_int8),
        ('airTemperatureChange', c_int8),
        ('rainPercentage', c_uint8),
    ]


class FastestLap(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('lapTime', c_float),
    ]


class Retirement(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class TeamMateInPits(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class RaceWinner(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class Penalty(F1PacketStructure):
    _fields_ = [
        ('penaltyType', c_uint8),
        ('infringementType', c_uint8),
        ('vehicleIdx', c_uint8),
        ('otherVehicleIdx', c_uint8),
        ('time', c_uint8),
        ('lapNum', c_uint8),
        ('placesGained', c_uint8),
    ]


class SpeedTrap(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
        ('speed', c_float),
        ('isOverallFastestInSession', c_uint8),
        ('isDriverFastestInSession', c_uint8),
        ('fastestVehicleIdxInSession', c_uint8),
        ('fastestSpeedInSession', c_float),
    ]


class StartLights(F1PacketStructure):
    _fields_ = [
        ('numLights', c_uint8),
    ]


class DriveThroughPenaltyServed(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class StopGoPenaltyServed(F1PacketStructure):
    _fields_ = [
        ('vehicleIdx', c_uint8),
    ]


class Flashback(F1PacketStructure):
    _fields_ = [
        ('flashbackFrameIdentifier', c_uint32),
        ('flashbackSessionTime', c_float),
    ]


class Buttons(F1PacketStructure):
    _fields_ = [
        ('buttonStatus', c_uint32),
    ]


class EventDataDetails(Union):
    _fields_ = [
        ('FastestLap', FastestLap),
        ('Retirement', Retirement),
        ('TeamMateInPits', TeamMateInPits),
        ('RaceWinner', RaceWinner),
        ('Penalty', Penalty),
        ('SpeedTrap', SpeedTrap),
        ('StartLights', StartLights),
        ('DriveThroughPenaltyServed', DriveThroughPenaltyServed),
        ('StopGoPenaltyServed', StopGoPenaltyServed),
        ('Flashback', Flashback),
        ('Buttons', Buttons),
    ]
