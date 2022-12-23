from enum import Enum
from typing import Dict, Final


PACKET_HEADER_LENGTH: Final[int] = 24
"""The length of the packet header, in bytes."""

EVENT_PACKET_LENGTH: Final[int] = PACKET_HEADER_LENGTH + 16
"""The length of the event packet (including header), in bytes.

This length includes the 4 byte event code, and 12 bytes for the
event data union.
"""

PACKET_HEADER_ID_INDEX: Final[int] = 5
"""The byte index of the packet id."""

GRID_SIZE: Final[int] = 22
"""The number of grid positions."""

TIRE_COUNT: Final[int] = 4
"""Number of tires per car.

Because you never know...
"""

MAX_MARSHAL_ZONES: Final[int] = 21
"""Maximum number of marshal zones."""

MAX_WEATHER_SAMPLES: Final[int] = 56
"""Maximum number of weather samples for a session."""

MAX_TYRE_STINTS: Final[int] = 8
"""Maximum number of tire stints."""

MAX_LAP_HISTORIES: Final[int] = 100
"""Maximum number of lap histories for a session."""

NULL_BYTE_VALUE: Final[int] = 255
"""Value of null packet data for unsigned, single-byte types."""

NAME_SIZE: Final[int] = 48
"""Size of a driver name in the packets."""


class EventStringCode(Enum):
    """String codes used to identify an event."""

    SESSION_START = 'SSTA'
    SESSION_END = 'SEND'
    FASTEST_LAP = 'FTLP'
    RETIREMENT = 'RTMT'
    DRS_ENABLED = 'DRSE'
    DRS_DISABLED = 'DRSD'
    TEAM_MATE_IN_PITS = 'TMPT'
    CHEQUERED_FLAG = 'CHQF'
    RACE_WINNER = 'RCWN'
    PENALTY = 'PENA'
    SPEED_TRAP = 'SPTP'
    START_LIGHTS = 'STLG'
    LIGHTS_OUT = 'LGOT'
    DRIVE_THROUGH_SERVED = 'DTSV'
    STOP_GO_SERVED = 'SGSV'
    FLASHBACK = 'FLBK'
    BUTTON = 'BUTN'


class PacketId(Enum):
    """Integer ids of the packets."""

    MOTION = 0
    SESSION = 1
    LAP_DATA = 2
    EVENT = 3
    PARTICIPANTS = 4
    CAR_SETUPS = 5
    CAR_TELEMETRY = 6
    CAR_STATUS = 7
    FINAL_CLASSIFICATION = 8
    LOBBY_INFO = 9
    CAR_DAMAGE = 10
    SESSION_HISTORY = 11


class TeamId(Enum):
    """Integer ids for each team."""

    MERCEDES = 0
    FERRARI = 1
    RED_BULL_RACING = 2
    WILLIAMS = 3
    ASTON_MARTIN = 4
    ALPINE = 5
    ALPHA_TAURI = 6
    HAAS = 7
    MCLAREN = 8
    ALFA_ROMEO = 9
    MERCEDES_2020 = 85
    FERRARI_2020 = 86
    RED_BULL_2020 = 87
    WILLIAMS_2020 = 88
    RACING_POINT_2020 = 89
    RENAULT_2020 = 90
    ALPHA_TAURI_2020 = 91
    HAAS_2020 = 92
    MCLAREN_2020 = 93
    ALFA_ROMEO_2020 = 94
    ASTON_MARTIN_DB11_V12 = 95
    ASTON_MARTIN_VANTAGE_F1_EDITION = 96
    ASTON_MARTIN_VANTAGE_SAFETY_CAR = 97
    FERRARI_F8_TRIBUTO = 98
    FERRARI_ROMA = 99
    MCLAREN_720S = 100
    MCLAREN_ARTURA = 101
    MERCEDES_AMG_GT_BLACK_SERIES_SAFETY_CAR = 102
    MERCEDES_AMG_GTR_PRO = 103
    F1_CUSTOM_TEAM = 104
    PREMA_21 = 106
    UNI_VIRTUOSI_21 = 107
    CARLIN_21 = 108
    HITECH_21 = 109
    ART_GP_21 = 110
    MP_MOTORSPORT_21 = 111
    CHAROUZ_21 = 112
    DAMS_21 = 113
    CAMPOS_21 = 114
    BWT_21 = 115
    TRIDENT_21 = 116
    MERCEDES_AMG_GT_BLACK_SERIES = 117


