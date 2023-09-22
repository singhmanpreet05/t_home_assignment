#!/usr/bin/env python3


import socket
import selectors
import types
from src.app_handler import AppHandler
import logging
logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.app_handler = AppHandler()

    def __call__(self, host, port):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        logger.info(f"Listening on {(host, port)}")
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self._accept_wrapper(key.fileobj)
                    else:
                        self._service_connection(key, mask)
        except KeyboardInterrupt:
            logger.info("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

    # private

    def _accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        logger.info(f"Accepted connection from {addr}")
        conn.setblocking(False)

        # addr: is the address of the client
        # inb: is the input buffer to keep collecting input
        # outb: is the output buffer to send data to client
        # send_back: is to store the intent to send back data to client
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"",send_back=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)


    def _service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)

            # if client sent the data keep adding to the buffer till newline
            if recv_data:
                data.inb += recv_data
                if data.inb.endswith(b'\n'):
                    result = self.app_handler(data.inb[:-1])
                    data.outb = result
                    data.inb = data.inb[0:0]
                    data.send_back = b'1' # intent to send response to client

            # if the client or server wants to close connection then close it.
            if (not recv_data) or (data.send_back and not data.outb):
                logger.info(f"Closing connection to {data.addr}")
                self.sel.unregister(sock)
                sock.close()
                data.send_back = b''


        if mask & selectors.EVENT_WRITE:
            if data.send_back:
                logger.info(f"Echoing {data.outb!r} to {data.addr}")
                sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[0:0]
                data.send_back = b''
