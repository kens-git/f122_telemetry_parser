import datetime
import logging
import typing
import constants.constants as const
from constants.constants import PenaltyId
import filters.Filter as fil
import packets.packet_data as pd
import packets.packets as pk
import utilities.data as du


PENALTY_STRINGS: typing.Dict[int, str] = {
    0: 'drive through',
    1: 'stop-go',
    2: 'grid penalty',
    3: 'penalty reminder',
    4: 'time penalty',
    5: 'warning',
    6: 'disqualified',
    7: 'removed from formation lap',
    8: 'parked too long timer',
    9: 'tire regulations',
    10: 'this lap invalidated',
    11: 'this and next lap invalidated',
    12: 'this lap invalidated without reason',
    13: 'this and next lap invalidated without reason',
    14: 'this and previous lap invalidated',
    15: 'this and previous lap invalidated without reason',
    16: 'retired',
    17: 'black flag timer',
}

INFRINGEMENT_STRINGS: typing.Dict[int, str] = {
    0: 'blocking by slow driving',
    1: 'blocking by driving the wrong way',
    2: 'reversing off the start line',
    3: 'a severe collision',
    4: 'a minor collision',
    5: 'a collision and failure to relinquish a position',
    6: 'a collision and failure to relinquish multiple positions',
    7: 'corner cutting resulting in a time gain',
    8: 'corner cutting resulting in a single position gained',
    9: 'corner cutting resulting in multiple positions gained',
    10: 'crossing the pit exit lane',
    11: 'ignoring blue flags',
    12: 'ignoring yellow flags',
    13: 'ignoring a drive through',
    14: 'too many drive throughs',
    15: 'drive through reminder serve within n laps',
    16: 'drive through reminder serve this lap',
    17: 'pit lane speeding',
    18: 'parking for too long',
    19: 'ignoring tire regulations',
    20: 'being assessed too many penalties',
    21: 'multiple warnings',
    22: 'approaching disqualification',
    23: 'tire regulations select single',
    24: 'tire regulations select multiple',
    25: 'corner cutting',
    26: 'running wide',
    27: 'corner cutting with a minor time gain',
    28: 'corner cutting with a significant time gain',
    29: 'corner cutting with an extreme time gain',
    30: 'wall riding',
    31: 'using a flashback',
    32: 'resetting to the track',
    33: 'blocking the pit lane',
    34: 'a jump start',
    35: 'a safety car to car collision',
    36: 'a safety car illegal overtake',
    37: 'exceeding the allowed safety car pace',
    38: 'exceeding the allowed virtual safety car pace',
    39: 'being below the allowed formation lap speed',
    40: 'improper formation lap parking',
    41: 'retired mechanical failure',
    42: 'retired terminally damaged',
    43: 'falling too far back of the safety car',
    44: 'black flag timer',
    45: 'an unserved stop go penalty',
    46: 'an unserved drive through penalty',
    47: 'an engine component change',
    48: 'a gearbox change',
    49: 'a parc fermé change',
    50: 'a league grid penalty',
    51: 'a retry',
    52: 'an illegal time gain',
    53: 'a mandatory pitstop',
    54: 'attribute assigned',
}


GENERIC_PENALTY_IDS = (
    PenaltyId.DRIVE_THROUGH.value, PenaltyId.STOP_GO.value,
    PenaltyId.GRID_PENALTY.value, PenaltyId.TYRE_REGULATIONS.value)

LAP_INVALIDATION_PENALTY_IDS = (
    PenaltyId.THIS_LAP_INVALIDATED.value,
    PenaltyId.THIS_AND_NEXT_LAP_INVALIDATED.value,
    PenaltyId.THIS_LAP_INVALIDATED_WITHOUT_REASON.value,
    PenaltyId.LAP_INVALIDATED_WITHOUT_REASON.value,
    PenaltyId.THIS_AND_PREVIOUS_LAP_INVALIDATED.value,
    PenaltyId.THIS_AND_PREVIOUS_LAP_INVALIDATED_WITHOUT_REASON.value)