class DriverId(Enum):
    """Integer ids for real-life drivers."""

    CARLOS_SAINZ = 0
    DANIIL_KVYAT = 1
    DANIEL_RICCIARDO = 2
    FERNANDO_ALONSO = 3
    FELIPE_MASSA = 4
    KIMI_RÄIKKÖNEN = 6
    LEWIS_HAMILTON = 7
    MAX_VERSTAPPEN = 9
    NICO_HULKENBURG = 10
    KEVIN_MAGNUSSEN = 11
    ROMAIN_GROSJEAN = 12
    SEBASTIAN_VETTEL = 13
    SERGIO_PEREZ = 14
    VALTTERI_BOTTAS = 15
    ESTEBAN_OCON = 17
    LANCE_STROLL = 19
    ARRON_BARNES = 20
    MARTIN_GILES = 21
    ALEX_MURRAY = 22
    LUCAS_ROTH = 23
    IGOR_CORREIA = 24
    SOPHIE_LEVASSEUR = 25
    JONAS_SCHIFFER = 26
    ALAIN_FOREST = 27
    JAY_LETOURNEAU = 28
    ESTO_SAARI = 29
    YASAR_ATIYEH = 30
    CALLISTO_CALABRESI = 31
    NAOTA_IZUM = 32
    HOWARD_CLARKE = 33
    WILHEIM_KAUFMANN = 34
    MARIE_LAURSEN = 35
    FLAVIO_NIEVES = 36
    PETER_BELOUSOV = 37
    KLIMEK_MICHALSKI = 38
    SANTIAGO_MORENO = 39
    BENJAMIN_COPPENS = 40
    NOAH_VISSER = 41
    GERT_WALDMULLER = 42
    JULIAN_QUESADA = 43
    DANIEL_JONES = 44
    ARTEM_MARKELOV = 45
    TADASUKE_MAKINO = 46
    SEAN_GELAEL = 47
    NYCK_DE_VRIES = 48
    JACK_AITKEN = 49
    GEORGE_RUSSELL = 50
    MAXIMILIAN_GÜNTHER = 51
    NIREI_FUKUZUMI = 52
    LUCA_GHIOTTO = 53
    LANDO_NORRIS = 54
    SÉRGIO_SETTE_CÂMARA = 55
    LOUIS_DELÉTRAZ = 56
    ANTONIO_FUOCO = 57
    CHARLES_LECLERC = 58
    PIERRE_GASLY = 59
    ALEXANDER_ALBON = 62
    NICHOLAS_LATIFI = 63
    DORIAN_BOCCOLACCI = 64
    NIKO_KARI = 65
    ROBERTO_MERHI = 66
    ARJUN_MAINI = 67
    ALESSIO_LORANDI = 68
    RUBEN_MEIJER = 69
    RASHID_NAIR = 70
    JACK_TREMBLAY = 71
    DEVON_BUTLER = 72
    LUKAS_WEBER = 73
    ANTONIO_GIOVINAZZI = 74
    ROBERT_KUBICA = 75
    ALAIN_PROST = 76
    AYRTON_SENNA = 77
    NOBUHARU_MATSUSHITA = 78
    NIKITA_MAZEPIN = 79
    GUANYA_ZHOU = 80
    MICK_SCHUMACHER = 81
    CALLUM_ILOTT = 82
    JUAN_MANUEL_CORREA = 83
    JORDAN_KING = 84
    MAHAVEER_RAGHUNATHAN = 85
    TATIANA_CALDERON = 86
    ANTHOINE_HUBERT = 87
    GUILIANO_ALESI = 88
    RALPH_BOSCHUNG = 89
    MICHAEL_SCHUMACHER = 90
    DAN_TICKTUM = 91
    MARCUS_ARMSTRONG = 92
    CHRISTIAN_LUNDGAARD = 93
    YUKI_TSUNODA = 94
    JEHAN_DARUVALA = 95
    GULHERME_SAMAIA = 96
    PEDRO_PIQUET = 97
    FELIPE_DRUGOVICH = 98
    ROBERT_SCHWARTZMAN = 99
    ROY_NISSANY = 100
    MARINO_SATO = 101
    AIDAN_JACKSON = 102
    CASPER_AKKERMAN = 103
    JENSON_BUTTON = 109
    DAVID_COULTHARD = 110
    NICO_ROSBERG = 111
    OSCAR_PIASTRI = 112
    LIAM_LAWSON = 113
    JURI_VIPS = 114
    THEO_POURCHAIRE = 115
    RICHARD_VERSCHOOR = 116
    LIRIM_ZENDELI = 117
    DAVID_BECKMANN = 118
    ALESSIO_DELEDDA = 121
    BENT_VISCAAL = 122
    ENZO_FITTIPALDI = 123
    MARK_WEBBER = 125
    JACQUES_VILLENEUVE = 126


