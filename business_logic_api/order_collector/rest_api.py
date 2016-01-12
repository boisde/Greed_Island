#!/usr/bin/env python
# coding:utf-8

"""
REST API definition.
"""
from threading import Timer
from tools_lib.transwarp.tz import utc_8_now
from tools_lib.transwarp.web import ctx, post, api, get
from tools_lib.mail import send_mail
from model_logics.logics import HotOrderLogic, OrderStateLogLogic
from model_logics.fsm import FSM

"""API definition order: CREATE->DELETE->UPDATE->SELECT->OTHER"""
""">>>Begin REST api for HotOrder"""


def api_hot_order_create():
    # TODO 1. 判断时间,地区内的人力,返回YES/NO 2.人力为YES,调用专人直送创建,返回Created/NotCreated 3.记录log到DB
    request = ctx.request.input()
    OrderStateLogLogic.create(**request)
    HotOrderLogic.create(**request)


@api
@post('/hot_order/update_state')
def api_hot_order_update_state():
    # 参数validate主要在DB层实现
    req = ctx.request.input()
    FSM.update_state(**req)


@api
@get('/hot_order/check_state/:hot_order_id')
def api_hot_order_check_state(hot_order_id):
    # 简单判断hot_order_id是否存在
    _p = HotOrderLogic.find_by('id, hot_order_name, state, date(update_time)', 'where id=?', '', hot_order_id)
    if not _p:
        raise AttributeError("HotOrder with id=[{}] not found.".format(hot_order_id))
    elif _p[0]['date(update_time)'] != utc_8_now(is_date=True):
        return "NO_RUN"
    else:
        return _p[0]['state']


""">>>End REST api for HotOrder"""
