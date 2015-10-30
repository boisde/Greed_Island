# -*- coding:utf-8 -*-
import sys
import platform
from copy import deepcopy
from functools import wraps
from gtz import TimeZone

def platform_pass(node_list=[]):
    """
    平台可执行
    :param node_list: 可执行的机器号列表
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            if platform.node() in node_list:
                return func(*args, **kwargs)
        return __wrapper
    return wrapper


def platform_stop(node_list=[]):
    """
    平台不可执行
    :param node_list: 不可执行的机器号列表
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            if platform.node() not in node_list:
                return func(*args, **kwargs)
        return __wrapper
    return wrapper


def class_authenticated(func):
    """
    判断是否登录
    """
    def wrapper(self, request, *args, **kwargs):
        return func(self, request, *args, **kwargs)
    return wrapper


def func_log(func):
    """
    打印开始和结束时间
    @param func:
    @return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print "[{ct}] starting {func_name}...".format(ct=TimeZone.local_now(), func_name=func.__name__)
        rst = func(*args, **kwargs)
        print "[{ct}] ending {func_name}...".format(ct=TimeZone.local_now(), func_name=func.__name__)
        return rst
    return wrapper

def update_sys_path(append_sys_path=[]):
    """
    动态修改sys.path列表，函数执行后恢复
    @param append_sys_path:
    @return:
    """
    def wrapper(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            old_sys_path = deepcopy(sys.path)
            for _path in append_sys_path:
                sys.path.insert(0, _path)
            rst = func(*args, **kwargs)
            sys.path = old_sys_path
            return rst
        return __wrapper
    return wrapper