DRIVER_NAMES: Dict[int, str] = {
    DriverId.CARLOS_SAINZ.value: 'Carlos Sainz',
    DriverId.DANIIL_KVYAT.value: 'Daniil Kvyat',
    DriverId.DANIEL_RICCIARDO.value: 'Daniel Ricciardo',
    DriverId.FERNANDO_ALONSO.value: 'Fernando Alonso',
    DriverId.FELIPE_MASSA.value: 'Felipe Massa',
    DriverId.KIMI_RÄIKKÖNEN.value: 'Kimi Räikkönen',
    DriverId.LEWIS_HAMILTON.value: 'Lewis Hamilton',
    DriverId.MAX_VERSTAPPEN.value: 'Max Verstappen',
    DriverId.NICO_HULKENBURG.value: 'Nico Hulkenburg',
    DriverId.KEVIN_MAGNUSSEN.value: 'Kevin Magnussen',
    DriverId.ROMAIN_GROSJEAN.value: 'Romain Grosjean',
    DriverId.SEBASTIAN_VETTEL.value: 'Sebastian Vettel',
    DriverId.SERGIO_PEREZ.value: 'Sergio Perez',
    DriverId.VALTTERI_BOTTAS.value: 'Valtteri Bottas',
    DriverId.ESTEBAN_OCON.value: 'Esteban Ocon',
    DriverId.LANCE_STROLL.value: 'Lance Stroll',
    DriverId.ARRON_BARNES.value: 'Arron Barnes',
    DriverId.MARTIN_GILES.value: 'Martin Giles',
    DriverId.ALEX_MURRAY.value: 'Alex Murray',
    DriverId.LUCAS_ROTH.value: 'Lucas Roth',
    DriverId.IGOR_CORREIA.value: 'Igor Correia',
    DriverId.SOPHIE_LEVASSEUR.value: 'Sophie Levasseur',
    DriverId.JONAS_SCHIFFER.value: 'Jonas Schiffer',
    DriverId.ALAIN_FOREST.value: 'Alain Forest',
    DriverId.JAY_LETOURNEAU.value: 'Jay Letourneau',
    DriverId.ESTO_SAARI.value: 'Esto Saari',
    DriverId.YASAR_ATIYEH.value: 'Yasar Atiyeh',
    DriverId.CALLISTO_CALABRESI.value: 'Callisto Calabresi',
    DriverId.NAOTA_IZUM.value: 'Naota Izum',
    DriverId.HOWARD_CLARKE.value: 'Howard Clarke',
    DriverId.WILHEIM_KAUFMANN.value: 'Wilheim Kaufmann',
    DriverId.MARIE_LAURSEN.value: 'Marie Laursen',
    DriverId.FLAVIO_NIEVES.value: 'Flavio Nieves',
    DriverId.PETER_BELOUSOV.value: 'Peter Belousov',
    DriverId.KLIMEK_MICHALSKI.value: 'Klimek Michalski',
    DriverId.SANTIAGO_MORENO.value: 'Santiago Moreno',
    DriverId.BENJAMIN_COPPENS.value: 'Benjamin Coppens',
    DriverId.NOAH_VISSER.value: 'Noah Visser',
    DriverId.GERT_WALDMULLER.value: 'Gert Waldmuller',
    DriverId.JULIAN_QUESADA.value: 'Julian Quesada',
    DriverId.DANIEL_JONES.value: 'Daniel Jones',
    DriverId.ARTEM_MARKELOV.value: 'Artem Markelov',
    DriverId.TADASUKE_MAKINO.value: 'Tadasuke Makino',
    DriverId.SEAN_GELAEL.value: 'Sean Gelael',
    DriverId.NYCK_DE_VRIES.value: 'Nyck De Vries',
    DriverId.JACK_AITKEN.value: 'Jack Aitken',
    DriverId.GEORGE_RUSSELL.value: 'George Russell',
    DriverId.MAXIMILIAN_GÜNTHER.value: 'Maximilian Günther',
    DriverId.NIREI_FUKUZUMI.value: 'Nirei Fukuzumi',
    DriverId.LUCA_GHIOTTO.value: 'Luca Ghiotto',
    DriverId.LANDO_NORRIS.value: 'Lando Norris',
    DriverId.SÉRGIO_SETTE_CÂMARA.value: 'Sérgio Sette Câmara',
    DriverId.LOUIS_DELÉTRAZ.value: 'Louis Delétraz',
    DriverId.ANTONIO_FUOCO.value: 'Antonio Fuoco',
    DriverId.CHARLES_LECLERC.value: 'Charles Leclerc',
    DriverId.PIERRE_GASLY.value: 'Pierre Gasly',
    DriverId.ALEXANDER_ALBON.value: 'Alexander Albon',
    DriverId.NICHOLAS_LATIFI.value: 'Nicholas Latifi',
    DriverId.DORIAN_BOCCOLACCI.value: 'Dorian Boccolacci',
    DriverId.NIKO_KARI.value: 'Niko Kari',
    DriverId.ROBERTO_MERHI.value: 'Roberto Merhi',
    DriverId.ARJUN_MAINI.value: 'Arjun Maini',
    DriverId.ALESSIO_LORANDI.value: 'Alessio Lorandi',
    DriverId.RUBEN_MEIJER.value: 'Ruben Meijer',
    DriverId.RASHID_NAIR.value: 'Rashid Nair',
    DriverId.JACK_TREMBLAY.value: 'Jack Tremblay',
    DriverId.DEVON_BUTLER.value: 'Devon Butler',
    DriverId.LUKAS_WEBER.value: 'Lukas Weber',
    DriverId.ANTONIO_GIOVINAZZI.value: 'Antonio Giovinazzi',
    DriverId.ROBERT_KUBICA.value: 'Robert Kubica',
    DriverId.ALAIN_PROST.value: 'Alain Prost',
    DriverId.AYRTON_SENNA.value: 'Ayrton Senna',
    DriverId.NOBUHARU_MATSUSHITA.value: 'Nobuharu Matsushita',
    DriverId.NIKITA_MAZEPIN.value: 'Nikita Mazepin',
    DriverId.GUANYA_ZHOU.value: 'Guanya Zhou',
    DriverId.MICK_SCHUMACHER.value: 'Mick Schumacher',
    DriverId.CALLUM_ILOTT.value: 'Callum Ilott',
    DriverId.JUAN_MANUEL_CORREA.value: 'Juan Manuel Correa',
    DriverId.JORDAN_KING.value: 'Jordan King',
    DriverId.MAHAVEER_RAGHUNATHAN.value: 'Mahaveer Raghunathan',
    DriverId.TATIANA_CALDERON.value: 'Tatiana Calderon',
    DriverId.ANTHOINE_HUBERT.value: 'Anthoine Hubert',
    DriverId.GUILIANO_ALESI.value: 'Guiliano Alesi',
    DriverId.RALPH_BOSCHUNG.value: 'Ralph Boschung',
    DriverId.MICHAEL_SCHUMACHER.value: 'Michael Schumacher',
    DriverId.DAN_TICKTUM.value: 'Dan Ticktum',
    DriverId.MARCUS_ARMSTRONG.value: 'Marcus Armstrong',
    DriverId.CHRISTIAN_LUNDGAARD.value: 'Christian Lundgaard',
    DriverId.YUKI_TSUNODA.value: 'Yuki Tsunoda',
    DriverId.JEHAN_DARUVALA.value: 'Jehan Daruvala',
    DriverId.GULHERME_SAMAIA.value: 'Gulherme Samaia',
    DriverId.PEDRO_PIQUET.value: 'Pedro Piquet',
    DriverId.FELIPE_DRUGOVICH.value: 'Felipe Drugovich',
    DriverId.ROBERT_SCHWARTZMAN.value: 'Robert Schwartzman',
    DriverId.ROY_NISSANY.value: 'Roy Nissany',
    DriverId.MARINO_SATO.value: 'Marino Sato',
    DriverId.AIDAN_JACKSON.value: 'Aidan Jackson',
    DriverId.CASPER_AKKERMAN.value: 'Casper Akkerman',
    DriverId.JENSON_BUTTON.value: 'Jenson Button',
    DriverId.DAVID_COULTHARD.value: 'David Coulthard',
    DriverId.NICO_ROSBERG.value: 'Nico Rosberg',
    DriverId.OSCAR_PIASTRI.value: 'Oscar Piastri',
    DriverId.LIAM_LAWSON.value: 'Liam Lawson',
    DriverId.JURI_VIPS.value: 'Juri Vips',
    DriverId.THEO_POURCHAIRE.value: 'Theo Pourchaire',
    DriverId.RICHARD_VERSCHOOR.value: 'Richard Verschoor',
    DriverId.LIRIM_ZENDELI.value: 'Lirim Zendeli',
    DriverId.DAVID_BECKMANN.value: 'David Beckmann',
    DriverId.ALESSIO_DELEDDA.value: 'Alessio Deledda',
    DriverId.BENT_VISCAAL.value: 'Bent Viscaal',
    DriverId.ENZO_FITTIPALDI.value: 'Enzo Fittipaldi',
    DriverId.MARK_WEBBER.value: 'Mark Webber',
    DriverId.JACQUES_VILLENEUVE.value: 'Jacques Villeneuve',
}
"""Associates a driver id with their full name."""


