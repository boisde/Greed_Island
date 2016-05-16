#!/usr/bin/env python
# coding:utf-8

import logging
from datetime import datetime
from tools_lib.transwarp.web import UTC_0, UTC_8
from models import TaskState, DATETIME_FORMAT


class TaskStateLogic(object):
    """
    Model logic for TaskState.
    """
    """>>>Begin DB functions"""

    @staticmethod
    def create(**kw):
        # 参数合法性检查. 如果不合法,直接报错.
        TaskStateLogic.is_valid_kw(**kw)
        now = datetime.utcnow().replace(tzinfo=UTC_0).astimezone(UTC_8).strftime(DATETIME_FORMAT)
        kw['create_time'] = kw.get('create_time', now)
        kw['update_time'] = kw.get('update_time', now)
        task_state = TaskState(**kw)
        task_state.insert()

    @staticmethod
    def find_by(cols, where, group_order_limit, *args):
        where = "%s %s" % (where, group_order_limit)
        return TaskState.find_by(cols, where, *args)
    """<<<End DB functions"""

    """>>>Begin class util functions"""

    @staticmethod
    def is_valid_kw(**kw):
        mappings = TaskState.__mappings__
        # 检查是否要求存在的参数都存在
        args = set(kw.keys())
        required = {key_name for key_name, orm_val in mappings.iteritems() if orm_val.nullable is False and orm_val.primary_key is False}
        if not required.issubset(args):
            raise ValueError("Not providing required args: %s." % list(required-args))
        # 检查参数类型
        for key_name, kv in kw.iteritems():
            if key_name in mappings:
                orm_val = mappings[key_name]
                if orm_val.ddl.find('int') != -1:
                    try:
                        int(kv)
                    except ValueError:
                        raise ValueError("[%s]:[%s] should be type of [%s]." % (key_name, str(kv), orm_val.ddl))
                elif orm_val.ddl.find('char') != -1:
                    char_len = int(orm_val.ddl[orm_val.ddl.find('(') + 1:orm_val.ddl.find(')')])
                    if (not kv) and orm_val.nullable == True:  # 参数值设置可以为空且传入参数就是空
                        continue
                    elif kv and len(kv) > char_len:
                        raise ValueError("[%s]:[%s] should be str of length[%s]." % (key_name, str(kv), char_len))
            else:
                logging.warning(
                    "[%s]:[%s] won't be passed since [%s] is not valid." % (key_name, kv, key_name))

    """<<<End class util functions"""

    """>>>Begin class API functions"""
    """<<<End class API functions"""
