#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: whitney
@file: route.py
@time: 2018/12/19 11:37 AM
"""
# from app.admin.handler import admin_route
from app.handler import route

handlers = []
# handlers.extend(admin_route.urls)

# 缺省路由
handlers.extend(route.urls)