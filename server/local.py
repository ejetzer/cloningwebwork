#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, multiprocessing, json, socket

class CourseServer(asyncio.Protocol):
    
    def __init__(self, loop, exercises):
        'CourseServer(exercises={name: socket})'
        self.loop = loop
        self.exercises = exercises
    
    def connection_made(self, transport):
        self.transport = transport
    
    def parse(self, message):
        exercise, message = json.loads(message)
        exercise = self.exercises[exercise]
        return exercise, message
    
    def get_exercise(self, exercise, message, ins, outs):
        loop = asyncio.new_event_loop()
        coro = loop.create_connection(
            lambda: Client(message, loop, ins),
            sock=exercise)
        loop.run_until_complete(coro)
        #loop.run_forever()
        loop.close()
        size, res = int(outs.recv()), b''
        ins.send(b'1')
        while len(res) < size:
            res += outs.recv()
        return res
    
    def data_received(self, data):
        message = data.decode()
        exercise, command = self.parse(message)
        with socket.socketpair() as ins, outs:
            res = self.get_exercise(exercise, command, ins, outs)
        self.transport.write(res)

class ExerciseServer(asyncio.Protocol):
    
    def __init__(self, exercise):
        self.exercise = exercise
    
    def connection_made(self, transport):
        self.transport = transport
    
    def data_received(self, data):
        message = data.decode()
        message = json.loads(message)
        res = self.exercise(**message)
        res = json.dumps(res)
        self.transport.write(res.encode())

class Client(asyncio.Protocol):
    
    def __init__(self, message, loop, sock):
        self.message = message
        self.loop = loop
        self.sock = sock
    
    def connection_made(self, transport):
        transport.write(self.message.encode())
    
    def data_received(self, data):
        self.sock.send(bytes(len(data)))
        self.sock.recv()
        self.sock.sendall(data)
    
    def connection_lost(self, exc):
        self.loop.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Make exercises
    exs = {}
    # Make course
    coro = loop.create_server(lambda: CourseServer(loop, exs),
                              '127.0.0.1', 8888)
    # Launch!
    print('Launch.')
    try:
        server = loop.run_until_complete(coro)
        print('Serving on', server.sockets[0].getsockname())
        loop.run_forever()
    except KeyboardInterrupt:
        print('^C: Exit.')
    loop.close()
    print('Done.')