IGNORED_PENALTY_IDS = (
    PenaltyId.PENALTY_REMINDER.value,
    PenaltyId.PARKED_TOO_LONG_TIMER.value,
    PenaltyId.RETIRED.value,
    PenaltyId.BLACK_FLAG_TIMER.value)


def print_with_session_timestamp(timestamp: float, string: str):
    time_string = (str(datetime.timedelta(seconds=timestamp))[:-3] if
                   timestamp != 0 else '0:00:00.000')
    logging.info(f'[{time_string}] {string}')


def create_time_of_day_string(timestamp: int) -> str:
    return str(datetime.timedelta(minutes=timestamp))


def create_penalty_string(
        penalty_id: int, infringement_id: int, offender: str,
        second_driver: typing.Optional[str] = None,
        time: typing.Optional[int] = None):
    penalty = PENALTY_STRINGS[penalty_id]
    infringement = INFRINGEMENT_STRINGS[infringement_id]
    if penalty_id in GENERIC_PENALTY_IDS:
        return f'{offender} has been assessed a {penalty} for {infringement}.'
    if penalty_id in LAP_INVALIDATION_PENALTY_IDS:
        return f'{offender} has {penalty} for {infringement}.'
    if penalty_id == PenaltyId.REMOVED_FROM_FORMATION_LAP.value:
        return f'{offender} has been {penalty} for {infringement}.'
    second_driver = (f' with {second_driver}'
                     if second_driver is not None else '')
    if penalty_id == PenaltyId.TIME_PENALTY.value:
        time_str = f'{time}s' if time is not None else ''
        return f'{offender} has been assessed a {time_str} {penalty} for \
{infringement}{second_driver}.'
    if penalty_id == PenaltyId.WARNING.value:
        return f'{offender} has been issued a warning for \
{infringement}{second_driver}.'
    if penalty_id == PenaltyId.DISQUALIFIED.value:
        return f'{offender} has been disqualified for \
{infringement}{second_driver}.'
    raise ValueError('Unhandled penalty id in create_penalty_string')


def get_driver_name(driver_id: int, fallback_name: str):
    try:
        return const.DRIVER_NAMES[driver_id]
    except KeyError:
        pass
    return fallback_name


