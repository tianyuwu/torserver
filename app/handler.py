#!/usr/bin/env python
# encoding: utf-8
import json

import datetime
import tornado.web
from tornado.log import app_log

from app.error_status import NOT_ERROR, GENERAL_ERROR, Msg


class ComplexEncoder(json.JSONEncoder):
    """处理json化时时间格式的问题"""

    def default(self, obj):
        if obj is None:
            return ''
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.identify = None

    @property
    def db(self):
        return self.application.db

    @property
    def log(self):
        return app_log

    @property
    def redis(self):
        return self.application.redis

    def get_current_user(self):
        return self.identify.get("uuid") if self.identify else None

    def write_json(self, error=NOT_ERROR, data=None):
        """返回json数据时用，默认正常时状态为100
        return
            data: 返回的数据
            msg: 错误信息
            code: 错误代码
        """
        chuck = None
        if error == NOT_ERROR:
            chuck = dict(
                code=NOT_ERROR,
                msg="success",
            )
            if data: chuck['data'] = data
        # 通用错误
        elif isinstance(error, int):
            msg = GENERAL_ERROR.get(error)
            chuck = dict(
                code=error,
                msg=msg
            )
            self.log.warning("Response has warning: {2}({1})".format(self.request.uri,
                                                                     error,
                                                                     data or msg
                                                                     ))
        elif isinstance(error, Msg):
            chuck = dict(
                code=error.code,
                msg=error.msg
            )
            self.log.warning("Response is error: {1}({2})".format(self.request.uri,
                                                                  error.code,
                                                                  data or error.msg
                                                                  ))

        jsonstr = json.dumps(chuck, cls=ComplexEncoder)
        self.finish(jsonstr)

    def write_error(self, status_code, **kwargs):
        """Write errors as JSON."""
        self.set_header("Content-Type", "application/json")
        if "exc_info" in kwargs:
            etype, value, traceback = kwargs["exc_info"]
            if hasattr(value, "messages"):
                self.write_json(422)
        else:
            self.write_json(status_code)

class DefaultHandler(BaseHandler):
    def get(self):
        self.write_error(404)

    def post(self):
        self.write_error(404)