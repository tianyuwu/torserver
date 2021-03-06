#!/usr/bin/env python
# encoding: utf-8
from marshmallow import fields, validate

from app.schema import BaseSchema


class UserLoginSchema(BaseSchema):
    email = fields.Str(required=True,
                          validate=validate.Regexp('^[1]\d{10}$|[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$'),
                          description='邮箱或者手机号')
    password = fields.Str(required=True,
                          validate=validate.Length(min=6, max=18),
                          description='用户的密码')

    # 自定义验证规则
    # @validates('location')
    # def validate_location(self, value):
    #     valid_locations = [u'SHANGHAI', u'TOKYO', u'NEWYORK']
    #     if value not in valid_locations:
    #         raise ValidationError('Unknown location.')