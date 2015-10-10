#!/usr/bin/env python
# coding:utf-8

# from mm_common.user_center.models.dispatch_center import DispatchRecord
# from mm_common.area_center.models.city import CityHRManagerRelation
# from mm_common.event_center.models.deliver_fsm_log import DeliverFSMLog
# from mm_common.user_center.models.deliver_images import DeliverImage
# from mm_common.user_center.models.real_info import RealInfo
# from mm_common.user_center.models.apply_deliver import ApplyDeliver
# from mm_common.user_center.models.deliver_org import DeliverOrg
# from lib.gedis import Redis
# from lib.utils.node_utils import get_staff_info
# from lib.redis_key import key_deliver_auto_quit_absent_days
# from lib.timezone import TimeZone
# from lib.glogging import GLogging

from bisect import bisect
# class DeliverUtils(object):
#     height_score_map = {
#         # 男
#         1: {
#             1: 3,  # 180以上
#             2: 5,  # 170~180
#             3: 3,  # 165~169
#             4: 1,  # 165以下
#             5: 1,  # 160~164
#             # 0: -1  # 160以下/其他 不通过
#         },
#         # 女
#         2: {
#             1: 3,  # 170 以上
#             2: 5,  # 160~170
#             3: 3,  # 155~159
#             # 0: -1  # 155以下/其他 不通过
#         }
#     }
#
#     for age in [-1, 0, 1, 17, 18, 19, 22, 42, 43, 1000]:
#         from bisect import bisect
#         # age=0, 0分; 18 <= age < 22, 8分; 22 <= age <= 42, 10分; 其它, -1分.
#         age_score = [-1, 0, -1, 8, 10, -1][bisect([0, 1, 18, 22, 43], age)]
#         print ("age=[%d], score=[%d]" % (age, age_score))


