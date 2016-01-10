#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server, json, urllib, pathlib, asyncio
import local

class Handler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args, courses={}, **kargs):
        self.courses = courses
        super().__init__(*args, **kargs)
    
    def get_course(self, course, message, ins, outs):
        loop = asyncio.new_event_loop()
        coro = loop.create_connection(
            lambda: local.Client(message, loop, ins),
            sock=course)
        loop.run_until_complete(coro)
        #loop.run_forever()
        loop.close()
        size, res = int(outs.recv()), b''
        ins.send(b'1')
        while len(res) < size:
            res += outs.recv()
        return res
    
    def do_GET(self):
        path = pathlib.Path(self.path)
        # Expecting something like /course/exercise
        course = self.courses.get(path.parent)
        if course is not None:
            ex = path.name
            content = self.rfile.read()
            content = json.loads(content)
            message = [ex, message]
            message = json.dumps(message)
            with socket.socketpair() as ins, outs:
                res = self.get_course(course, message, ins, outs)
            self.wfile.write(res)
        else:
            super().do_GET()
