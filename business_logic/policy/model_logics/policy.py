#!/usr/bin/env python
# coding:utf-8

from tools_lib.transwarp.tz import utc_8_now
from tools_lib.transwarp.validate import is_valid_kw
from tools_lib.transwarp import db
from models import Policy, DailyPolicy


class PolicyLogic(object):
    """
    Model logic for Policy.
    """
    """>>>Begin DB functions"""
    @staticmethod
    def create(**kw):
        kw['state'] = None
        now = utc_8_now()
        kw['create_time'] = now
        kw['update_time'] = now
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(Policy, **kw)
        # 检查id,policy_name, 如果存在record, 不允许添加
        sanity_check = Policy.find_by('id, policy_name', 'where id=? OR policy_name=?',
                                      *[kw['id'], kw['policy_name']])
        if sanity_check:
            raise ValueError("Already exist record with id=[%s], policy_name=[%s]." % (sanity_check[0]['id'], sanity_check[0]['policy_name']))
        policy = Policy(**kw)
        policy.insert()

    @staticmethod
    def update(policy_id, **kw):
        # 参数合法性检查. 如果不合法,直接报错.
        is_valid_kw(Policy, is_update=True, **kw)
        # 获取想要的记录
        p = Policy.get('id', policy_id)
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
        return Policy.find_by(cols, where, *args)
    """<<<End DB functions"""


class DailyPolicyLogic(object):
    @staticmethod
    def snapshot():
        # 批量插入之前, 先将已有的当日快照数据删掉
        statistic_date = utc_8_now(is_date=True)
        db.update('delete from `%s` where `statistic_date`=?' % DailyPolicy.__table__, statistic_date)

        cols = ["policy_name", "policy_content", "start_effect_time", "end_effect_time", "applied_to", "notification",
                "policy_leader", "state", "create_time", "update_time", "statistic_date"]
        p_today = PolicyLogic.find_by('*', '', '')
        data = []
        for p in p_today:
            data.append((p.policy_name, p.policy_content, p.start_effect_time, p.end_effect_time, p.applied_to,
                         p.notification, p.policy_leader, p.state, p.create_time, p.update_time, statistic_date))
        if data:
            db.insert_many(DailyPolicy.__table__, cols, data)
        return len(data)