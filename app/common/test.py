#!/usr/bin/env python
# encoding: utf-8
# coding:utf-8
import aiopg
import ujson

from tornado.escape import json_encode, json_decode
from tornado.ioloop import IOLoop

from tornado.testing import AsyncHTTPTestCase, unittest

from app.common.handler import route
from config import DSN
from server import Application


class CommonTest(AsyncHTTPTestCase):

    # async def get_app(self):
    #     async with aiopg.create_pool(DSN) as db:
    #         return Application(db, route.urls)
    def test_index(self):
        a = 3
        self.assertEqual(a, 3)

    # def test_hello(self):
    #     response = self.fetch("/hello", method="GET")
    #     self.assertEqual(response.code, 200)
    #
    # def test_job(self):
    #     response = self.fetch("/job", method="GET")
    #     self.assertEqual(response.code, 200)

if __name__ == '__main__':
    unittest.main()