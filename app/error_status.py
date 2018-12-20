#!/usr/bin/env python
# encoding: utf-8
#!/usr/bin/env python
# encoding: utf-8
"""
@version: ??
@author: whitney
@file: error_status.py
@time: 2018/11/28 4:55 PM
"""
class Msg:
    """
    错误消息对象
    """

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def json(self):
        return {'code': self.code, 'msg': self.msg}

NOT_ERROR = 100
# 通用错误
GENERAL_ERROR = {
    400: '非法请求',
    422: '参数错误',
    500: '服务器异常',
    404: '请求的资源不存在'
}

# 定义消息对象
PARAMETER_ERROR = Msg(422, '参数错误')
TOKEN_TIME_OUT = Msg(401, '会话超时')
AUTH_FAILED = Msg(403, '认证失败')
URL_ERROR = Msg(404, '请求地址不存在')
SERVICE_ERROR = Msg(500, '服务器内部错误')

# 用户相关
SXS_4001 = Msg(4001, '用户不存在')
SXS_4002 = Msg(4002, '账号格式错误')
SXS_4003 = Msg(4003, '密码错误')
USER_NOT_EXIST = Msg(4005, '账号不存在')