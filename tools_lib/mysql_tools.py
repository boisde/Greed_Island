# -*- coding:utf-8 -*-
# 提供一些适用于mysql数据库的工具函数

import MySQLdb
import platform
from tools_lib.host_info import *
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB

DEBUG = True

# mysql 辅助函数
def dictfetchall(cursor):
    """
    Returns all rows from a cursor as a dict
    :param cursor:
    :return:
    """
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def get_conn_from_old_db():
    """
    连接原master主库
    @return:
    """
    return Mysql()

def get_conn_from_db():
    """
    获取当前主库的连接
    """
    __DB_Settings = {
        TEST_CORE_API_NODE: {
            "host": TEST_CORE_DB_IP,
            "port": 3306,
            "user": "fengdev",
            "passwd": "qaz123",
            "charset": "utf8",    
        },
        ONLINE_AL_171_NODE: {
            'host': ONLINE_AL_CORE_DB_INNER_IP,
            'user': 'fengservice',
            'passwd': 'sk#u6j%n2x&w9ia',
            'port': 3306,
            "charset": "utf8",
        },
        LOCAL_SGY_NODE: {
            "host": TEST_CORE_DB_IP,
            "port": 3306,
            "user": "fengdev",
            "passwd": "qaz123",
            "charset": "utf8",
        },
        # 只读账户连接线上主库
        LOCAL_NOBODY_NODE: {
            "host": ONLINE_AL_CORE_DB_OUTER_IP,
            "port": 3306,
            "user": "fengdevelop",
            "passwd": "dk@s3h%y7tr#c0z",
            "charset": "utf8",
        },
    }
    __DB_Settings[LOCALHOST_NODE] = __DB_Settings[TEST_CORE_API_NODE]
    __DB_Settings[LOCAL_SGY_NODE] = __DB_Settings[LOCAL_NOBODY_NODE]
    node = platform.node()
    if node not in __DB_Settings.keys():
        node = LOCALHOST_NODE
    return Mysql(db_setting=__DB_Settings[node])


class Mysql(object):
    """
    获取连接对象
    conn = Mysql.getConn()
    释放连接对象
    conn.close()
    """
    DB_Settings = {
        TEST_CORE_API_NODE: {
            "host": "10.0.0.212",
            "port": 3306,
            "user": "fengdev",
            "passwd": "qaz123",
            "charset": "utf8",
        },
        ONLINE_AL_171_NODE: {
            "host": "10.171.133.162",
            "port": 3306,
            "user": "fengservice",
            "passwd": "sk#u6j%n2x&w9ia",
            "charset": "utf8",
        },
        LOCALHOST_NODE: {
            "host": "10.0.0.212",
            "port": 3306,
            "user": "fengdev",
            "passwd": "qaz123",
            "charset": "utf8",
        },
        # 只读账户连接线上主库
        LOCAL_NOBODY_NODE: {
            "host": "182.92.158.10",
            "port": 3306,
            "user": "fengdevelop",
            "passwd": "dk@s3h%y7tr#c0z",
            "charset": "utf8",
        },
    }
    DB_Settings[LOCAL_SGY_NODE] = DB_Settings[LOCALHOST_NODE]

    __pool = {}

    def __init__(self, db_setting=None):
        self._conn = self.__get_conn(db_setting)
        self._cursor = self._conn.cursor()

    @classmethod
    def get_db_settings(cls):
        node = platform.node()
        if node not in cls.DB_Settings.keys():
            node = LOCALHOST_NODE
        return cls.DB_Settings[node]

    @classmethod
    def __get_conn(cls, db_setting=None):
        """
        从连接池中获取连接
        @return:
        """
        if db_setting is None:
            db_setting = cls.get_db_settings()
        if cls.__pool.get(db_setting['host']) is None:
            cls.__pool[db_setting['host']] = PooledDB(
                creator=MySQLdb,
                mincached=1,
                maxcached=20,
                cursorclass=DictCursor,
                **db_setting
            )
        return cls.__pool[db_setting['host']].connection()

    def get_all(self, sql, param=None):
        if DEBUG:
            print sql
            print param

        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = []
        return result

    def get_one(self, sql, param=None, value_only=True):
        if DEBUG:
            print sql
            print param
        if param is None:
            self._cursor.execute(sql)
        else:
            self._cursor.execute(sql, param)
        rst = self._cursor.fetchone()
        if value_only:
            rst = rst.values()
            rst = rst[0] if len(rst) > 0 else None
        return rst

    def execute(self, sql, param=None):
        if DEBUG:
            print sql
            print param
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def end(self, option='commit'):
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def close(self, is_end=True):
        """
        释放连接池
        @param is_end:
        @return:
        """
        if is_end:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()


class Conn2Mysql(object):
    def __init__(self, old=False):
        """
        获取mysql连接
        @param old: 是否连接到原主库
        @return:

        Usage:

            with Conn2Mysql() as cn:
                some code ....

        """
        self.cn = get_conn_from_old_db() if old else get_conn_from_db()

    def __enter__(self):
        return self.cn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cn.close(is_end=(exc_type is None))
