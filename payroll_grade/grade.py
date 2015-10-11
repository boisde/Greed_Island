#!/usr/bin/env python
# coding:utf-8
import os
from model_logics.transwarp.log import init_log
# 配置全局logging. => 配完PYTHON_PATH,在所有的import前做!!!
init_log(os.path.dirname(os.path.abspath(__file__)))

import logging
from bisect import bisect
from model_logics.models import PayrollGrade, DailyRankV3
from model_logics.transwarp import db
from model_logics.config import CONFIGS

# init db:
db.create_engine(**CONFIGS.db)


class PayrollGradeLogic(object):
    """
    Model logic for PayrollGrade.
    """

    """>>>Begin DB functions"""

    @staticmethod
    def find_by(cols, where, group_order_limit, *args):
        # 记得做时间限制, 因为历史数据的表会变的很大.
        where = "%s %s" % (where, group_order_limit)
        return PayrollGrade.find_by(cols, where, *args)

    """<<<End DB functions"""

    """>>>Begin class util functions"""

    @classmethod
    def get_org_grading_guide(cls, statistic_date, middle_team_org_num=None):
        # 拿日营收评级规则
        # TODO 此处调用hjw的函数, 返回 {<中队架构编号>:[tip_goal]}
        # tip_goals = hjw.get_grading_guide(statistic_date, middle_team_org_num)
        tip_goals = {
            u'0000000000000000000000000000000000000000000010010070020000000000': [x for x in xrange(10, 151, 20)]}
        if middle_team_org_num:
            tip_goal = tip_goals[middle_team_org_num]
            if isinstance(tip_goal, list) and len(tip_goal) == 8:
                pass
            elif isinstance(tip_goal, list) and len(tip_goal) > 8:
                tip_goals[middle_team_org_num] = tip_goal[-8:]
                logging.warning("Tip_goals for middle_team[%s] is longer than 8." % middle_team_org_num)
            else:
                logging.exception("Tip_goals for middle_team[%s] is Un-processable." % middle_team_org_num)
        else:
            pass
        return tip_goals

    @classmethod
    def get_grade_spots_per_middle_team(cls, mid_team_size):
        # mid_team_size: [1:6), [6:11), [11:16), [16:21), [21:max)
        mid_team_size_spots = [[0, 0, 0], [0, 0, 1], [0, 1, 2], [1, 2, 3], [1, 2, 4], [1, 3, 5]][
            bisect([1, 6, 11, 16, 21], mid_team_size)]
        print ("mid_team_size=[%d], spots=[%s]" % (mid_team_size, mid_team_size_spots))
        return mid_team_size_spots

    @classmethod
    def grade_man(cls, tip, level, tip_goal):
        # 前一个数组长度必须比后一个大一, 比如前一个为9, 后面一个必须为8
        # [90,  80,  70,  60,  50,  40,  30,  20,  10]
        #   [140, 160, 180, 200, 220, 240, 260, 280]
        grades = [x for x in xrange(90, (90 - 10 * level - 1), -10)]
        tip_goal = tip_goal[:level]
        grade = grades[bisect(tip_goal, tip)]
        print (
            "tip=[%.1f], grade=[%s]. using grades=%s, tip_goal=%s, level=[%s]" % (tip, grade, grades, tip_goal, level))
        return grade

    @classmethod
    def get_grades(cls, statistic_date, deliveryman_id=None):
        man_grades = {}  # {<user_id>: <grade>} eg. {7740959: 20}
        # 取单个
        if deliveryman_id:
            # 取该配送员架构编号, 该配送员所属中队架构编号
            drv3 = DailyRankV3.find_by('user_id, org_num', 'where statistic_date=? AND user_id=?', statistic_date,
                                       deliveryman_id)[0]
            middle_team_org_num = drv3.org_num[:len(drv3.org_num) - 9] + '0' * 9
            # TODO 取当日中队出勤队员人数: 此处调用hjw的函数, 返回 {<中队架构编号>:number_of_teammates_on_duty_per_date}
            # number_of_middle_teammates = hjw.get_middle_teammates_on_duty_per_date(statistic_date, middle_team_org_num)
            number_of_middle_teammates = 1
            # 拿日营收评级规则
            tip_goal = cls.get_org_grading_guide(statistic_date, middle_team_org_num)[middle_team_org_num]
            spots = cls.get_grade_spots_per_middle_team(number_of_middle_teammates)
            # 拿中队日营收并从高到低排序
            daily_tips = DailyRankV3.find_by('user_id, tip',
                                             'where statistic_date=? and org_num regexp ?',
                                             statistic_date, drv3.org_num[:len(drv3.org_num) - 9] + '.' * 9)
            print len(daily_tips)
            daily_ranking = sorted(daily_tips, cmp=lambda x, y: cmp(x.tip, y.tip), reverse=True)
            for i in xrange(len(daily_ranking) - 1):  # {'user_id': 7740959, 'tip': 125.1}
                man = daily_ranking[i]
                nxt = daily_ranking[i + 1]  # 用于处理并列
                lower = 0
                for j in xrange(len(spots)):
                    if spots[j] == 0:
                        lower = j + 1
                        continue
                    else:
                        break
                level = 8 - lower  # 坑没了, 降评级
                print("lower=[%s]" % lower)
                # 先评级
                grade = cls.grade_man(man.tip, level, tip_goal)
                # 判断是否占了现有的最高的坑, 更新spots数组; (lower+1)*10只可能是10,20,30,40(要排除40的情况)
                if lower < 3 and (
                    lower + 1) * 10 == grade and nxt.tip != man.tip:  # 评级刚好在现有最高的坑上, 不是同一个人(第一个人的情况除外), 且不是并列.
                    spots[lower] -= 1
                print "adding man=[%s]" % man.user_id
                man_grades[man.user_id] = grade
            # 有且只有一个人/处理最后一个人
            if len(daily_ranking) == 1 or i + 1 == len(daily_ranking):
                nxt = daily_ranking[-1]
                lower = 0
                for j in xrange(len(spots)):
                    if spots[j] == 0:
                        lower = j + 1
                        continue
                    else:
                        break
                level = 8 - lower  # 坑没了, 降评级
                print "adding man=[%s]" % nxt.user_id
                man_grades[nxt.user_id] = cls.grade_man(nxt.tip, level, tip_goal)
        # TODO 取所有
        else:
            pass
        return man_grades

    """<<<End class util functions"""

    """>>>Begin class API functions"""
    """<<<End class API functions"""


if __name__ == '__main__':
    for t_mid_team_size in [-1, 0, 1, 5, 6, 11, 15, 16, 21, 1000]:
        PayrollGradeLogic.get_grade_spots_per_middle_team(t_mid_team_size)

    for t_tip in [0, 10.3, 90, 98.3, 100.3, 200.2, 210.2, 220.2, 240.2, 260, 260, 260, 260.2, 260.2, 280.2]:
        PayrollGradeLogic.get_grades('2015-8-2', deliveryman_id=7751524)
