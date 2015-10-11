#!/usr/bin/env python
# coding:utf-8

"""
Models for payroll_grade
"""
from transwarp.orm import Model, StringField, IntegerField, DateTimeField, DateField

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class PayrollGrade(Model):
    """存储薪资等级Model,存储配送员日营收评级(可能需要实时),用于薪资结算,历史数据查询"""
    __table__ = "payroll_grade"
    id = IntegerField(ddl='int(11)', comment=u'日营收等级id', primary_key=True)

    statistic_date = DateField(comment=u'哪一日的营收', key=True)
    deliveryman_id = IntegerField(default=None, nullable=False, ddl='int(11)', comment=u'风先生id', key=True)
    grade = IntegerField(default=None, nullable=False, ddl='int(3)', comment=u'风先生当日营收评级[10,90,step=10]')

    middle_team_org_num = StringField(default=None, nullable=False, ddl='varchar(32)', comment=u'所属中队架构编号')
    delivery_fee = IntegerField(default=None, nullable=False, ddl='int(11)', comment=u'配送费(日营收), 单位为分')
    delivery_fee_goal = IntegerField(default=None, nullable=False, ddl='int(11)', comment=u'配送费(日营收)目标值, 单位为分')
    delivery_fee_rank = IntegerField(default=None, nullable=True, ddl='int(3)', comment=u'配送费(日营收)在所属中队中的排名')

    create_time = DateTimeField(key=True, auto_now_add=True)
    update_time = DateTimeField(auto_now=True)


class DailyRankV3(Model):
    """仅用于读取计算日营收评级相关数据"""
    __table__ = "daily_rank_v3"
    id = IntegerField(ddl='int(11)', comment=u'id', primary_key=True)

    statistic_date = DateField(comment=u'哪一日的营收', key=True)
    user_id = IntegerField(default=None, nullable=False, ddl='int(11)', comment=u'风先生id', key=True)
    org_num = StringField(default=None, nullable=False, ddl='varchar(65)', comment=u'所属中队架构编号')
    number_of_middle_teammates = IntegerField(ddl='smallint(6)', comment=u'该日所属中队成员数')


if __name__ == "__main__":
    print PayrollGrade().__sql__()
    print DailyRankV3().__sql__()