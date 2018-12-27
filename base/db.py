#!/usr/bin/env python
# encoding: utf-8
import re

import tornado.util
import logging

logger = logging.getLogger(__name__)

class NoResultError(Exception):
    pass


class DB(object):
    def __init__(self, db, placeholder=None):
        self.db = db
        self.placeholder = placeholder

    async def execute(self, *args):
        """
        执行sql
        :param args:
        :return:
        """
        pass

    async def execute_find(self, *args):
        """执行查询单条记录的sql"""
        pass

    async def execute_select(self, *args):
        """执行查询多条记录的sql"""
        pass

    async def find(self, table, fields='*', condition=None, params=None):
        """查询单条"""
        where_str, _params = self.conditions(condition)
        if not params:
            params = _params
        select_str = "SELECT {0} FROM {1} ".format(fields, table)

        rs = await self.execute_find(select_str + where_str, *params)
        return rs

    async def select(self, table, fields='*', condition=None, order=None, offset=0,
                     limit=0, params=None):
        """查询多条"""
        where_str, _params = self.conditions(condition)
        if not params:
            params = _params

        order_str = self.order_str(order)
        limit_str = self.limit_str(offset, limit)

        select_str = "SELECT {0} FROM {1} {2} {3} {4}". \
            format(fields, table, where_str, order_str, limit_str)
        rs = await self.execute_select(select_str, *params)
        return rs

    async def count(self, table, condition=None, params=None):
        """统计条数"""
        where_str, _params = self.conditions(condition)
        if not params:
            params = _params
        count_str = "SELECT count(1) as num FROM {0} {1}".format(table, where_str)
        res = await self.execute_find(count_str, *params)
        if res:
            rv = res['num']
        else:
            rv = 0
        return rv

    async def execute_count(self, sql_str, *params):
        """
        通过sql统计条数
        :param sql_str:
        :return:
        """
        pattern = 'select ([\s\S]*) from'
        replace_str = "SELECT COUNT(*) as num FROM"
        count_sql = re.sub(pattern, replace_str, sql_str.lower())
        res = await self.execute_find(count_sql, *params)
        if res:
            rv = res['num']
        else:
            rv = 0
        return rv

    async def insert(self, table, data_dict, return_id=False):
        """
        插入数据
        :param table: 表名
        :param data_dict: 插入的数据
        :return: True or False
        """
        sql_str = "INSERT INTO {0}".format(table)
        insert_str, params = self.get_insert_str(data_dict)
        if not return_id:
            res = await self.execute(sql_str + insert_str, *params)
        else:
            res = await self.execute_find(sql_str + insert_str + " RETURNING id", *params)
            if not isinstance(res, bool):
                res = res['id']
        return res

    async def update(self, table, data_dict, condition, params=None):
        """
        更新数据
        :param table: 表名
        :param data_dict: 要更新的数据
        :param condition: 更新条件
        :param params: 传入的参数(list格式)，仅当字符串传入时候需要
        :return: True or False
        """
        update_str, _params = self.get_update_str(data_dict)
        condition_str, _params1 = self.conditions(condition)
        if not params:
            _params.extend(_params1)
            params = _params

        sql_str = "UPDATE {0} SET {1} {2}".format(table, update_str, condition_str)
        res = await self.execute(sql_str, *params)
        return res

    def print_sql(self, sql, args=()):
        sql = re.sub(r'%s', "'%s'", sql)
        out_sql = sql % tuple(args)

        return 'Execute SQL:\n{}'.format(out_sql)
        # return sql

    def conditions(self, condition):
        """
        查询条件，支持两种方式，字典和字符串，字符串需要用到单引号
        eg： "nick_name='Whitney'
                or
            {"nick_name":"Whitney"}
        :placeholder 占位符 %s or $n
        :return 返回sql片段和参数
        """
        condition_sql = ''
        params = ''
        if hasattr(condition, "items"):
            # mapping objects
            query = condition.items()
            l = []
            params = []
            # preserve old behavior
            if self.placeholder == '$n':
                for index, (k, v) in enumerate(query):
                    if v:
                        # 模糊搜索的支持
                        l.append("{0}=${1}".format(k, index + 1) \
                                 if k[0]!='~' else "{0} ~ {1}".format(k[1:], index+1))
                        params.append(v)
            else:
                for k, v in query:
                    if v:
                        # 模糊搜索支持
                        if v[0] in ['~','～']:
                            l.append("{0} ~ %s".format(k))
                            params.append(v[1:])
                        else:
                            l.append("{0}=%s".format(k))
                            params.append(v)

            if len(l):
                condition_sql = "where " + ' AND '.join(l)
            else:
                condition_sql = ''

        elif isinstance(condition, str):
            condition_sql = "WHERE " + condition

        return condition_sql, params

    def get_insert_str(self, data_dict):
        """
        组合插入的sql
        """
        sql_str = ''
        params = []
        if hasattr(data_dict, "items"):
            # mapping objects
            query = data_dict.items()
            fields = []
            values = []
            # preserve old behavior
            if self.placeholder == '$n':
                for index, (k, v) in enumerate(query):
                    fields.append(k)
                    values.append('${}'.format(index + 1))
                    params.append(v)
            else:
                for k, v in query:
                    fields.append(k)
                    values.append('%s')
                    params.append(v)

            fields_str = ','.join(fields)
            values_str = ",".join(values)
            sql_str = "({0}) VALUES ({1})".format(fields_str, values_str)

        elif isinstance(data_dict, str):
            sql_str = data_dict

        return sql_str, params

    def get_update_str(self, data_dict):
        if hasattr(data_dict, "items"):
            l = []
            args = []
            if self.placeholder == '$n':
                for index, (k, v) in enumerate(data_dict.items()):
                    l.append("{0}=${1}".format(k, index + 1))
                    args.append(v)
            else:
                for k, v in data_dict.items():
                    l.append("{0}=%s".format(k))
                    args.append(v)

            if len(l):
                sql_str = ",".join(l)
            else:
                sql_str = ''
            return sql_str, args

    def limit_str(self, offset, limit):
        """
        组合sql中的limit部分
        :param offset:
        :param limit:
        :return:
        """
        limit_str = ''
        if limit:
            limit_str = "OFFSET {} LIMIT {}".format(offset, limit)
        return limit_str

    def order_str(self, order_list):
        """
        组合sql中的排序部分
        :param order_list:
        :return:
        """
        if not order_list:
            return ''

        return ' ORDER BY ' + ','.join(
            map(lambda x: x[1:] + ' DESC' if x[0] == '-' else x + ' ASC', order_list))

