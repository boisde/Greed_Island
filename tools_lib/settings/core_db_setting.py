#!/usr/bin/env python
# coding:utf-8

import platform
from tools_lib.host_info import *

node = platform.node()

# 增加新平台，就在db_hosts字典中增加一个键值对，切勿修改已有的信息
db_hosts = {
    LOCALHOST_NODE: {
        'host': LOCALHOST_IP,
        'user': 'root',
        'password': '',
        'port': 3306
    },
    TEST_CORE_API_NODE: {
        'host': TEST_DEV_APP_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
    ONLINE_AL_171_NODE: {
        'host': ONLINE_AL_CORE_DB_INNER_IP,
        'user': 'fengservice',
        'password': 'sk#u6j%n2x&w9ia',
        'port': 3306
    },
    # LOCAL_SGY_NODE: {
    #     'host': ONLINE_AL_CORE_DB_OUTER_IP,
    #     'user': 'fengdevelop',
    #     'password': 'dk@s3h%y7tr#c0z',
    #     'port': 3306
    # },
    LOCAL_SGY_NODE: {
        'host': TEST_DEV_APP_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
}

db_hosts_slave = {
    LOCALHOST_NODE: {
        'host': LOCALHOST_IP,
        'user': 'root',
        'password': '',
        'port': 3306
    },
    TEST_CORE_API_NODE: {
        'host': TEST_DEV_APP_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
    ONLINE_AL_171_NODE: {
        'host': ONLINE_AL_CORE_DB_INNER_IP,
        'user': 'fengservice',
        'password': 'sk#u6j%n2x&w9ia',
        'port': 3306
    },
    # LOCAL_SGY_NODE: {
    #     'host': ONLINE_AL_CORE_DB_OUTER_IP,
    #     'user': 'fengdevelop',
    #     'password': 'dk@s3h%y7tr#c0z',
    #     'port': 3306
    # },
    LOCAL_SGY_NODE: {
        'host': TEST_DEV_APP_IP,
        'user': 'fengdev',
        'password': 'qaz123',
        'port': 3306
    },
}
# 没有匹配就使用 localhost 配置
db_host = db_hosts.get(node, db_hosts[TEST_CORE_API_NODE])
# 从数据库配置, 没有匹配就使用 localhost 配置
db_host_slave = db_hosts_slave.get(node, db_hosts_slave[TEST_CORE_API_NODE])


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gez_cmd_auth',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'pay': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pay',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'pay_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pay',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'f_shop': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'f_shop',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'f_shop_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'f_shop',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'f_account': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'f_account',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'f_account_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'f_account',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'cloud_order': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cloud_order',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'cloud_order_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cloud_order',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_SH': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_SH',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_SH_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_SH',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_SH_SUMMARY': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_SH_SUMMARY',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_SH_SUMMARY_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_SH_SUMMARY',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },

    'F_DB_EVENT_PS': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_PS',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_PS_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_PS',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_PS_SUMMARY': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_PS_SUMMARY',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_EVENT_PS_SUMMARY_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_EVENT_PS_SUMMARY',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_USER_PS': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_USER_PS',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_USER_PS_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_USER_PS',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },

    'F_DB_USER_SH': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_USER_SH',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_USER_SH_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_USER_SH',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },

    'F_DB_REPORT_PS': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_REPORT_PS',                      # Or path to database file if using sqlite3.
        'USER': db_host['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host['password'],                  # Not used with sqlite3.
        'HOST': db_host['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
    'F_DB_REPORT_PS_slave': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'F_DB_REPORT_PS',                      # Or path to database file if using sqlite3.
        'USER': db_host_slave['user'],                      # Not used with sqlite3.
        'PASSWORD': db_host_slave['password'],                  # Not used with sqlite3.
        'HOST': db_host_slave['host'],                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': db_host_slave['port'],                      # Set to empty string for default. Not used with sqlite3.
    },
}


class AtomRouter(object):
    """Default Router for Atom services"""

    def db_for_read(self, model, **hints):
        if hasattr(model, '_db'):
            if model._db in (
                'F_DB_USER_SH', 'F_DB_EVENT_SH'
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
        return True

    def allow_syncdb(self, db, model):
        if hasattr(model, '_db'):
            model_db = model._db
        else:
            model_db = 'default'
        return db == model_db

MALL_DATABASES = {
    'default':DATABASES['f_shop'],
    'f_shop':DATABASES['f_shop'],
    'pay':DATABASES['pay'],
    'cloud_order': DATABASES['cloud_order'],

    'F_DB_EVENT': DATABASES['F_DB_EVENT'],
    'F_DB_EVENT_SH': DATABASES['F_DB_EVENT_SH'],
    'F_DB_EVENT_SH_SUMMARY': DATABASES['F_DB_EVENT_SH_SUMMARY'],
    'F_DB_EVENT_PS': DATABASES['F_DB_EVENT_PS'],
    'F_DB_EVENT_PS_SUMMARY': DATABASES['F_DB_EVENT_PS_SUMMARY'],
    'F_DB_USER_PS': DATABASES['F_DB_USER_PS'],
    'F_DB_USER_SH': DATABASES['F_DB_USER_SH'],

    'F_DB_EVENT_slave': DATABASES['F_DB_EVENT_slave'],
    'F_DB_EVENT_SH_slave': DATABASES['F_DB_EVENT_SH_slave'],
    'F_DB_EVENT_SH_SUMMARY_slave': DATABASES['F_DB_EVENT_SH_SUMMARY_slave'],
    'F_DB_EVENT_PS_slave': DATABASES['F_DB_EVENT_PS_slave'],
    'F_DB_EVENT_PS_SUMMARY_slave': DATABASES['F_DB_EVENT_PS_SUMMARY_slave'],
    'F_DB_USER_PS_slave': DATABASES['F_DB_USER_PS_slave'],
    'F_DB_USER_SH_slave': DATABASES['F_DB_USER_SH_slave'],

    'f_shop_slave':DATABASES['f_shop_slave'],
    'pay_slave':DATABASES['pay_slave'],
    'cloud_order_slave': DATABASES['cloud_order_slave'],
}

ACCOUNT_DATABASES = {
    'default': DATABASES['f_account'],
    'f_account': DATABASES['f_account'],
    'F_DB_USER_SH': DATABASES['F_DB_USER_SH'],
    'F_DB_EVENT_SH': DATABASES['F_DB_EVENT_SH'],
    'F_DB_EVENT_SH_SUMMARY': DATABASES['F_DB_EVENT_SH_SUMMARY'],

    'f_account_slave': DATABASES['f_account_slave'],
    'F_DB_USER_SH_slave': DATABASES['F_DB_USER_SH_slave'],
    'F_DB_EVENT_SH_slave': DATABASES['F_DB_EVENT_SH_slave'],
    'F_DB_EVENT_SH_SUMMARY_slave': DATABASES['F_DB_EVENT_SH_SUMMARY_slave'],
}
