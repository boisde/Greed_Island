#!/usr/bin/env python
# coding:utf-8

"""
Models for policy
"""

from tools_lib.transwarp.orm import Model, StringField, IntegerField, DateTimeField, DateField

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class Policy(Model):
    """运营政策Model, 存储带有时效性的运营策略信息"""
    __table__ = 'policy'

    id = IntegerField(ddl='int(11)', primary_key=True)
    policy_name = StringField(default=None, nullable=False, ddl='varchar(64)', comment=u'运营政策名称')
    policy_content = StringField(default=None, nullable=False, ddl='varchar(512)', comment=u'运营政策详情')
    start_effect_time = DateTimeField(nullable=True, comment=u'开始生效时间', key=True)
    end_effect_time = DateTimeField(nullable=True, comment=u'结束生效时间', key=True)
    applied_to = StringField(ddl='varchar(128)', comment=u'适用人群')
    notification = StringField(nullable=True, ddl='varchar(256)', comment=u'提醒/通知的内容')
    policy_leader = StringField(nullable=True, ddl='varchar(32)', comment=u'政策负责人')
    state = StringField(default=None, nullable=True, ddl='varchar(16)',
                        comment=u'定时任务状态 RESET:今日尚未启动 STARTED:已启动 OK:运行成功'
                                u' RUNTIME-ERR:运行错误 TIMEOUT-ERR:运行超时', key=True)

    create_time = DateTimeField(auto_now_add=True, key=True)  # UTC+8:00
    update_time = DateTimeField(auto_now=True, key=True)  # UTC+8:00

    def __hash__(self):
        return hash("%d" % self.id)

    def __eq__(self, other):
        return self.id == other.id


class TaskState(Model):
    """运营政策相关定时任务状态变化Model, 存储定时任务运行状态相关的事件"""
    __table__ = 'task_state'

    id = IntegerField(ddl='int(11)', primary_key=True)
    policy_task_id = IntegerField(ddl='int(11)', key=True)
    policy_name = StringField(default=None, nullable=False, ddl='varchar(64)', comment=u'运营政策名称')
    state_change_time = DateTimeField(auto_now=True)  # UTC+8:00
    state = StringField(default=None, nullable=True, ddl='varchar(16)',
                        comment=u'定时任务状态 RESET:今日尚未启动 STARTED:已启动 OK:运行成功 RUNTIME-ERR:运行错误 TIMEOUT-ERR:运行超时', key=True)
    state_info = StringField(default=None, nullable=True, ddl='varchar(256)', comment=u'状态变更详细信息')


class DailyPolicy(Model):
    """运营政策Model的每日快照, 存储带有时效性的运营策略信息(每日定时调用RESET之前建立快照)"""
    __table__ = 'daily_policy'

    id = IntegerField(ddl='int(11)', primary_key=True)
    policy_name = StringField(default=None, nullable=False, ddl='varchar(64)', comment=u'运营政策名称')
    policy_content = StringField(default=None, nullable=False, ddl='varchar(512)', comment=u'运营政策详情')
    start_effect_time = DateTimeField(nullable=True, comment=u'开始生效时间', key=True)
    end_effect_time = DateTimeField(nullable=True, comment=u'结束生效时间', key=True)
    applied_to = StringField(ddl='varchar(128)', comment=u'适用人群')
    notification = StringField(nullable=True, ddl='varchar(256)', comment=u'提醒/通知的内容')
    policy_leader = StringField(nullable=True, ddl='varchar(32)', comment=u'政策负责人')
    state = StringField(default=None, nullable=True, ddl='varchar(16)',
                        comment=u'定时任务状态 RESET:今日尚未启动 STARTED:已启动 OK:运行成功'
                                u' RUNTIME-ERR:运行错误 TIMEOUT-ERR:运行超时', key=True)

    create_time = DateTimeField(auto_now_add=True, key=True)  # UTC+8:00
    update_time = DateTimeField(auto_now=True, key=True)  # UTC+8:00
    statistic_date = DateField(key=True)


if __name__ == "__main__":
    print Policy().__sql__()
    print TaskState().__sql__()
    print DailyPolicy().__sql__()
