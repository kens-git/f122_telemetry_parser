from ctypes import Array
import datetime
import logging
from typing import cast, Dict, Optional
from constants.constants import (
    DRIVER_NAMES, EventStringCode, NULL_BYTE_VALUE, PenaltyId, SESSION_TEXT,
    TRACK_NAMES, WEATHER_TEXT)
from filters.Filter import Filter
from packets.packet_data import (
    DriveThroughPenaltyServed, FastestLap, ParticipantsData, Penalty,
    RaceWinner, Retirement, StartLights, StopGoPenaltyServed)
from packets.packets import (
    EventPacket, Packet, PacketId, ParticipantsPacket, SessionPacket)
import utilities.data as du


PENALTY_STRINGS: Dict[int, str] = {
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
"""Associates human-readable strings with penalty ids."""

INFRINGEMENT_STRINGS: Dict[int, str] = {
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
"""Associates human-readable strings with infringement ids."""


GENERIC_PENALTY_IDS = (
    PenaltyId.DRIVE_THROUGH.value, PenaltyId.STOP_GO.value,
    PenaltyId.GRID_PENALTY.value, PenaltyId.TYRE_REGULATIONS.value)
"""Generic penalties that affect a single driver."""

LAP_INVALIDATION_PENALTY_IDS = (
    PenaltyId.THIS_LAP_INVALIDATED.value,
    PenaltyId.THIS_AND_NEXT_LAP_INVALIDATED.value,
    PenaltyId.THIS_LAP_INVALIDATED_WITHOUT_REASON.value,
    PenaltyId.LAP_INVALIDATED_WITHOUT_REASON.value,
    PenaltyId.THIS_AND_PREVIOUS_LAP_INVALIDATED.value,
    PenaltyId.THIS_AND_PREVIOUS_LAP_INVALIDATED_WITHOUT_REASON.value)
"""Penalties that result in lap invalidation."""

IGNORED_PENALTY_IDS = (
    PenaltyId.PENALTY_REMINDER.value,
    PenaltyId.PARKED_TOO_LONG_TIMER.value,
    PenaltyId.RETIRED.value,
    PenaltyId.BLACK_FLAG_TIMER.value)
"""Penalties that are ignored by the LogFilter."""


def print_with_session_timestamp(timestamp: float, string: str):
    """Logs a string to the console with a session timestamp.

    Args:
        timestamp: The session timestamp.
        string: The string to log.
    """

    time_string = (str(datetime.timedelta(seconds=timestamp))[:-3] if
                   timestamp != 0 else '0:00:00.000')
    logging.info(f'[{time_string}] {string}')


def create_time_of_day_string(timestamp: int) -> str:
    """Creates a string for a time of day from a session timestamp.

    Args:
        timestamp: The session timestamp.

    Returns:
        A string displaying the time of day (e.g., 15:00:00)
    """

    return str(datetime.timedelta(minutes=timestamp))


def create_penalty_string(
        penalty_id: int, infringement_id: int, offender: str,
        second_driver: Optional[str] = None, time: Optional[int] = None):
    """Creates a human-friendly string of information about a penalty.

    Args:
        penalty_id: The id of the penalty.
        infringement_id: The id of the infringement.
        offender: The name of the offending driver.
        second_driver: The name of the second driver involved in the
            incident.
        time: The penalty time in seconds given to the offender.
    """
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


def get_driver_name(driver_id: int, fallback_name: str) -> str:
    """Returns a driver's name, or a fallback if it's not available.

    Args:
        driver_id: The id of the driver.
        fallback_name: Name to return if the queried name isn't available.

    Returns:
        The available driver name.
    """

    try:
        return DRIVER_NAMES[driver_id]
    except KeyError:
        pass
    return fallback_name


class LogFilter(Filter):
    """Defines a Filter that logs info about a session to the console."""

    def __init__(self):
        self.data = {}
        self.session_displayed = False
        self.participants: Optional[Array[ParticipantsData]] = None

    def _get_driver_name(self, vehicle_index: int):
        participant = cast(Array[ParticipantsData],
                           self.participants)[vehicle_index]
        return get_driver_name(
            participant.driverId, du.to_string(participant.name))

    def filter_session(self, packet: SessionPacket):
        if self.session_displayed is True:
            return
        self.session_displayed = True
        logging.info(f'\t{TRACK_NAMES[packet.trackId]}')
        logging.info(f'\t{SESSION_TEXT[packet.sessionType]}')
        logging.info(f'\t{create_time_of_day_string(packet.timeOfDay)}')
        logging.info(f'\t{WEATHER_TEXT[packet.weather]}')
        logging.info(f'\tAir: {packet.airTemperature}°')
        logging.info(f'\tTrack: {packet.trackTemperature}°')

    def filter_event(self, packet: EventPacket):
        event_code = du.to_string(packet.eventStringCode)
        if event_code == EventStringCode.SESSION_START.value:
            print_with_session_timestamp(
                packet.sessionTime, 'Session started.')
        elif event_code == EventStringCode.SESSION_END.value:
            print_with_session_timestamp(
                packet.sessionTime, 'Session ended.')
            self._reset()
        elif event_code == EventStringCode.FASTEST_LAP.value:
            data = cast(FastestLap, packet.eventDetails.FastestLap)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has set the fastest lap time of \
{str(datetime.timedelta(seconds=data.lapTime))[3:-3]}.')
        elif event_code == EventStringCode.RETIREMENT.value:
            data = cast(Retirement, packet.eventDetails.Retirement)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has retired from the session.')
        elif event_code == EventStringCode.DRS_ENABLED.value:
            print_with_session_timestamp(
                packet.sessionTime, 'DRS has been enabled.')
        elif event_code == EventStringCode.DRS_DISABLED.value:
            print_with_session_timestamp(
                packet.sessionTime, 'DRS has been disabled.')
        elif event_code == EventStringCode.TEAM_MATE_IN_PITS.value:
            print_with_session_timestamp(
                packet.sessionTime, 'Your teammate is in the pits.')
        elif event_code == EventStringCode.CHEQUERED_FLAG.value:
            print_with_session_timestamp(
                packet.sessionTime,
                'The chequered flag has been waved.')
        elif event_code == EventStringCode.RACE_WINNER.value:
            data = cast(RaceWinner, packet.eventDetails.RaceWinner)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has been declared the winner.')
        elif event_code == EventStringCode.PENALTY.value:
            data = cast(Penalty, packet.eventDetails.Penalty)
            if data.penaltyType in IGNORED_PENALTY_IDS:
                return
            other_vehicle = data.otherVehicleIdx
            second_driver = (self._get_driver_name(other_vehicle)
                             if other_vehicle != NULL_BYTE_VALUE else None)
            time = data.time if data.time != NULL_BYTE_VALUE else None
            p_string = create_penalty_string(
                data.penaltyType, data.infringementType,
                self._get_driver_name(data.vehicleIdx),
                second_driver=second_driver, time=time)
            print_with_session_timestamp(
                packet.sessionTime, p_string)
        elif event_code == EventStringCode.SPEED_TRAP.value:
            pass
        elif event_code == EventStringCode.START_LIGHTS.value:
            data = cast(StartLights, packet.eventDetails.StartLights)
            print_with_session_timestamp(
                packet.sessionTime, '*' * data.numLights)
        elif event_code == EventStringCode.LIGHTS_OUT.value:
            print_with_session_timestamp(
                packet.sessionTime,
                'It\'s lights out and away we go!')
        elif event_code == EventStringCode.DRIVE_THROUGH_SERVED.value:
            data = cast(DriveThroughPenaltyServed,
                        packet.eventDetails.DriveThroughPenaltyServed)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has served a drive through penalty.')
        elif event_code == EventStringCode.STOP_GO_SERVED.value:
            data = cast(StopGoPenaltyServed,
                        packet.eventDetails.StopGoPenaltyServed)
            driver_name = self._get_driver_name(data.vehicleIdx)
            print_with_session_timestamp(
                packet.sessionTime,
                f'{driver_name} has served a stop-and-go penalty.')
        elif event_code == EventStringCode.FLASHBACK.value:
            print_with_session_timestamp(
                packet.sessionTime, 'Flashback initiated.')

    def filter_participants(self, packet: ParticipantsPacket):
        if self.participants is not None:
            return
        self.participants = packet.participants

    def _reset(self):
        self.participants = None
        self.session_displayed = False
