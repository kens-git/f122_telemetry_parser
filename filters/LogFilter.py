import typing
import constants.constants as const
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
    7: 'Removed from formation lap',
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
    29: 'corner cutting with a significant time gain',
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


def print_penalty(penalty_id: int, infraction_id: int, offender: str,
                  second_driver: typing.Optional[str] = None,
                  time: typing.Optional[int] = None):
    p = PENALTY_STRINGS[penalty_id]
    i = INFRINGEMENT_STRINGS[infraction_id]
    t = ''
    if time is not None:
        t = f'{time}s'

    match penalty_id:
        case 0:
            print(f'{offender} has been assessed a {p} for {i}.')
        case 1:
            print(f'{offender} has been assessed a {p} for {i}.')
        case 2:
            print(f'{offender} has been assessed a {p} for {i}.')
        case 3:
            pass
        case 4:
            q = ''
            if second_driver is not None:
                q = f' with {second_driver}'
            print(f'{offender} has been assessed a {t} {p} for {i}{q}.')
        case 5:
            q = ''
            if second_driver is not None:
                q = f' with {second_driver}'
            print(f'{offender} has been issued a warning for {i}{q}.')
        case 6:
            print(f'{offender} has been disqualified for {i}.')
        case 7:
            print(f'{offender} has been {p} for {i}')
        case 8:
            print(f'{offender} has been assessed a {p} for {i}')
        case 9:
            print(f'{offender} has been assessed a {p} for {i}')
        case 10:
            print(f'{offender} has {p} for {i}')
        case 11:
            print(f'{offender} has {p} for {i}')
        case 12:
            print(f'{offender} has {p} for {i}')
        case 13:
            print(f'{offender} has {p} for {i}')
        case 14:
            print(f'{offender} has {p} for {i}')
        case 15:
            print(f'{offender} has {p} for {i}')
        case 16:
            pass
        case 17:
            pass
        case _:
            pass


class LogFilter(fil.Filter):
    def __init__(self):
        self.data = {}
        self.packet_count: int = 0
        self.participants: typing.Optional[
            pk.GameEntityData[pd.ParticipantsData]] = None
        self.numActiveCars: int = 0

    def filter(self, packet: pk.Packet):
        packet = typing.cast(const.PACKET_TYPE[packet.packetId.value], packet)
        match packet.packetId.value:
            case 1:
                self._filter_session(packet)
            case 2:
                self._filter_lap_data(packet)
            case 3:
                self._filter_event(packet)
            case 4:
                self._filter_participants(packet)
            case 10:
                self._filter_car_damage(packet)
            case _:
                pass  # TODO
        self.packet_count += 1

    def _filter_session(self, packet: pk.SessionPacket):
        pass

    def _filter_lap_data(self, packet: pk.LapDataPacket):
        pass

    def _filter_event(self, packet: pk.EventPacket):
        match du.to_string(packet.eventStringCode):
            case 'SSTA':
                print('Session started.')
            case 'SEND':
                print('Session ended.')
            case 'FTLP':
                # packet = typing.cast(pk.FastestLapPacket, packet)
                print('__Driver__ has set the fastest lap of __time__.')
            case 'RTMT':
                print('__Driver__ has retired from the session.')
            case 'DRSE':
                print('DRS has been enabled.')
            case 'DRSD':
                print('DRS has been disabled.')
            case 'TMPT':
                print('Your teammate is in the pits.')
            case 'CHQF':
                print('The chequered flag has been waved.')
            case 'RCWN':
                print('__Driver__ has been declared the winner.')
            case 'PENA':
                packet = typing.cast(pk.PenaltyPacket, packet)
                # ignore reminder, timer penalty events and retired penalties.
                if packet.penaltyType.value in (3, 8, 16, 17):
                    return
                s = packet.otherVehicleIdx.value
                time = None
                if packet.time.value != 255:
                    time = packet.time.value
                # TODO: assumes participants is initialized
                print_penalty(
                    packet.penaltyType.value,
                    packet.infringementType.value,
                    du.to_string(self.participants[packet.vehicleIdx.value].name),
                    second_driver=du.to_string(
                        self.participants[s].name) if s != 255 else None,
                    time=time)
            case 'SPTP':
                pass
            case 'STLG':
                packet = typing.cast(pk.StartLightsPacket, packet)
                print('*' * packet.numLights.value)
            case 'LGOT':
                print('It\'s lights out and away we go!')
            case 'DTSV':
                print('__Driver__ has served a drive through penalty.')
            case 'SGSV':
                print('__Driver__ has served a stop-and-go penalty.')
            case 'FLBK':
                print('Flashback initiated.')
            case 'BUTN':
                pass
            case _:
                pass

    def _filter_participants(self, packet: pk.ParticipantsPacket):
        if self.participants is not None:
            return
        self.participants = packet.participants
        self.numActiveCars = packet.numActiveCars.value

    def _filter_car_damage(self, packet: pk.CarDamagePacket):
        pass
