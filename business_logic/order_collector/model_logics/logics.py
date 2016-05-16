#!/usr/bin/env python
# coding:utf-8

from tools_lib.transwarp.tz import utc_8_now
from tools_lib.transwarp.validate import is_valid_kw
from models import HotOrder, OrderStateLog


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
        # 检查id,hot_order_name, 如果存在record, 不允许添加
        sanity_check = HotOrder.find_by('order_id', 'where order_id=? AND gen_from=?',
                                        *[kw['order_id'], kw['gen_from']])
        if sanity_check:
            raise ValueError("Already exist record with id=[%s], hot_order_name=[%s]." % (sanity_check[0]['id'], sanity_check[0]['hot_order_name']))
        hot_order = HotOrder(**kw)
        hot_order.insert()

    @staticmethod
    def update(hot_order_id, **kw):
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(HotOrder, is_update=True, **kw)
        # 获取想要的记录
        p = HotOrder.get('id', hot_order_id)
        # 如果找不到这条记录,报错
        if not p:
            raise AttributeError("Could not find in hot_order with [id]=[%s]. So could not update it, either."
                                 % hot_order_id)
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


class OrderStateLogLogic(object):
    """
    Model logic for OrderState.
    """
    """>>>Begin DB functions"""

    @staticmethod
    def create(**kw):
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(OrderStateLog, **kw)
        now = utc_8_now()
        kw['state_change_time'] = kw.get('state_change_time', now)
        task_state = OrderStateLog(**kw)
        task_state.insert()

    @staticmethod
    def find_by(cols, where, group_order_limit, *args):
        where = "%s %s" % (where, group_order_limit)
        return OrderStateLog.find_by(cols, where, *args)
    """<<<End DB functions"""