class StaffFSM(object):
    """
    配送员有限状态机
    """
    ################################################
    # 配送员状态
    ################################################
    # 初始状态
    CHECK_STATUS_INIT = 1 # 'CHECK_INIT'
    # 城市未开通
    CHECK_STATUS_NO_AREA_MANAGER = 2 # 'CHECK_NO_AREA_MANAGER'
    # 评分未通过
    CHECK_STATUS_REGISTERED_DENY = 'CHECK_REGISTERED_DENY'
    # WEB注册
    CHECK_STATUS_WEB_REGISTERED = 'CHECK_WEB_REGISTERED'
    # APP注册
    CHECK_STATUS_APP_REGISTERED = 'CHECK_APP_REGISTERED'
    # 兼职审核通过
    CHECK_STATUS_PART_TIME_WORKING = 'CHECK_PART_TIME_WORKING'
    # 申请全职待审核状态
    CHECK_STATUS_APPLY_FULL_TIME = 'CHECK_APPLY_FULL_TIME'
    # 申请全职待面试状态
    CHECK_STATUS_WAIT_INTERVIEW = 'CHECK_WAIT_INTERVIEW'
    # 已面试
    CHECK_STATUS_HRBP_INTERVIEWED = 'CHECK_HRBP_INTERVIEWED'
    # 资料待补全
    CHECK_STATUS_WAIT_INFO_COMPLETED = 'CHECK_WAIT_INFO_COMPLETED'
    # 人力审核通过
    # CHECK_STATUS_PENDING = 'CHECK_PENDING'
    # 人力审核拒绝
    # CHECK_STATUS_PENDING_DENY = 'CHECK_PENDING_DENY'
    # 管控审核通过
    CHECK_STATUS_UNALLOCATED = 'CHECK_UNALLOCATED'
    # 管控审核拒绝
    CHECK_STATUS_UNALLOCATED_DENY = 'CHECK_UNALLOCATED_DENY'
    # 已绑定小队
    CHECK_STATUS_BINDING_TEAM = 'CHECK_BINDING_TEAM'
    # 已上岗
    CHECK_STATUS_WORKING = 'CHECK_WORKING'
    # 申请离职
    CHECK_STATUS_RESIGN = 'CHECK_RESIGN'
    # 离职
    CHECK_STATUS_QUITED = 'CHECK_QUITED'
    # 推荐自离
    CHECK_STATUS_RECOMMEND_QUIT = 'CHECK_RECOMMEND_QUIT'
    # 黑名单
    CHECK_STATUS_BANNED = 'CHECK_STATUS_BANNED'
    # 建议淘汰
    CHECK_STATUS_ELIMINATED = 'CHECK_ELIMINATED'
    # 停职
    CHECK_STATUS_RETAIN = 'CHECK_STATUS_RETAIN'
    # 停职申请离职
    CHECK_STATUS_RETAIN_RESIGN = 'CHECK_RETAIN_RESIGN'
    # 7日未入职
    CHECK_STATUS_NO_FIRST_ORDER = 'CHECK_NO_FIRST_ORDER'

    # 过渡期的老状态
    # 人力面试拒绝
    # CHECK_STATUS_HR_INTERVIEWED_DENY = 'CHECK_HR_INTERVIEWED_DENY'
    # 人力面试通过
    # CHECK_STATUS_HR_INTERVIEWED = 'CHECK_HR_INTERVIEWED'
    # # 已注册
    # CHECK_STATUS_REGISTERED = "CHECK_REGISTERED"

    # 状态名称映射表
    CHECK_STATUS_NAME_MAP = {
        CHECK_STATUS_INIT: u'初始状态',
        CHECK_STATUS_NO_AREA_MANAGER: u'城市未开通',
        CHECK_STATUS_REGISTERED_DENY: u'评分未通过',
        CHECK_STATUS_WEB_REGISTERED: u'WEB注册',
        CHECK_STATUS_APP_REGISTERED: u'APP注册',
        CHECK_STATUS_PART_TIME_WORKING: u'兼职审核通过',
        CHECK_STATUS_APPLY_FULL_TIME: u'申请全职待审核',
        CHECK_STATUS_WAIT_INTERVIEW: u'申请全职待面试',
        # CHECK_STATUS_HR_INTERVIEWED_DENY: u'人力面试拒绝',
        # CHECK_STATUS_HR_INTERVIEWED: u'人力面试通过',
        CHECK_STATUS_HRBP_INTERVIEWED: u'已面试',
        CHECK_STATUS_WAIT_INFO_COMPLETED: u'资料待补全',
        # CHECK_STATUS_PENDING: u'人力审核通过',
        # CHECK_STATUS_PENDING_DENY: u'人力审核拒绝',
        CHECK_STATUS_UNALLOCATED: u'管控审核通过',
        CHECK_STATUS_UNALLOCATED_DENY: u'管控审核拒绝',
        CHECK_STATUS_BINDING_TEAM: u'已绑定小队',
        CHECK_STATUS_WORKING: u'已上岗',
        CHECK_STATUS_RESIGN: u'申请离职',
        CHECK_STATUS_QUITED: u'离职',
        CHECK_STATUS_RECOMMEND_QUIT: u'推荐自离',
        CHECK_STATUS_BANNED: u'黑名单',
        CHECK_STATUS_ELIMINATED: u'建议淘汰',
        CHECK_STATUS_RETAIN: u'停职',
        CHECK_STATUS_RETAIN_RESIGN: u'停职申请离职',
        CHECK_STATUS_NO_FIRST_ORDER: u'7日未入职',
    }

    ################################################
    # 不同业务功能配送员状态分类集合
    ################################################
    # 全职能接单状态
    FULL_TIME_CAN_ADOPTED_STATUS_LIST = [
        CHECK_STATUS_WORKING, CHECK_STATUS_RESIGN,
        CHECK_STATUS_RECOMMEND_QUIT, CHECK_STATUS_ELIMINATED,
        CHECK_STATUS_BINDING_TEAM
    ]
    # 所有能接单
    CAN_ADOPTED_STATUS_LIST = FULL_TIME_CAN_ADOPTED_STATUS_LIST + [
        CHECK_STATUS_PART_TIME_WORKING
    ]
    # 可绑定组织架构树的状态集合 = 已上岗状态集合 + 监管审核通过状态
    CAN_BOUND_TREE_STATUS_LIST = CAN_ADOPTED_STATUS_LIST + [CHECK_STATUS_UNALLOCATED]
    CAN_BOUND_TREE_STATUS_LIST.pop(
        CAN_BOUND_TREE_STATUS_LIST.index(CHECK_STATUS_PART_TIME_WORKING)
    )
    # 已离职的状态集合
    QUIT_STATUS_LIST = [
        CHECK_STATUS_QUITED, CHECK_STATUS_BANNED
    ]
    # 待上岗的状态集合
    WAIT_WORKING_STATUS_LIST = [
        # CHECK_STATUS_REGISTERED, CHECK_STATUS_HR_INTERVIEWED,
        # CHECK_STATUS_PENDING,
        CHECK_STATUS_WEB_REGISTERED, CHECK_STATUS_APP_REGISTERED, CHECK_STATUS_WAIT_INFO_COMPLETED,
        CHECK_STATUS_UNALLOCATED, CHECK_STATUS_APPLY_FULL_TIME, CHECK_STATUS_WAIT_INTERVIEW
    ]

    ####################################################
    # 配送员状态转换事件
    ####################################################
    # 城市已开通且评分通过且WEB注册
    EVENT_CITY_SCORE_WEB_YES = 1
    # 城市未开通
    EVENT_CITY_NO = 2
    # 城市已开通且评分已通过且APP注册
    EVENT_CITY_SCORE_APP_YES = 3
    # 城市已开通且评分不通过
    EVENT_CITY_SCORE_NO = 4
    # 人事经理面试通过
    EVENT_HM_INTERVIEW_YES = 5
    # 人事经理面试拒绝
    EVENT_HM_INTERVIEW_NO = 6
    # APP资料补全
    EVENT_COMPLETE_INFO = 7
    # 后台人力审核通过
    EVENT_HR_CHECK_YES = 8
    # 后台人力审核拒绝
    EVENT_HR_CHECK_NO = 9
    # 后台人力判定资料不全
    # EVENT_HR_DECIDE_INFO_INCOMPLETED = 10
    # 后台管控审核通过
    # EVENT_MC_CHECK_YES = 11
    # 后台管控审核拒绝
    # EVENT_MC_CHECK_NO = 12
    # 后台管控审核退回
    # EVENT_MC_RETURN = 22
    # 后台配送架构绑定
    EVENT_BIND_TREE = 13
    # 后台配送架构解绑
    EVENT_UNBIND_TREE = 21
    # 接首单
    EVENT_ADOPT_FIRST_ORDER = 14
    # 申请离职
    EVENT_APPLY_RESIGN = 15
    # 人事经理判定辞退
    EVENT_HM_DECIDE_QUIT = 16
    # 人事经理判定留职
    EVENT_HM_DECIDE_RETAIN = 17
    # 连续3天旷工
    EVENT_CONTINUE_ABSENT = 18
    # 当月累计5次淘汰预警
    EVENT_WARNING = 19
    # 7天未接首单
    EVENT_CONTINUE_NO_FIRST_ORDER = 20
    # 兼职风先生申请成为全职
    EVENT_APPLY_FULL_TIME = 23
    # 绑定区域人力经理
    EVENT_BIND_HRBP = 24
    # 后台拉黑
    EVENT_BANNED = 25
    # 管控拒绝返回兼职状态
    EVENT_MC_RETURN_TO_PART_TIME = 26

    # TODO:以下两个事件是通过trigger在别的事件执行的时候调用的
    # 注册时系统判定全职申请
    EVENT_SYSTEM_JUMP_FULL_TIME = 27
    # 注册时系统判定全职申请然后被拒绝回到初始状态
    # EVENT_SYSTEM_JUMP_INIT = 28

    # # TODO:以下两个事件是通过trigger在别的事件执行的时候调用的
    # # 离职被拒绝返回working(需接首单)
    # EVENT_SYSTEM_DENY_QUIT_TO_WORKING = 30
    # # 离职被拒绝返回已邦队
    # EVENT_SYSTEM_DENY_QUIT_TO_BINDING_TEAM = 31

    # 风先生申请离职然后自己撤销
    EVENT_CANCEL_RESIGN = 28
    # EVENT_APPLY_RESIGN_CANCEL_WITH_FIRST_ORDER = 32     # 返回已邦队且有首单
    # EVENT_APPLY_RESIGN_CANCEL_ONLY_BOUND_TEAM = 33      # 返回仅绑队但是没有首单

    # 风人力反馈面试结果
    EVENT_HRBP_INTERVIEW = 29


    # 定义CallBack
    # === 判断当前状态是否转换兼职为全职
    @classmethod
    def _parttime_to_fulltime(cls, **kw):
        return cls.CHECK_STATUS_UNALLOCATED
    # if obj.check_status == DeliverFSM.CHECK_STATUS_HRBP_INTERVIEWED and (next_status == DeliverFSM.CHECK_STATUS_UNALLOCATED):
    #     obj.job_type = RealInfo.FULL_TIME
    #     obj.qualified_work_time = TimeZone.utc_now()
    #     obj.quit_time = None
    #     obj.first_order_time = None
    #     obj.save(update_fields=['job_type', 'qualified_work_time', 'quit_time', 'first_order_time'])

    # === 判断当前操作是否为离职
    @classmethod
    def _quitting(cls, **kw):
        from_state = kw.get('from_state', None)
        if from_state == cls.CHECK_STATUS_NO_FIRST_ORDER:
            # 离职且拉黑
            cls._ban(**{'staff_id': kw.get('staff_id', None)})
            return cls.CHECK_STATUS_BANNED
        else:
            return cls.CHECK_STATUS_QUITED
    # if next_status == DeliverFSM.CHECK_STATUS_QUITED or (
    #         obj.check_status == DeliverFSM.CHECK_STATUS_NO_FIRST_ORDER and (
    #                     next_status == DeliverFSM.CHECK_STATUS_BANNED)):
    #     obj.quit_time = TimeZone.utc_now()
    #     obj.save(update_fields=['quit_time'])
    #     # 解绑架构
    #     DeliverOrg.filter(user_id=obj.user_id).update(user_id=None)

    # === 判断当前操作是否为拉黑，拉黑除状态修改之外，还需要修改quit_time和banned字段
    @classmethod
    def _ban(cls, **kw):

        return cls.CHECK_STATUS_BANNED
    # if next_status == DeliverFSM.CHECK_STATUS_BANNED and isinstance(obj, RealInfo):
    #     obj.quit_time = TimeZone.utc_now()
    #     obj.banned = True
    #     obj.save(update_fields=['banned', 'quit_time'])
    #     # 解绑架构
    #     DeliverOrg.filter(user_id=obj.user_id).update(user_id=None)

    # === 判断当前操作是否拒绝系统自动推荐离职，拒绝系统推荐离职的同时需要清理缓存
    @classmethod
    def _handle_system_recommend_quit(cls, **kw):
        first_order_time = kw.get('first_order_time', None)

        if first_order_time:
            # todo clear old redis key
            return cls.CHECK_STATUS_WORKING
        else:
            return cls.CHECK_STATUS_BINDING_TEAM

    # if obj.check_status == DeliverFSM.CHECK_STATUS_RECOMMEND_QUIT and (
    #             next_status == DeliverFSM.CHECK_STATUS_WORKING):
    #     user_id = obj.user.id
    #     key = key_deliver_auto_quit_absent_days.format(user_id=user_id)
    #     redis_client = Redis()
    #     redis_client.delete(key)



    # 状态转换字典, 元素结构: (初始状态，条件): 下一个状态
    FSM = {
        (CHECK_STATUS_INIT, EVENT_CITY_NO): CHECK_STATUS_NO_AREA_MANAGER,
        (CHECK_STATUS_INIT, EVENT_CITY_SCORE_NO): CHECK_STATUS_REGISTERED_DENY,
        (CHECK_STATUS_INIT, EVENT_CITY_SCORE_WEB_YES): CHECK_STATUS_WEB_REGISTERED,
        (CHECK_STATUS_INIT, EVENT_CITY_SCORE_APP_YES): CHECK_STATUS_APP_REGISTERED,

        (CHECK_STATUS_WEB_REGISTERED, EVENT_BANNED): _ban,
        (CHECK_STATUS_WEB_REGISTERED, EVENT_HR_CHECK_NO): CHECK_STATUS_INIT,
        # (CHECK_STATUS_WEB_REGISTERED, EVENT_HM_INTERVIEW_NO): CHECK_STATUS_HR_INTERVIEWED_DENY,
        (CHECK_STATUS_WEB_REGISTERED, EVENT_HR_CHECK_YES): CHECK_STATUS_PART_TIME_WORKING,
        (CHECK_STATUS_WEB_REGISTERED, EVENT_HM_INTERVIEW_YES): CHECK_STATUS_WAIT_INFO_COMPLETED,

        (CHECK_STATUS_APP_REGISTERED, EVENT_BANNED): _ban,
        (CHECK_STATUS_APP_REGISTERED, EVENT_HR_CHECK_NO): CHECK_STATUS_INIT,
        # (CHECK_STATUS_APP_REGISTERED, EVENT_HM_INTERVIEW_NO): CHECK_STATUS_HR_INTERVIEWED_DENY,  # 完结状态?
        (CHECK_STATUS_APP_REGISTERED, EVENT_HR_CHECK_YES): CHECK_STATUS_PART_TIME_WORKING,
        (CHECK_STATUS_APP_REGISTERED, EVENT_HM_INTERVIEW_YES): CHECK_STATUS_WAIT_INFO_COMPLETED,

        # 注册的时候选择全职则自动进入全职审核状态
        (CHECK_STATUS_APP_REGISTERED, EVENT_SYSTEM_JUMP_FULL_TIME): CHECK_STATUS_APPLY_FULL_TIME,  # TODO 不自己生成事件,反而让FE/APP调接口.
        (CHECK_STATUS_WEB_REGISTERED, EVENT_SYSTEM_JUMP_FULL_TIME): CHECK_STATUS_APPLY_FULL_TIME,  # TODO 不自己生成事件,反而让FE/APP调接口.

        (CHECK_STATUS_PART_TIME_WORKING, EVENT_APPLY_FULL_TIME): CHECK_STATUS_APPLY_FULL_TIME,

        (CHECK_STATUS_APPLY_FULL_TIME, EVENT_HR_CHECK_NO): CHECK_STATUS_INIT,
        (CHECK_STATUS_APPLY_FULL_TIME, EVENT_BIND_HRBP): CHECK_STATUS_WAIT_INTERVIEW,

        (CHECK_STATUS_WAIT_INTERVIEW, EVENT_MC_RETURN_TO_PART_TIME): CHECK_STATUS_INIT,  # 注册的时候选择全职，然后分别在人力、管控被拒绝
        (CHECK_STATUS_WAIT_INTERVIEW, EVENT_HRBP_INTERVIEW): CHECK_STATUS_HRBP_INTERVIEWED,


        # (CHECK_STATUS_WAIT_INFO_COMPLETED, EVENT_COMPLETE_INFO): CHECK_STATUS_HR_INTERVIEWED,  # 完结状态?
        (CHECK_STATUS_WAIT_INFO_COMPLETED, EVENT_HM_INTERVIEW_YES): CHECK_STATUS_HRBP_INTERVIEWED,

        (CHECK_STATUS_HRBP_INTERVIEWED, EVENT_MC_RETURN_TO_PART_TIME): CHECK_STATUS_INIT,  # 注册的时候选择全职，然后分别在人力、管控被拒绝
        (CHECK_STATUS_HRBP_INTERVIEWED, EVENT_COMPLETE_INFO): CHECK_STATUS_WAIT_INFO_COMPLETED,
        (CHECK_STATUS_HRBP_INTERVIEWED, EVENT_BANNED): _ban,
        (CHECK_STATUS_HRBP_INTERVIEWED, EVENT_HM_INTERVIEW_NO): CHECK_STATUS_PART_TIME_WORKING,
        (CHECK_STATUS_HRBP_INTERVIEWED, EVENT_HM_INTERVIEW_YES): _parttime_to_fulltime,  # todo 需要维护'job_type', 'qualified_work_time', 'quit_time', 'first_order_time'

        (CHECK_STATUS_UNALLOCATED, EVENT_BANNED): _ban,
        (CHECK_STATUS_UNALLOCATED, EVENT_BIND_TREE): CHECK_STATUS_BINDING_TEAM,

        (CHECK_STATUS_BINDING_TEAM, EVENT_UNBIND_TREE): CHECK_STATUS_UNALLOCATED,
        (CHECK_STATUS_BINDING_TEAM, EVENT_BANNED): _ban,
        (CHECK_STATUS_BINDING_TEAM, EVENT_APPLY_RESIGN): CHECK_STATUS_RESIGN,
        (CHECK_STATUS_BINDING_TEAM, EVENT_CONTINUE_NO_FIRST_ORDER): CHECK_STATUS_NO_FIRST_ORDER,  # 定时任务: 7天不接单
        (CHECK_STATUS_BINDING_TEAM, EVENT_ADOPT_FIRST_ORDER): CHECK_STATUS_WORKING,  # KEY

        (CHECK_STATUS_WORKING, EVENT_BANNED): _ban,
        (CHECK_STATUS_WORKING, EVENT_APPLY_RESIGN): CHECK_STATUS_RESIGN,
        (CHECK_STATUS_WORKING, EVENT_CONTINUE_ABSENT): CHECK_STATUS_RECOMMEND_QUIT,  # 定时任务: 3天没接单
        (CHECK_STATUS_WORKING, EVENT_WARNING): CHECK_STATUS_ELIMINATED,  #淘汰配送员, 可以不维护

        (CHECK_STATUS_RESIGN, EVENT_HM_DECIDE_RETAIN): CHECK_STATUS_WORKING,
        (CHECK_STATUS_RESIGN, EVENT_CANCEL_RESIGN): CHECK_STATUS_WORKING,  # 申请离职撤销  todo recheck
        (CHECK_STATUS_RESIGN, EVENT_BANNED): _ban,
        (CHECK_STATUS_RESIGN, EVENT_HM_DECIDE_QUIT): _quitting,  # HM是什么;此处改为QUIT可否(DB中event存储在哪里)

        (CHECK_STATUS_RECOMMEND_QUIT, EVENT_HM_DECIDE_RETAIN): _handle_system_recommend_quit, # TODO 推荐离职,暂时还保留; 可能以后会没有用
        (CHECK_STATUS_RECOMMEND_QUIT, EVENT_HM_DECIDE_QUIT): _ban,

        (CHECK_STATUS_ELIMINATED, EVENT_HM_DECIDE_RETAIN): CHECK_STATUS_WORKING,
        (CHECK_STATUS_ELIMINATED, EVENT_HM_DECIDE_QUIT): CHECK_STATUS_RETAIN,  # ??? 留职待查 ???

        (CHECK_STATUS_RETAIN, EVENT_APPLY_RESIGN): CHECK_STATUS_RETAIN_RESIGN,

        (CHECK_STATUS_RETAIN_RESIGN, EVENT_HM_DECIDE_RETAIN): CHECK_STATUS_RETAIN,
        (CHECK_STATUS_RETAIN_RESIGN, EVENT_HM_DECIDE_QUIT): _quitting,

        (CHECK_STATUS_NO_FIRST_ORDER, EVENT_HM_DECIDE_QUIT): _quitting,  # _quitting 且 _ban
        (CHECK_STATUS_NO_FIRST_ORDER, EVENT_HM_DECIDE_RETAIN): CHECK_STATUS_BINDING_TEAM

    }










    # === 创建real_info记录的入口状态，事件 ===
    # === 如果需要修改real_info的初始状态， 修改if后面即可 ===
    # === real_info不会重复创建 ===
    # 兼职审核通过即建立real_info
    REAL_INFO_ENTRY_STATUS = [i for i in FSM.keys() if FSM[i] == CHECK_STATUS_PART_TIME_WORKING]
    # 申请的时候如果是选择全职，则跳过兼职申请全职，此时需要另一个real_info入口
    REAL_INFO_ENTRY_STATUS += [i for i in FSM.keys() if FSM[i] == CHECK_STATUS_APPLY_FULL_TIME]

    @classmethod
    def get_next_status(cls, current_status, condition, **kwargs):
        """
        获取下一状态
        @param current_status: 当前状态
        @param condition: 条件
        @return: 如果返回None表示错误状态或条件
        """
        state = cls.FSM.get((current_status, condition), None)
        return state if isinstance(state, int) else state(**kwargs)

    @classmethod
    def update_check_status(cls, obj, condition, current_status=None, **kwargs):
        """
        更新对象的状态
        @param obj: ApplyDeliver 或 RealInfo 对象
        @param current_status: 当前状态, 如果为None就拿obj的check_status字段
        @param condition: 配送员事件类型
        @param kwargs: 目前支持:
            executor_id: 操作人ID
            remark: 操作备注
        @return: obj 或 None, None表示出错
        """
        if current_status is None:
            current_status = obj.check_status
        if isinstance(obj, ApplyDeliver):
            # 如果传入了apply_deliver对象，尝试查找对应的real_info对象
            # 因为real_info会同步apply_deliver，如果有real_info，则优先更新real_info
            deliver_ri = RealInfo.get(user_id=obj.user_id)
            if deliver_ri:
                obj = deliver_ri
        next_status = cls.get_next_status(current_status, condition, **kw)

        # 日志
        # debug_str = "{user_id}: from {current_status} to {next_status}, conditon: {condition}".format(
        #     user_id=obj.user_id,
        #     current_status=current_status,
        #     next_status=next_status,
        #     condition=condition
        # )
        # GLogging.async_write_log(GLogging.REGISTER_LOGGER, debug_str)

        # 解绑该配送员
        if next_status in [DeliverFSM.CHECK_STATUS_BANNED, DeliverFSM.CHECK_STATUS_QUITED]:
            org_info = DeliverOrg.get(user_id=obj.user_id)
            if org_info:
                org_info.user_id = 0
                org_info.save()

        if next_status:
            # === 判断当前状态是否转换兼职为全职

            # === 判断当前操作是否为离职

            # === 判断当前操作是否为拉黑，拉黑除状态修改之外，还需要修改quit_time和banned字段

            # === 判断当前操作是否拒绝系统自动推荐离职，拒绝系统推荐离职的同时需要清理缓存

            # 更新状态
            from_status = obj.check_status
            obj.check_status = next_status
            obj.save(update_fields=['check_status'])

            # === 判断当前状态是否需要创建real_info记录
            for FSM_k in cls.REAL_INFO_ENTRY_STATUS:
                if from_status == FSM_k[0] and condition == FSM_k[1]:
                    cls.pass_deliver(obj.user_id)

            # 日志
            DeliverFSMLog.objects.create(
                user_id=obj.user_id,
                executor_id=kwargs.get('executor_id', 0),
                from_status=from_status,
                to_status=next_status,
                event=condition,
                remark=kwargs.get('remark', '')
            )
            # 进入分配中心处理
            # cls.dispatch_to_center(obj)
            return obj
        else:
            return None


    # @classmethod
    # def pass_deliver(cls, deliver_id):
    #     """
    #     生成real_info记录, 参照古老的pass_deliver
    #     :param deliver_id:
    #     :return:
    #     """
    #     app_id = 883
    #     apply_info = ApplyDeliver.get(user_id=deliver_id)
    #     user_id = apply_info.user_id
    #     image = DeliverImage.get(app_id=app_id, user__id=user_id)
    #     real_info = RealInfo.get(app_id=app_id, user__id=user_id, deleted=False)
    #     if not real_info:
    #         # 仅当real_info没有创建记录的时候才创建
    #         RealInfo.create(
    #             app_id=app_id,
    #             user_id=user_id,
    #             id_images=image.id_image if image else "",
    #             real_name=apply_info.name,
    #             gravatar=image.avatar if image else "",
    #             location=apply_info.location,
    #             city=apply_info.city,
    #             city_code=apply_info.city_code,
    #             province_code=apply_info.province_code,
    #             province=apply_info.province,
    #             district_code=apply_info.district_code,
    #             district=apply_info.district,
    #             check_status=apply_info.check_status,
    #             job_type=apply_info.job_type,
    #             deliver_category=apply_info.deliver_category
    #         )