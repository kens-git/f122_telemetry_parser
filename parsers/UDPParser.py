import logging
from queue import Queue
import socket
from threading import Thread
from typing import cast, Final, Optional
from filters.Filter import Filter
from utilities.parse import parse_packet


UDP_MAX_SIZE: Final[int] = 65507
"""Maximum UDP packet size, in bytes."""


class UDPParser:
    """Defines a class for parsing packet data and distributing it.

    Packet data is parsed then queued, where it's passed to the filter
    as quickly as the filter can process it.
    """

    def __init__(self, filter: Filter, port: int):
        """Initializes the UDPParser instance.

        Args:
            filter: That filter that will process the packets.
            port: The UDP port to listen for packets on.
        """

        self.port: int = port
        self.filter: Filter = filter
        self.socket: Optional[socket.socket] = None
        self.data_queue = Queue[bytes]()

    def is_running(self) -> bool:
        """Determines if the parser is actively listening for packets.

        Returns:
            True if the socket is still active.
        """

        return self.socket is not None

    def start(self):
        """Starts the parser.

        A UDP socket is opened and two daemon threads are created
        (in a producer/consumer patter) to ensure parsing and filtering
        do not block the main thread.
        """

        self.socket = socket.socket(family=socket.AF_INET,
                                    type=socket.SOCK_DGRAM)
        Thread(target=self._consumer, daemon=True).start()
        Thread(target=self._producer, daemon=True).start()

    def stop(self):
        """Stops the parser.

        The socket is shut down and any queued packets are deleted.
        """

        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_RDWR)
            # TODO: throws an OSError on Windows
            # socket.close()
            self.socket = None
            with self.data_queue.mutex:
                self.data_queue.queue.clear()

    def _consumer(self):
        while self.socket:
            self.filter.filter(parse_packet(self.data_queue.get()))

    def _producer(self):
        # TODO: accept host in constructor
        cast(socket.socket, self.socket).bind(('127.0.0.1', self.port))
        logging.info('UDPParser started successfully.')
        logging.info(f'Using filter: {type(self.filter).__name__}')
        logging.info(f'Listening on port {self.port}.\n')
        while self.socket:
            data = self.socket.recvfrom(UDP_MAX_SIZE)[0]
            self.data_queue.put(data)
