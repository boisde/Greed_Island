#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Qian Lei'

import platform
from tools_lib.host_info import *

node = platform.node()

# 增加新平台，就在db_hosts字典中增加一个键值对，切勿修改已有的信息
db_hosts = {
    # LOCALHOST_NODE: {
    #   'host': LOCALHOST_IP,
    #   'user': 'root',
    #   'password': 'admindev',
    #   'port': 3306
    # },
    # 本地数据库暂时链接测试服务器
    LOCALHOST_NODE: {
        'host': TEST_BL_DB_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
    TEST_BL_SERVICE_NODE: {
        'host': TEST_BL_DB_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
    BL_SERVICE_NODE: {
        'host': BL_DB_IP,
        'user': 'fengbusiness',
        'password': 'bu3l%si6u&w9*bn',
        'port': 3306
    },
    LOCAL_SGY_NODE: {
        'host': TEST_BL_DB_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
}

db_hosts_slave = {
    # LOCALHOST_NODE: {
    #   'host': LOCALHOST_IP,
    #   'user': 'root',
    #   'password': 'admindev',
    #   'port': 3306
    # },
    # 本地数据库暂时链接测试服务器
    LOCALHOST_NODE: {
        'host': TEST_BL_DB_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
    TEST_BL_SERVICE_NODE: {
        'host': TEST_BL_DB_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
    BL_SERVICE_NODE: {
        'host': BL_DB_IP,
        'user': 'fengbusiness',
        'password': 'bu3l%si6u&w9*bn',
        'port': 3306
    },
    "online_outer": {
        'host': BL_DB_OUTER_IP,
        'user': 'fengdevelop',
        'password': 'dyj3h@6$n*bg8rd',
        'port': 3306
    },
}
db_hosts_slave[LOCAL_SGY_NODE] = db_hosts_slave[TEST_BL_SERVICE_NODE]

# 没有匹配就使用 localhost 配置
db_host = db_hosts.get(node, db_hosts['localhost'])
# 从数据库配置, 没有匹配就使用 localhost 配置
db_host_slave = db_hosts_slave.get(node, db_hosts_slave['localhost'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_shop',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_shop': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_shop',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_shop_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_shop',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
    'bl_news': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_news',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_news_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_news',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
    'bl_notice': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_notice',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_notice_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_notice',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
    'bl_invite': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_invite',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_invite_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_invite',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
    'bl_complaint': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_complaint',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_complaint_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_complaint',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
    'bl_charge': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_charge',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_charge_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_charge',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
    'bl_device': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_device',  # Or path to database file if using sqlite3.
        'USER': db_host['user'],  # Not used with sqlite3.
        'PASSWORD': db_host['password'],  # Not used with sqlite3.
        'HOST': db_host['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],  # Set to empty string for default. Not used with sqlite3.
    },
    'bl_device_slave': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bl_device',  # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],  # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],  # Not used with sqlite3.
        'HOST': db_host_slave['host'],  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],
    },
}

SHOP_DATABASES = {
    'default': DATABASES['bl_shop'],
    'bl_shop': DATABASES['bl_shop'],
    'bl_shop_slave': DATABASES['bl_shop_slave'],
}
NEWS_DATABASES = {
    'default': DATABASES['bl_news'],
    'bl_news': DATABASES['bl_news'],
    'bl_news_slave': DATABASES['bl_news_slave'],
}
NOTICE_DATABASES = {
    'default': DATABASES['bl_notice'],
    'bl_notice': DATABASES['bl_notice'],
    'bl_notice_slave': DATABASES['bl_notice_slave'],
}
INVITE_DATABASES = {
    'default': DATABASES['bl_invite'],
    'bl_invite': DATABASES['bl_invite'],
    'bl_invite_slave': DATABASES['bl_invite_slave'],
}
COMPLAINT_DATABASES = {
    'default': DATABASES['bl_complaint'],
    'bl_complaint': DATABASES['bl_complaint'],
    'bl_complaint_slave': DATABASES['bl_complaint_slave'],
}
CHARGE_DATABASES = {
    'default': DATABASES['bl_charge'],
    'bl_charge': DATABASES['bl_charge'],
    'bl_charge_slave': DATABASES['bl_charge_slave'],
}
DEVICE_DATABASES = {
    'default': DATABASES['bl_device'],
    'bl_device': DATABASES['bl_device'],
    'bl_device_slave': DATABASES['bl_device_slave'],
}


class AtomRouter(object):
    """Default Router for Atom services"""

    def db_for_read(self, model, **hints):
        if hasattr(model, '_db'):
            if model._db in (
                    'user_center', 'pay', 'F_DB_EVENT_PS_SUMMARY',
                    'F_DB_EVENT_SH_SUMMARY', 'auth_center', 'F_DB_USER_PS'
            ):
                return model._db
            return '%s_slave' % model._db
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        if hasattr(model, '_db'):
            return model._db
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # if hasattr(obj1, '_db') and hasattr(obj2, '_db') and  obj1._db == obj2._db:
        #     return True
        # else:
        #     return False
        return True

    def allow_syncdb(self, db, model):
        if hasattr(model, '_db'):
            model_db = model._db
        else:
            model_db = 'default'
        return db == model_db
