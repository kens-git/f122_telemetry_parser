import dataclasses
import inspect
import typing
import constants.constants as const
import custom_types.basic as bt
import utilities.data as du
import utilities.packet as pu
import packets.packets as pk
import packets.packet_data as pd


T = typing.TypeVar('T')


GameData: typing.Set[typing.Any] = {
    pd.CarDamageData, pd.CarSetupsData, pd.CarStatusData, pd.CarTelemetryData,
    pd.FinalClassificationData, pd.LapDataData, pd.LobbyInfoData,
    pd.MotionData, pd.ParticipantsData, pd.LapHistoryData,
    pd.TyreStintHistoryData, pd.MarshalZone, pd.WeatherForecastSample,
}


# TODO: move
class Ref(typing.Generic[T]):
    def __init__(self, value: T):
        self.value: T = value


def parse_from_bytes(
        data: bytes, index: Ref[int], DataType: typing.Type[T]) -> T:
    if inspect.isclass(DataType):
        if issubclass(DataType, bt.BasicType):
            value = du.unpack(data, index.value, DataType)
            index.value += bt.BASIC_TYPE_FORMAT[DataType].size
            return typing.cast(T, value)
        if issubclass(DataType, pk.EventPacket):
            return DataType(parse_from_bytes(data, index, field.type) for
                            field in dataclasses.fields(DataType))  # type: ignore
    if typing.get_origin(DataType) is tuple:
        return typing.cast(T, tuple(parse_from_bytes(data, index, e) for
                           e in typing.get_args(DataType)))
    if DataType in GameData:
        return DataType(*[parse_from_bytes(data, index, field.type) for
                        field in dataclasses.fields(DataType)])
    raise ValueError(
        f'Unexpected type received by parse_data: {DataType}.')


def parse_packet(data: bytes) -> pk.Packet:
    PacketType = const.PACKET_TYPE[pu.get_packet_id(data)]
    if PacketType is pk.EventPacket:
        event_code = du.to_string(parse_from_bytes(
            data, Ref(const.PACKET_HEADER_LENGTH), pk.EventCode))
        PacketType = const.EVENT_DETAILS_TYPE[event_code]
    index = Ref[int](0)
    return PacketType(*[parse_from_bytes(data, index, field.type) for
                      field in dataclasses.fields(PacketType)])