class TrackId(Enum):
    """Integer ids for in-game tracks."""

    MELBOURNE = 0
    PAUL_RICARD = 1
    SHANGHAI = 2
    SAKHIR_BAHRAIN = 3
    CATALUNYA = 4
    MONACO = 5
    MONTREAL = 6
    SILVERSTONE = 7
    HOCKENHEIM = 8
    HUNGARORING = 9
    SPA = 10
    MONZA = 11
    SINGAPORE = 12
    SUZUKA = 13
    ABU_DHABI = 14
    TEXAS = 15
    BRAZIL = 16
    AUSTRIA = 17
    SOCHI = 18
    MEXICO = 19
    BAKU_AZERBAIJAN = 20
    SAKHIR_SHORT = 21
    SILVERSTONE_SHORT = 22
    TEXAS_SHORT = 23
    SUZUKA_SHORT = 24
    HANOI = 25
    ZANDVOORT = 26
    IMOLA = 27
    PORTIMÃO = 28
    JEDDAH = 29
    MIAMI = 30


TRACK_NAMES: Dict[int, str] = {
    TrackId.MELBOURNE.value: 'Albert Park Circuit',
    TrackId.PAUL_RICARD.value: 'Circuit Paul Ricard',
    TrackId.SHANGHAI.value: 'Shanghai International Circuit',
    TrackId.SAKHIR_BAHRAIN.value: 'Bahrain International Circuit',
    TrackId.CATALUNYA.value: 'Circuit de Barcelona-Catalunya',
    TrackId.MONACO.value: 'Circuit de Monte Carlo',
    TrackId.MONTREAL.value: 'Circuit Gilles-Villeneuve',
    TrackId.SILVERSTONE.value: 'Silverstone Circuit',
    TrackId.HOCKENHEIM.value: 'Hockenheimring',
    TrackId.HUNGARORING.value: 'Hungaroring',
    TrackId.SPA.value: 'Circuit Spa-Francorchamps',
    TrackId.MONZA.value: 'Autodromo Nazionale Monza',
    TrackId.SINGAPORE.value: 'Marina Bay Circuit',
    TrackId.SUZUKA.value: 'Suzuka Circuit',
    TrackId.ABU_DHABI.value: 'Yas Marina Circuit',
    TrackId.TEXAS.value: 'Circuit of the Americas',
    TrackId.BRAZIL.value: 'Autódromo José Carlos Pace',
    TrackId.AUSTRIA.value: 'Red Bull Ring',
    TrackId.SOCHI.value: 'Sochi Autodrom',
    TrackId.MEXICO.value: 'Autódromo Hermanos Rodríguez',
    TrackId.BAKU_AZERBAIJAN.value: 'Baku City Circuit',
    TrackId.SAKHIR_SHORT.value: 'Sakhir Short',
    TrackId.SILVERSTONE_SHORT.value: 'Silverstone Short',
    TrackId.TEXAS_SHORT.value: 'Texas Short',
    TrackId.SUZUKA_SHORT.value: 'Suzuka Short',
    TrackId.HANOI.value: 'Hanoi Circuit',
    TrackId.ZANDVOORT.value: 'Circuit Zandvoort',
    TrackId.IMOLA.value: 'Autodromo Enzo e Dino Ferrari',
    TrackId.PORTIMÃO.value: 'Algarve International Circuit',
    TrackId.JEDDAH.value: 'Jeddah Corniche Circuit',
    TrackId.MIAMI.value: 'Miami International Autodrome',
}
"""Associates a track id with that track's full name."""


