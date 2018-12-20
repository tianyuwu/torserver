#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: whitney
@file: route.py
@time: 2018/12/19 11:37 AM
"""
from app.common.handler import route
from app.handler import DefaultHandler
from app.user.handler import user_route

handlers = []
handlers.extend(route.urls)
handlers.extend(user_route.urls)

# 缺省路由
handlers.append((r'.*', DefaultHandler))