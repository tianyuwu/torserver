#!/usr/bin/env python
# encoding: utf-8
"""
使用：
1. application类中setting方法传入log_request配置
2. application类中创建单例
    self.log = MgLog(config.MONGO_HOST).logger
3. handler基类中创建一个方法
    BaseHandler():
        @property
        def log(self):
            return self.application.log
4. 业务中需要写日志的地方调用，self.log.info方法即可写入日志
"""
import logging
# from logging.handlers import SMTPHandler
# from log4mongo.handlers import MongoHandler
import os

import time
from logging.handlers import RotatingFileHandler

from tornado.escape import to_basestring
from tornado.web import access_log
import tornado.log


class LogFormatter(tornado.log.LogFormatter):
    """修改tornado默认输出日志格式"""

    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


levels = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
          }

def init_log_system(log_level='debug', send_mail=False, mail_list=[]):
    print('Init Log System...')
    if not os.path.exists('log'):
        os.mkdir('log')

    log_name = "log_{}".format(int(time.time()))
    filename = 'log/%s.log' % log_name
    fh = RotatingFileHandler(filename, maxBytes=1024 * 1024 * 50, backupCount=50)
    fh.setLevel(levels.get('warning'))

    logging.root.addHandler(fh)
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    # 发送错误日志邮件
    # if send_mail:
    #     mail_handler = SMTPHandler('smtp.qq.com', 'xxx@qq.com', mail_list, 'Server Error',
    #                            ('xxx@qq.com', 'xxx'), ())
    #     mail_handler.setLevel(logging.ERROR)
    #     logging.root.addHandler(mail_handler)


def log_request(handler):
    """修改tornado日志消息格式"""
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error
    request_time = 1000.0 * handler.request.request_time()
    # 屏蔽掉静态文件输出
    if ('/static' not in handler.request.uri) or handler.get_status() > 304:
        log_method("""%d %s %s %.2fms 
%s""", handler.get_status(), handler._request_summary(),handler.current_user, request_time,
                   to_basestring(handler.request.body))