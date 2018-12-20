#!/usr/bin/env python
# encoding: utf-8

# 数据库配置
DB_HOST = 'postgre'
DB_PORT = 3433
DB_NAME = 'postgre'
DB_USER = 'postgre'
DB_PASSWORD = 'postgre`s password'

# redis配置
STORE_OPTIONS = {
    'redis_host': 'redis',
    'redis_port': 1200,
    'redis_pass': 'redis`s password',
}


try:
    from local_settings import *
except ImportError:
    pass