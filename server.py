#!/usr/bin/env python
# encoding: utf-8
import asyncio
import signal
import sys

import aiopg
import aredis
import os
from tornado import httpserver, web
from tornado.platform import asyncio as tornado_asyncio

import asyncpg
import uvloop

from tornado.options import options, define

from base.db import AsyncPG, AioPG
from base.log import log_request, init_log_system
from config import DB_NAME, DB_USER, DB_HOST, DB_PORT, DB_PASSWORD, STORE_OPTIONS

define("port", default=8888, help="run on the given port", type=int)

class Application(web.Application):
    def __init__(self, db_pool, debug=True):
        settings = dict(
            allow_remote_access=True,
            cookie_secret='6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC',
            debug=debug,
            log_function=log_request,  # 日志显示内容调整
            static_path=os.path.join(os.path.dirname(__file__), "app/admin/dist/static"),
        )
        from app.route import handlers
        super(Application, self).__init__(handlers, **settings)

        # Register other unit
        # self.db = AsyncPG(db_pool)
        self.db = AioPG(db_pool)
        # redis
        self.redis = aredis.StrictRedis(host=STORE_OPTIONS['redis_host'], port=STORE_OPTIONS['redis_port'],
                                   password=STORE_OPTIONS['redis_pass'], db=0)

async def init_db_pool():
    # return await asyncpg.create_pool(
    #     database=DB_NAME,
    #     user=DB_USER,
    #     host=DB_HOST,
    #     port=DB_PORT,
    #     password=DB_PASSWORD
    # )
    return await aiopg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def get_loop():
    # 设置uvloop为事件循环的loop,uvloop更加高效
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    tornado_asyncio.AsyncIOMainLoop().install()

    # 初始化数据库连接池
    return asyncio.get_event_loop()

class Server(object):
    def __init__(self):
        self.loop = get_loop()
        db_pool = self.loop.run_until_complete(init_db_pool())
        self.app = Application(db_pool)

        signal.signal(signal.SIGINT, self.stop)

    def start(self):
        options.parse_command_line()

        http_server = httpserver.HTTPServer(self.app, xheaders=True)
        http_server.listen(options.port)

        # 日志系统
        init_log_system()
        print('Server running in http://127.0.0.1:{}'.format(options.port))
        self.loop.run_forever()


    def stop(self, sig, frame):
        print('\nServer stop success!')
        self.loop.stop()
        sys.exit(0)


if __name__ == "__main__":
    server = Server()
    server.start()