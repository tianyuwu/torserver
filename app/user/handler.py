#!/usr/bin/env python
# encoding: utf-8
from app.handler import BaseHandler
from app.user.model import UsersModel
from app.user.schema import UserLoginSchema
from base.argparser import use_args
from base.route import Route

user_route = Route()

@user_route(r"/user/login")
class LoginHandler(BaseHandler):

    async def get(self):
        # 模型类查询
        # data = await UsersModel(self.db).list_all()
        # 直接查询
        data = await self.db.find('users')
        self.write_json(data=data)

    @use_args(UserLoginSchema)
    def post(self, username, password, remember):
        """
        用户登录
        :param username:
        :param password:
        :param remember:
        :return:
        """
        self.write("Hello, {}".format(username))