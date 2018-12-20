#!/usr/bin/env python
# encoding: utf-8
import functools
from webargs.tornadoparser import parser

class Parser(object):
    def __call__(self, schema):
        def wrapper(func):
            @functools.wraps(func)
            def decorator(self):
                # 校验参数
                req_args = parser.parse(schema, self.request)
                # 参数个数在5个以内，直接解构
                if len(req_args) <= 5:
                    return func(self, **req_args)

                return func(self, req_args)
            return decorator

        return wrapper

use_args = Parser()