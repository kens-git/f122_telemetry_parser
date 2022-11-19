import socket
import typing
import packets.packets as pk
import utilities.parse as parse


class UDPParser:
    def __init__(self,
                 callback: typing.Callable[[pk.Packet], None], port: int):
        self.port: int = port
        self.callback: typing.Callable[[pk.Packet], None] = callback
        self.socket: typing.Optional[socket.socket] = None

    def start(self):
        self.socket = socket.socket(family=socket.AF_INET,
                                    type=socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', self.port))
        self.is_running = True
        # TODO: create thread to run socket in, and potentially the filter
        while self.socket is not None:
            data = self.socket.recvfrom(2**16)[0]
            self.callback(parse.parse(data))

    def stop(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
