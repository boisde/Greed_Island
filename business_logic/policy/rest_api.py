#!/usr/bin/env python
# coding:utf-8

"""
REST API definition.
"""
from threading import Timer
from tools_lib.transwarp.tz import utc_8_now
from tools_lib.transwarp.web import ctx, post, api, get
from tools_lib.mail import send_mail
from model_logics.policy import PolicyLogic, DailyPolicyLogic
from model_logics.fsm import FSM

"""API definition order: CREATE->DELETE->UPDATE->SELECT->OTHER"""
""">>>Begin REST api for Policy"""


@api
@get('/policy/check_notify_reset/:is_notify')
def api_check_notify_reset(is_notify):
    def long_task(t_receivers, t_ids, t_names, t_states):
        send_mail(t_receivers, '(线上)定时任务运行错误',
                               '出错任务id=[%s],\n 任务名=[%s],\n 任务状态=[%s]\n' % (t_ids, t_names, t_states))
    # 每天早上10点, 判断凌晨的定时任务有没有跑/跑成功. 判断完, 1.发邮件,2.RESET.
    # 1.拿policy表里所有deleted不为1的id,state; 2.取出所有state不为OK的err_policies, 如果err_policies不为空, 发邮件; 3.RESET.
    all_policies = PolicyLogic.find_by('id, policy_name, state, date(update_time)', '', '')
    err_policies = []
    for p in all_policies:
        if p['state'] != 'OK':
            err_policies.append(p)
        elif p['state'] == 'OK' and p['date(update_time)'] != utc_8_now(is_date=True):
            err_policies.append(p)
    if is_notify == '1':
        if err_policies:
            # 发邮件
            receivers = ['chenxinlu@123feng.com','hujunwei@123feng.com']
            ids = ",".join([unicode(x.id).encode('utf-8') for x in err_policies])
            names = ",".join([x.policy_name.encode('utf-8') for x in err_policies])
            states = ",".join([x.state.encode('utf-8') for x in err_policies])
            # 创建一个定时器, 1秒hook到发警报邮件的任务函数(因为发邮件时间太长,接口不该等在那里)
            t = Timer(1.0, long_task, args=[receivers, ids, names, states])
            # 开启定时器
            t.start()
        else:
            return err_policies
    else:
        # RESET
        FSM.reset("RESET")
    return err_policies


@api
@post('/policy/update_state')
def api_update_state():
    # 参数validate主要在DB层实现
    req = ctx.request.input()
    FSM.update_state(**req)


@api
@get('/policy/check_state/:policy_id')
def api_check_state(policy_id):
    # 简单判断policy_id是否存在
    _p = PolicyLogic.find_by('id, policy_name, state, date(update_time)', 'where id=?', '', policy_id)
    if not _p:
        raise AttributeError("Policy with id=[{}] not found.".format(policy_id))
    elif _p[0]['date(update_time)'] != utc_8_now(is_date=True):
        return "NO_RUN"
    else:
        return _p[0]['state']


@api
@post('/policy/create')
def api_policy_create():
    request = ctx.request.input()
    PolicyLogic.create(**request)


@api
@post('/policy/snapshot')
def api_policy_snapshot():
    DailyPolicyLogic.snapshot()
""">>>End REST api for Policy"""