class AioPG(DB):
    """
    aiopg库的sql抽象类
    """
    def __init__(self, db):
        super(AioPG, self).__init__(db)

    def row_to_obj(self, row, cur):
        """Convert a SQL row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc.name] = val
        return obj

    async def execute(self, stmt, *args):
        """Execute a SQL statement.

        Must be called with ``await self.execute(...)``
        """
        with (await self.db.cursor()) as cur:
            try:
                await cur.execute(stmt, args)
                rs = True
                logger.info(self.print_sql(stmt, args))
            except Exception as e:
                rs = False
                logger.error(self.print_sql(stmt, args) + '\nError: {}'.format(e))
            return rs



    async def execute_select(self, stmt, *args):
        """Query for a list of results.

        Typical usage::

            results = await self.execute_select(...)

        Or::

            for row in await self.execute_select(...)
        """
        with (await self.db.cursor()) as cur:
            try:
                await cur.execute(stmt, args)
                rs =  [self.row_to_obj(row, cur) for row in await cur.fetchall()]
                logger.info(self.print_sql(stmt, args) + '\n\nResult: rows returned {}'.format(len(rs)))
            except Exception as e:
                logger.error(self.print_sql(stmt, args) + '\nError: {}'.format(e))
                rs = None
            return rs

    async def execute_find(self, stmt, *args):
        """Query for exactly one result.

        Raises NoResultError if there are no results, or ValueError if
        there are more than one.
        """
        with (await self.db.cursor()) as cur:
            try:
                await cur.execute(stmt, args)
                rs =  await cur.fetchone()
                rs = self.row_to_obj(rs, cur)
                logger.info(self.print_sql(stmt, args) + '\n\nResult: rows returned {}'.format(1 if rs else 0))
            except Exception as e:
                logger.error(self.print_sql(stmt, args) + '\nError: {}'.format(e))
                rs = None
            return rs


class AsyncPG(DB):
    """
    asyncpg的sql抽象类
    """
    def __init__(self, db):
        super(AsyncPG, self).__init__(db, '$n')


    async def execute_select(self, sql, *args, size=None):
        async with self.db.acquire() as con:
            try:
                rs = [dict(row) for row in await con.fetch(sql, *args)]
                logger.info(self.print_sql(sql, args) + '\n\nResult: rows returned {}'.format(len(rs)))
            except Exception as e:
                logger.error(self.print_sql(sql, args) + '\n\nError: {}'.format(e.message))
                rs = None
            return rs

    async def execute_find(self, sql, *args):
        async with self.db.acquire() as con:
            try:
                rs = await con.fetchrow(sql, *args)
                logger.info(self.print_sql(sql, args) + '\nResult: rows returned {}'.format(1 if rs else 0))
            except Exception as e:
                rs = None
                logger.error(self.print_sql(sql, args) + '\nError: {}'.format(e.message))

            return dict(rs) if rs else rs

    async def execute(self, sql, *args, autocommit=True):
        logger.info(self.print_sql(sql, args))
        async with self.db.acquire() as con:
            rs = await con.execute(sql, *args)
            return rs