class NationalityId(Enum):
    """Integer id for nationalities."""

    AMERICAN = 1
    ARGENTINEAN = 2
    AUSTRALIAN = 3
    AUSTRIAN = 4
    AZERBAIJANI = 5
    BAHRAINI = 6
    BELGIAN = 7
    BOLIVIAN = 8
    BRAZILIAN = 9
    BRITISH = 10
    BULGARIAN = 11
    CAMEROONIAN = 12
    CANADIAN = 13
    CHILEAN = 14
    CHINESE = 15
    COLOMBIAN = 16
    COSTA_RICAN = 17
    CROATIAN = 18
    CYPRIOT = 19
    CZECH = 20
    DANISH = 21
    DUTCH = 22
    ECUADORIAN = 23
    ENGLISH = 24
    EMIRIAN = 25
    ESTONIAN = 26
    FINNISH = 27
    FRENCH = 28
    GERMAN = 29
    GHANAIAN = 30
    GREEK = 31
    GUATEMALAN = 32
    HONDURAN = 33
    HONG_KONGER = 34
    HUNGARIAN = 35
    ICELANDER = 36
    INDIAN = 37
    INDONESIAN = 38
    IRISH = 39
    ISRAELI = 40
    ITALIAN = 41
    JAMAICAN = 42
    JAPANESE = 43
    JORDANIAN = 44
    KUWAITI = 45
    LATVIAN = 46
    LEBANESE = 47
    LITHUANIAN = 48
    LUXEMBOURGER = 49
    MALAYSIAN = 50
    MALTESE = 51
    MEXICAN = 52
    MONEGASQUE = 53
    NEW_ZEALANDER = 54
    NICARAGUAN = 55
    NORTHERN_IRISH = 56
    NORWEGIAN = 57
    OMANI = 58
    PAKISTANI = 59
    PANAMANIAN = 60
    PARAGUAYAN = 61
    PERUVIAN = 62
    POLISH = 63
    PORTUGUESE = 64
    QATARI = 65
    ROMANIAN = 66
    RUSSIAN = 67
    SALVADORAN = 68
    SAUDI = 69
    SCOTTISH = 70
    SERBIAN = 71
    SINGAPOREAN = 72
    SLOVAKIAN = 73
    SLOVENIAN = 74
    SOUTH_KOREAN = 75
    SOUTH_AFRICAN = 76
    SPANISH = 77
    SWEDISH = 78
    SWISS = 79
    THAI = 80
    TURKISH = 81
    URUGUAYAN = 82
    UKRAINIAN = 83
    VENEZUELAN = 84
    BARBADIAN = 85
    WELSH = 86
    VIETNAMESE = 87


