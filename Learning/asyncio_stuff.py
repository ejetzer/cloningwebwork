#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

# This program needs a server to be running at localhost:8888
# Taken from:
# https://docs.python.org/3/library/asyncio-protocol.html#tcp-echo-client-protocol

class TestProtocol(asyncio.Protocol):

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        # Send a message to the server
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def connection_lost(self, exc):
        print('The server closed the connection.')
        print('Stop the event loop.')
        self.loop.stop()

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    message = 'Hello world!'
    coro = loop.create_connection(lambda: TestProtocol(message, loop),
                                  'localhost', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
