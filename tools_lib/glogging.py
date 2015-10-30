# -*- coding:utf-8 -*-
__author__ = 'Harrison'

import logging
import os
import traceback
import platform
from tools_lib.host_info import *


class GLogging(object):
    # 日志文件路径
    LOGFILE_PATH = {
        BL_SERVICE_NODE: "/root/gezbox/Atom/log",
        TEST_BL_SERVICE_NODE: "/root/gezbox/Atom/log",
    }.get(platform.node(), os.path.join(os.path.dirname(__file__), 'log'))
    # 日志保存天数
    LOG_BACKUP_COUNT = 90

    ###########################################################
    # 日志类型
    ###########################################################
    PUSH_LOGGER = 'push_logger'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'data': {
                'format': "[%(asctime)s] %(levelname)s: %(message)s",
                'datefmt': "%Y/%m/%d %H:%M:%S"
            },
        },
        'handlers': {
            'push_handler': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': "%s/data/%s" % (LOGFILE_PATH, "push.log"),
                'when': 'midnight',
                'encoding': 'utf-8',
                'backupCount': LOG_BACKUP_COUNT,
                'formatter': 'data',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
        },
        'loggers': {
            PUSH_LOGGER: {
                'handlers': ['push_handler'],
                'level': 'INFO',
            }
        }
    }
    logging.config.dictConfig(LOGGING)

    @staticmethod
    def get_logger(logger_name=PUSH_LOGGER):
        return logging.getLogger(logger_name)

    @classmethod
    def write_log(cls, logger_name=PUSH_LOGGER, msg=''):
        """
        写日志
        @param logger_name: logger名称
        @param msg: 日志内容
        @return:
        """
        try:
            cls.get_logger(logger_name).info(msg)
        except:
            print traceback.format_exc()

    @classmethod
    def write_excepton(cls, logger_name=PUSH_LOGGER, msg=''):
        """
        写异常
        @param logger_name:
        @param msg:
        @return:
        """
        try:
            cls.get_logger(logger_name).exception(msg)
        except:
            print traceback.format_exc()

