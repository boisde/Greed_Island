# -*- coding:utf-8 -*-

class InvalidParams(Exception):
    pass


# 业务错误
class ServiceError(Exception):
    """ status_code, msg """
    pass


# 事件错误
class EventError(Exception):
    pass


# 定时任务有误
class PeriodicError(Exception):
    pass