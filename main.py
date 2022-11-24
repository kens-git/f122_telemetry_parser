import argparse
import sys
import typing
import filters.DebugFilter as debug_fil
import filters.Filter as fil
import filters.LogFilter as log_fil
import filters.NullFilter as null_fil
import filters.ReplayFilter as replay_fil
import filters.SessionFilter as session_fil
import parsers.UDPParser as udp

DEFAULT_PORT: typing.Final[int] = 20777

FILTERS: typing.Dict[str, typing.Tuple[str, typing.Type[fil.Filter]]] = {
    'debug': ('Logs packet ids to the console for debugging.',
              debug_fil.DebugFilter),
    'log': ('Logs basic information to the console.', log_fil.LogFilter),
    'null': ('Receives the parsed data but performs no action.',
             null_fil.NullFilter),
    'session': (
        'Writes all data from sessions to a JSON file.',
        session_fil.SessionFilter),
    'replay': (
        'Writes sessions to a JSON file for use with a race replay UI.',
        replay_fil.ReplayFilter),
}
AVAILABLE_FILTERS_HELP_TEXT: str = ''.join([
    f'{item[0]}: {item[1][0]}\n' for item in FILTERS.items()])


def get_args():
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Command-line tool for parsing and filtering EA\'s F1 22 \
UDP telemetry.')
    # TODO: formatting of arguments:
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
    port = typing.cast(int, args['port']) or DEFAULT_PORT
    try:
        filter: fil.Filter = FILTERS[args['filter']][1]()
    except KeyError:
        print(f'Unexpected filter given: {args["filter"]}')
        sys.exit(1)
    parser = udp.UDPParser(filter, port)
    try:
        parser.start()
        while parser.is_running():
            pass
    except KeyboardInterrupt:
        parser.stop()
        # TODO: clean up filter
