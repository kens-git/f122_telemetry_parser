from dataclasses import fields
from inspect import isclass
from typing import Any, cast, get_args, get_origin, Set, Type
from constants.constants import PACKET_HEADER_LENGTH
from custom_types.basic import BasicType, BASIC_TYPE_FORMAT
from custom_types.game import EventCode
from custom_types.generic import T
from custom_types.Ref import Ref
from packets.packets import (
    EVENT_DETAILS_TYPE, EventPacket, Packet, PACKET_TYPE)
from packets.packet_data import (
    CarDamageData, CarSetupsData, CarStatusData, CarTelemetryData,
    FinalClassificationData, LapDataData, LobbyInfoData,
    MotionData, ParticipantsData, LapHistoryData,
    TyreStintHistoryData, MarshalZone, WeatherForecastSample)
import utilities.data as du
from utilities.packet import get_packet_id


GameData: Set[Any] = {
    CarDamageData, CarSetupsData, CarStatusData, CarTelemetryData,
    FinalClassificationData, LapDataData, LobbyInfoData,
    MotionData, ParticipantsData, LapHistoryData,
    TyreStintHistoryData, MarshalZone, WeatherForecastSample,
}


def parse_from_bytes(
        data: bytes, index: Ref[int], DataType: Type[T]) -> T:
    if isclass(DataType):
        if issubclass(DataType, BasicType):
            value = du.unpack(data, index.value, DataType)
            index.value += BASIC_TYPE_FORMAT[DataType].size
            return cast(T, value)
        if issubclass(DataType, EventPacket):
            return DataType(parse_from_bytes(data, index, field.type) for
                            field in fields(DataType))  # type: ignore
    if get_origin(DataType) is tuple:
        return cast(T, tuple(parse_from_bytes(data, index, e) for
                             e in get_args(DataType)))
    if DataType in GameData:
        return DataType(*[parse_from_bytes(data, index, field.type) for
                        field in fields(DataType)])
    raise ValueError(
        f'Unexpected type received by parse_data: {DataType}.')


def parse_packet(data: bytes) -> Packet:
    PacketType = PACKET_TYPE[get_packet_id(data)]
    if PacketType is EventPacket:
        event_code = du.to_string(parse_from_bytes(
            data, Ref(PACKET_HEADER_LENGTH), EventCode))
        PacketType = EVENT_DETAILS_TYPE[event_code]
    index = Ref[int](0)
    return PacketType(*[parse_from_bytes(data, index, field.type) for
                      field in fields(PacketType)])
