import socket
import threading
import typing
import filters.Filter as fil
import utilities.parse as parse


class UDPParser:
    def __init__(self, filter: fil.Filter, port: int):
        self.port: int = port
        self.filter: fil.Filter = filter
        self.socket: typing.Optional[socket.socket] = None

    def is_running(self):
        return self.socket is not None

    def start(self):
        self.socket = socket.socket(family=socket.AF_INET,
                                    type=socket.SOCK_DGRAM)
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_RDWR)
            # TODO: throws an OSError on Windows
            # socket.close()
            self.socket = None

    def _run(self):
        self.socket.bind(('127.0.0.1', self.port))
        print('')
        print('UDPParser started successfully.')
        print(f'Using filter: {type(self.filter).__name__}')
        print(f'Listening on port {self.port}.')
        print('')
        while self.socket:
            data = self.socket.recvfrom(2**16)[0]
            self.filter.filter(parse.parse(data))
