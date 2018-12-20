#!/usr/bin/env python
# encoding: utf-8
from marshmallow import Schema


class BaseSchema(Schema):
    class Meta:
        strict = True