class GameModeId(Enum):
    """Integer ids for game modes."""

    EVENT_MODE = 0
    GRAND_PRIX = 3
    TIME_TRIAL = 5
    SPLITSCREEN = 6
    ONLINE_CUSTOM = 7
    ONLINE_LEAGUE = 8
    CAREER_INVITATIONAL = 11
    CHAMPIONSHIP_INVITATIONAL = 12
    CHAMPIONSHIP = 13
    ONLINE_CHAMPIONSHIP = 14
    ONLINE_WEEKLY_EVENT = 15
    CAREER_22 = 19
    CAREER_22_ONLINE = 20
    BENCHMARK = 127


class RulesetId(Enum):
    """Integer ids for each ruleset."""

    PRACTICE_AND_QUALIFYING = 0
    RACE = 1
    TIME_TRIAL = 2
    TIME_ATTACK = 4
    CHECKPOINT_CHALLENGE = 6
    AUTOCROSS = 8
    DRIFT = 9
    AVERAGE_SPEED_ZONE = 10
    RIVAL_DUEL = 11


class Surface(Enum):
    """Integer ids for surface types on and around the track."""

    TARMAC = 0
    RUMBLE_STRIP = 1
    CONCRETE = 2
    ROCK = 3
    GRAVEL = 4
    MUD = 5
    SAND = 6
    GRASS = 7
    WATER = 8
    COBBLESTONE = 9
    METAL = 10
    RIDGED = 11


