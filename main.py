from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import sys
import time
from typing import cast, Dict, Final, Tuple, Type
from filters.DebugFilter import DebugFilter
from filters.Filter import Filter
from filters.LogFilter import LogFilter
from filters.NullFilter import NullFilter
from filters.ReplayFilter import ReplayFilter
from parsers.UDPParser import UDPParser

DEFAULT_PORT: Final[int] = 20777

MAIN_THREAD_SLEEP_TIME_S: Final[float] = 0.016

logging.basicConfig(level=logging.INFO, format='%(message)s')

FILTERS: Dict[str, Tuple[str, Type[Filter]]] = {
    'debug': ('Logs packet ids to the console for debugging.', DebugFilter),
    'log': ('Logs basic session information to the console.', LogFilter),
    'null': ('Receives the parsed data but performs no action.',
             NullFilter),
    'replay': (
        'Writes sessions to a JSON file for use with a race replay UI.',
        ReplayFilter),
}
AVAILABLE_FILTERS_HELP_TEXT: str = ''.join([
    f'{item[0]}: {item[1][0]}\n' for item in FILTERS.items()])


def get_args():
    arg_parser = ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description='Command-line tool for parsing and filtering EA\'s F1 22 \
UDP telemetry.')
    arg_parser.add_argument(
        '-p', '--port', type=int,
        help=f'The UDP port to listen on. Defaults to {DEFAULT_PORT}.')
    arg_parser.add_argument(
        '-f', '--filter', type=str, required=True,
        help=f'''The filter applied to parsed data. Available filters:
\n\n{AVAILABLE_FILTERS_HELP_TEXT}''')
    return vars(arg_parser.parse_args())


if __name__ == '__main__':
    args = get_args()
    port = cast(int, args['port']) or DEFAULT_PORT
    try:
        filter: Filter = FILTERS[args['filter']][1]()
    except KeyError:
        logging.info(f'Unexpected filter given: {args["filter"]}')
        sys.exit(1)
    parser = UDPParser(filter, port)
    try:
        parser.start()
        while parser.is_running():
            time.sleep(MAIN_THREAD_SLEEP_TIME_S)
    except KeyboardInterrupt:
        parser.stop()
        filter.cleanup()
