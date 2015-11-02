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



@api
@post('/hot_order/create/:yes_or_no')
def api_hot_order_create(yes_or_no):
    print type(yes_or_no), yes_or_no
    # TODO 1. AG判断时间,地区内的人力 2.返回YES/NO 3.记录log到DB
    if yes_or_no == 1:
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


@api
@get('/hot_order/check_notify_reset')
def api_hot_order_check_notify_reset():
    def long_task(t_receivers, t_ids, t_names, t_states):
        send_mail(t_receivers, '(线上)定时任务运行错误',
                  '出错任务id=[%s],\n 任务名=[%s],\n 任务状态=[%s]\n' % (t_ids, t_names, t_states))

    # 每天早上10点, 判断凌晨的定时任务有没有跑/跑成功. 判断完, 1.发邮件,2.RESET.
    # 1.拿hot_order表里所有deleted不为1的id,state; 2.取出所有state不为OK的err_policies, 如果err_policies不为空, 发邮件; 3.RESET.
    all_policies = HotOrderLogic.find_by('id, hot_order_name, state, date(update_time)', '', '')
    err_policies = []
    for p in all_policies:
        if p['state'] != 'OK':
            err_policies.append(p)
        elif p['state'] == 'OK' and p['date(update_time)'] != utc_8_now(is_date=True):
            err_policies.append(p)
    if err_policies:
        # 发邮件
        receivers = ['chenxinlu@123feng.com']
        ids = ",".join([unicode(x.id).encode('utf-8') for x in err_policies])
        names = ",".join([x.hot_order_name.encode('utf-8') for x in err_policies])
        states = ",".join([x.state.encode('utf-8') for x in err_policies])
        # 创建一个定时器, 1秒hook到发警报邮件的任务函数(因为发邮件时间太长,接口不该等在那里)
        t = Timer(1.0, long_task, args=[receivers, ids, names, states])
        # 开启定时器
        t.start()
    # RESET
    FSM.reset("RESET")
    return err_policies


""">>>End REST api for HotOrder"""