class ButtonFlag(Enum):
    """Bit flags associated with a button on the controller."""

    CROSS_OR_A = 0x00000001
    TRIANGLE_OR_Y = 0x00000002
    CIRCLE_OR_B = 0x00000004
    SQUARE_OR_X = 0x00000008
    D_PAD_LEFT = 0x00000010
    D_PAD_RIGHT = 0x00000020
    D_PAD_UP = 0x00000040
    D_PAD_DOWN = 0x00000080
    OPTIONS_OR_MENU = 0x00000100
    L1_OR_LB = 0x00000200
    R1_OR_RB = 0x00000400
    L2_OR_LT = 0x00000800
    R2_OR_RT = 0x00001000
    LEFT_STICK_CLICK = 0x00002000
    RIGHT_STICK_CLICK = 0x00004000
    RIGHT_STICK_LEFT = 0x00008000
    RIGHT_STICK_RIGHT = 0x00010000
    RIGHT_STICK_UP = 0x00020000
    RIGHT_STICK_DOWN = 0x00040000
    SPECIAL = 0x00080000
    UDP_ACTION_1 = 0x00100000
    UDP_ACTION_2 = 0x00200000
    UDP_ACTION_3 = 0x00400000
    UDP_ACTION_4 = 0x00800000
    UDP_ACTION_5 = 0x01000000
    UDP_ACTION_6 = 0x02000000
    UDP_ACTION_7 = 0x04000000
    UDP_ACTION_8 = 0x08000000
    UDP_ACTION_9 = 0x10000000
    UDP_ACTION_10 = 0x20000000
    UDP_ACTION_11 = 0x40000000
    UDP_ACTION_12 = 0x80000000


class PenaltyId(Enum):
    """Integer ids for penalties."""

    DRIVE_THROUGH = 0
    STOP_GO = 1
    GRID_PENALTY = 2
    PENALTY_REMINDER = 3
    TIME_PENALTY = 4
    WARNING = 5
    DISQUALIFIED = 6
    REMOVED_FROM_FORMATION_LAP = 7
    PARKED_TOO_LONG_TIMER = 8
    TYRE_REGULATIONS = 9
    THIS_LAP_INVALIDATED = 10
    THIS_AND_NEXT_LAP_INVALIDATED = 11
    THIS_LAP_INVALIDATED_WITHOUT_REASON = 12
    LAP_INVALIDATED_WITHOUT_REASON = 13
    THIS_AND_PREVIOUS_LAP_INVALIDATED = 14
    THIS_AND_PREVIOUS_LAP_INVALIDATED_WITHOUT_REASON = 15
    RETIRED = 16
    BLACK_FLAG_TIMER = 17


