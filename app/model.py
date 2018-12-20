#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: whitney
@file: model.py
@time: 2018/12/19 4:12 PM
"""
class BaseModel(object):
    def __init__(self, db):
        self.db = db