class LogFilter(fil.Filter):
    def __init__(self):
        self.data = {}
        self.session_displayed = False
        self.participants: typing.Optional[
            pk.GridData[pd.ParticipantsData]] = None
        self.numActiveCars: int = 0

    def filter(self, packet: pk.Packet):
        packet_id = packet.packetId.value
        if packet_id == 1:
            self._filter_session(typing.cast(pk.SessionPacket, packet))
        elif packet_id == 3:
            self._filter_event(typing.cast(pk.EventPacket, packet))
        elif packet_id == 4:
            self._filter_participants(
                typing.cast(pk.ParticipantsPacket, packet))

    def _get_driver_name(self, vehicle_index: int):
        participant = self.participants[vehicle_index]
        return get_driver_name(
            participant.driverId.value, du.to_string(participant.name))

    def _filter_session(self, packet: pk.SessionPacket):
        if self.session_displayed is True:
            return
        self.session_displayed = True
        logging.info(f'\t{const.TRACK_NAMES[packet.trackId.value]}')
        logging.info(f'\t{const.SESSION_TEXT[packet.sessionType.value]}')
        logging.info(f'\t{create_time_of_day_string(packet.timeOfDay.value)}')
        logging.info(f'\t{const.WEATHER_TEXT[packet.weather.value]}')
        logging.info(f'\tAir: {packet.airTemperature.value}°')
        logging.info(f'\tTrack: {packet.trackTemperature.value}°')

    def _filter_event(self, packet: pk.EventPacket):
        event_code = du.to_string(packet.eventStringCode)
        if event_code == 'SSTA':
            print_with_session_timestamp(
                packet.sessionTime.value, 'Session started.')
        elif event_code == 'SEND':
            print_with_session_timestamp(
                packet.sessionTime.value, 'Session ended.')
            self._reset()
        elif event_code == 'FTLP':
            packet = typing.cast(pk.FastestLapPacket, packet)
            driver_name = self._get_driver_name(packet.vehicleIdx.value)
            print_with_session_timestamp(
                packet.sessionTime.value,
                f'{driver_name} has set the fastest lap time of \
{str(datetime.timedelta(seconds=packet.lapTime.value))[3:-3]}.')
        elif event_code == 'RTMT':
            packet = typing.cast(pk.RetirementPacket, packet)
            driver_name = self._get_driver_name(packet.vehicleIdx.value)
            print_with_session_timestamp(
                packet.sessionTime.value,
                f'{driver_name} has retired from the session.')
        elif event_code == 'DRSE':
            print_with_session_timestamp(
                packet.sessionTime.value, 'DRS has been enabled.')
        elif event_code == 'DRSD':
            print_with_session_timestamp(
                packet.sessionTime.value, 'DRS has been disabled.')
        elif event_code == 'TMPT':
            print_with_session_timestamp(
                packet.sessionTime.value, 'Your teammate is in the pits.')
        elif event_code == 'CHQF':
            print_with_session_timestamp(
                packet.sessionTime.value,
                'The chequered flag has been waved.')
        elif event_code == 'RCWN':
            packet = typing.cast(pk.RaceWinnerPacket, packet)
            driver_name = self._get_driver_name(packet.vehicleIdx.value)
            print_with_session_timestamp(
                packet.sessionTime.value,
                f'{driver_name} has been declared the winner.')
        elif event_code == 'PENA':
            packet = typing.cast(pk.PenaltyPacket, packet)
            if packet.penaltyType.value in IGNORED_PENALTY_IDS:
                return
            other_vehicle = packet.otherVehicleIdx.value
            second_driver = (self._get_driver_name(other_vehicle)
                             if other_vehicle != 255 else None)
            time = packet.time.value if packet.time.value != 255 else None
            p_string = create_penalty_string(
                packet.penaltyType.value,
                packet.infringementType.value,
                self._get_driver_name(packet.vehicleIdx.value),
                second_driver=second_driver, time=time)
            print_with_session_timestamp(
                packet.sessionTime.value, p_string)
        elif event_code == 'SPTP':
            pass
        elif event_code == 'STLG':
            packet = typing.cast(pk.StartLightsPacket, packet)
            print_with_session_timestamp(
                packet.sessionTime.value, '*' * packet.numLights.value)
        elif event_code == 'LGOT':
            print_with_session_timestamp(
                packet.sessionTime.value,
                'It\'s lights out and away we go!')
        elif event_code == 'DTSV':
            packet = typing.cast(pk.DriveThroughPenaltyServedPacket,
                                 packet)
            driver_name = self._get_driver_name(packet.vehicleIdx.value)
            print_with_session_timestamp(
                packet.sessionTime.value,
                f'{driver_name} has served a drive through penalty.')
        elif event_code == 'SGSV':
            packet = typing.cast(pk.StopGoPenaltyServedPacket, packet)
            driver_name = self._get_driver_name(packet.vehicleIdx.value)
            print_with_session_timestamp(
                packet.sessionTime.value,
                f'{driver_name} has served a stop-and-go penalty.')
        elif event_code == 'FLBK':
            print_with_session_timestamp(
                packet.sessionTime.value, 'Flashback initiated.')

    def _filter_participants(self, packet: pk.ParticipantsPacket):
        if self.participants is not None:
            return
        self.participants = packet.participants
        self.numActiveCars = packet.numActiveCars.value

    def _reset(self):
        self.numActiveCars = 0
        self.participants = None
        self.session_displayed = False