class InfringementId(Enum):
    """Integer ids for infringements."""

    BLOCKING_BY_SLOW_DRIVING = 0
    BLOCKING_BY_WRONG_WAY_DRIVING = 1
    REVERSING_OFF_THE_START_LINE = 2
    BIG_COLLISION = 3
    SMALL_COLLISION = 4
    COLLISION_FAILED_TO_HAND_BACK_POSITION_SINGLE = 5
    COLLISION_FAILED_TO_HAND_BACK_POSITION_MULTIPLE = 6
    CORNER_CUTTING_GAINED_TIME = 7
    CORNER_CUTTING_OVERTAKE_SINGLE = 8
    CORNER_CUTTING_OVERTAKE_MULTIPLE = 9
    CROSSED_PIT_EXIT_LANE = 10
    IGNORING_BLUE_FLAGS = 11
    IGNORING_YELLOW_FLAGS = 12
    IGNORING_DRIVE_THROUGH = 13
    TOO_MANY_DRIVE_THROUGHS = 14
    DRIVE_THROUGH_REMINDER_SERVE_WITHIN_N_LAPS = 15
    DRIVE_THROUGH_REMINDER_SERVE_THIS_LAP = 16
    PIT_LANE_SPEEDING = 17
    PARKED_FOR_TOO_LONG = 18
    IGNORING_TYRE_REGULATIONS = 19
    TOO_MANY_PENALTIES = 20
    MULTIPLE_WARNINGS = 21
    APPROACHING_DISQUALIFICATION = 22
    TYRE_REGULATIONS_SELECT_SINGLE = 23
    TYRE_REGULATIONS_SELECT_MULTIPLE = 24
    LAP_INVALIDATED_CORNER_CUTTING = 25
    LAP_INVALIDATED_RUNNING_WIDE = 26
    CORNER_CUTTING_RAN_WIDE_GAINED_TIME_MINOR = 27
    CORNER_CUTTING_RAN_WIDE_GAINED_TIME_SIGNIFICANT = 28
    CORNER_CUTTING_RAN_WIDE_GAINED_TIME_EXTREME = 29
    LAP_INVALIDATED_WALL_RIDING = 30
    LAP_INVALIDATED_FLASHBACK_USED = 31
    LAP_INVALIDATED_RESET_TO_TRACK = 32
    BLOCKING_THE_PITLANE = 33
    JUMP_START = 34
    SAFETY_CAR_TO_CAR_COLLISION = 35
    SAFETY_CAR_ILLEGAL_OVERTAKE = 36
    SAFETY_CAR_EXCEEDING_ALLOWED_PACE = 37
    VIRTUAL_SAFETY_CAR_EXCEEDING_ALLOWED_PACE = 38
    FORMATION_LAP_BELOW_ALLOWED_SPEED = 39
    FORMATION_LAP_PARKING = 40
    RETIRED_MECHANICAL_FAILURE = 41
    RETIRED_TERMINALLY_DAMAGED = 42
    SAFETY_CAR_FALLING_TOO_FAR_BACK = 43
    BLACK_FLAG_TIMER = 44
    UNSERVED_STOP_GO_PENALTY = 45
    UNSERVED_DRIVE_THROUGH_PENALTY = 46
    ENGINE_COMPONENT_CHANGE = 47
    GEARBOX_CHANGE = 48
    PARC_FERMÉ_CHANGE = 49
    LEAGUE_GRID_PENALTY = 50
    RETRY_PENALTY = 51
    ILLEGAL_TIME_GAIN = 52
    MANDATORY_PITSTOP = 53
    ATTRIBUTE_ASSIGNED = 54


class SessionId(Enum):
    """Integer ids for session types."""

    UNKNOWN = 0
    P1 = 1
    P2 = 2
    P3 = 3
    SHORT_P = 4
    Q1 = 5
    Q2 = 6
    Q3 = 7
    SHORT_Q = 8
    OSQ = 9
    R = 10
    R2 = 11
    R3 = 12
    TIME_TRIAL = 13


SESSION_TEXT: Dict[int, str] = {
    SessionId.UNKNOWN.value: 'Unknown',
    SessionId.P1.value: 'Practice 1',
    SessionId.P2.value: 'Practice 2',
    SessionId.P3.value: 'Practice 3',
    SessionId.SHORT_P.value: 'Short Practice',
    SessionId.Q1.value: 'Qualifying 1',
    SessionId.Q2.value: 'Qualifying 2',
    SessionId.Q3.value: 'Qualifying 3',
    SessionId.SHORT_Q.value: 'Short Qualifying',
    SessionId.OSQ.value: 'One-shot Qualifying',
    SessionId.R.value: 'Race',
    SessionId.R2.value: 'Race 2',
    SessionId.R3.value: 'Race 3',
    SessionId.TIME_TRIAL.value: 'Time Trial',
}
"""Associates a session id with its display text."""


class WeatherId(Enum):
    """Integer ids for weather."""

    CLEAR = 0
    LIGHT_CLOUD = 1
    OVERCAST = 2
    LIGHT_RAIN = 3
    HEAVY_RAIN = 4
    STORM = 5


WEATHER_TEXT: Dict[int, str] = {
    WeatherId.CLEAR.value: 'Clear',
    WeatherId.LIGHT_CLOUD.value: 'Light Cloud',
    WeatherId.OVERCAST.value: 'Overcast',
    WeatherId.LIGHT_RAIN.value: 'Light Rain',
    WeatherId.HEAVY_RAIN.value: 'Heavy Rain',
    WeatherId.STORM.value: 'Storm',
}
"""Associates a weather id with its display text."""
