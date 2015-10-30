#!/usr/bin/env python
# coding:utf-8

from tools_lib.transwarp.tz import utc_8_now
from tools_lib.transwarp.validate import is_valid_kw
from models import HotOrder, OrderState


class HotOrderLogic(object):
    """
    Model logic for HotOrder.
    """
    """>>>Begin DB functions"""
    @staticmethod
    def create(**kw):
        kw['state'] = None
        now = utc_8_now()
        kw['create_time'] = now
        kw['update_time'] = now
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(HotOrder, **kw)
        # 检查id,policy_name, 如果存在record, 不允许添加
        sanity_check = HotOrder.find_by('id, policy_name', 'where id=? OR policy_name=?',
                                        *[kw['id'], kw['policy_name']])
        if sanity_check:
            raise ValueError("Already exist record with id=[%s], policy_name=[%s]." % (sanity_check[0]['id'], sanity_check[0]['policy_name']))
        policy = HotOrder(**kw)
        policy.insert()

    @staticmethod
    def update(policy_id, **kw):
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(HotOrder, is_update=True, **kw)
        # 获取想要的记录
        p = HotOrder.get('id', policy_id)
        # 如果找不到这条记录,报错
        if not p:
            raise AttributeError("Could not find in policy with [id]=[%s]. So could not update it, either."
                                 % policy_id)
        for key_name in kw:
            if key_name in p:
                p[key_name] = kw[key_name]
        now = utc_8_now()
        p['update_time'] = now
        p.update()

    @staticmethod
    def find_by(cols, where, group_order_limit, *args):
        where = "%s %s" % (where, group_order_limit)
        return HotOrder.find_by(cols, where, *args)
    """<<<End DB functions"""


class OrderStateLogic(object):
    """
    Model logic for OrderState.
    """
    """>>>Begin DB functions"""

    @staticmethod
    def create(**kw):
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(OrderState, **kw)
        now = utc_8_now()
        kw['create_time'] = kw.get('create_time', now)
        kw['update_time'] = kw.get('update_time', now)
        task_state = OrderState(**kw)
        task_state.insert()

    @staticmethod
    def find_by(cols, where, group_order_limit, *args):
        where = "%s %s" % (where, group_order_limit)
        return OrderState.find_by(cols, where, *args)
    """<<<End DB functions"""
