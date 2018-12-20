#!/usr/bin/env python
# encoding: utf-8
from app.handler import BaseHandler
from base.route import Route

route = Route()

@route(r"/")
class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")