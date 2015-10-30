#!/usr/bin/env python
# coding:utf-8
import logging
import threading

from threading import Timer
from tools_lib.transwarp.web import Dict
from tools_lib.transwarp.db import with_transaction
from tools_lib.transwarp.tz import utc_8_now
from logics import HotOrderLogic, OrderStateLogic

shared = Dict()
lock = threading.RLock()


class FSM(object):
    """
    Model logic for XXX.
    """

    # (1)清线程空间里的该任务: shared.tasks.remove(task_uuid), (2)结束后写DB添加ERR-TIMEOUT事件和更新状态
    @staticmethod
    def timer_job(job_task_id, job_task_uuid, job_to):
        try:
            lock.acquire()
            global shared
            shared.pop(job_task_uuid)  # 确保重复的uuid,DB里面的状态只变更一次.
        finally:
            lock.release()
        logging.info("I'm changing DB[%s, %s] to [TIMEOUT-ERR]..." % (job_task_uuid, utc_8_now()))
        FSM.write_db(job_task_id, utc_8_now(), 'TIMEOUT-ERR', 'TIMEOUT after [%s] minutes.' % job_to)
        logging.info("--[Timer]My Thread--: %s, shared: %s" % (threading.current_thread(), shared))
        logging.info("--[Timer]Active threads count--: %s" % threading.active_count())

    # STARTED: 开始一个定时器; 丢进线程共享内存.
    @staticmethod
    def started(s_task_id, policy_name, s_task_uuid, s_start_time, s_state, to):
        try:
            lock.acquire()
            global shared
            # 判断同UUID的任务是否已经存在
            if s_task_uuid in shared:
                err_msg = "Same UUID=[%s] for policy[%s] with id=[%s] has already been started." % (
                    s_task_uuid, policy_name, s_task_id
                )
                logging.info(err_msg)
                raise ValueError("Same UUID=[%s] for policy[%s] with id=[%s] has already been started." % (
                    s_task_uuid, policy_name, s_task_id
                ))
            # 创建一个定时器, hook到失败后的任务函数
            t = Timer(to*60, FSM.timer_job, args=[s_task_id, s_task_uuid, to])
            # 丢定时器对象指针和任务相关信息到线程共享内存
            shared[s_task_uuid] = {"task_id": s_task_id, "start_time": s_start_time, "timer": t}
        finally:
            lock.release()
        # 开启定时器
        t.start()
        logging.info("Timer: %s will timeout after [%s] minutes." % (t, to))
        # 写DB
        FSM.write_db(s_task_id, s_start_time, s_state, "STARTED")
        logging.info("--[STARTED]My Thread--: %s, shared: %s" % (threading.current_thread(), shared))
        logging.info("--[STARTED]Active threads count--: %s" % threading.active_count())

    # OK/ERR: cancel()一个定时器线程; 从线程共享内存里面去掉.
    @staticmethod
    def ended(o_task_id, o_task_uuid, o_start_time, o_state, o_info=None):
        try:
            task_timer = shared[o_task_uuid]["timer"]  # 如果没有发STARTED/已经超时, task_timer就是None
        except KeyError:
            raise ValueError("任务[%s](uuid=[%s])没有发送过启动信息或者该任务已经超时." % (o_task_id, o_task_uuid))
        task_timer.cancel()
        # task_timer.join()  # 不去阻塞main thread来等timer线程死掉,只要定时器里面的函数不执行就行.
        try:
            lock.acquire()
            shared.pop(o_task_uuid)
        finally:
            lock.release()
        # 写DB
        FSM.write_db(o_task_id, o_start_time, o_state, o_info)
        logging.info("--[OK/ERR]My Thread--: %s, shared: %s" % (threading.current_thread(), shared))
        logging.info("--[OK/ERR]Active threads count--: %s" % threading.active_count())

    # RESET: 确保清空shared(可能会有残余的timer线程,到期执行以后会无法pop而报错,不会损坏DB数据); 将DB任务state全体update成'今日未启动'.
    @staticmethod
    def reset(r_state):
        all_policy = HotOrderLogic.find_by("id", "", "limit 0,1000")
        # 写DB
        for policy in all_policy:
            FSM.write_db(policy, utc_8_now(), r_state, "RESET")
        try:
            lock.acquire()
            global shared
            shared.clear()
        finally:
            lock.release()

    # 写DB, (1)添加状态变更事件,用于历史查询. (2)更新任务state.
    @staticmethod
    @with_transaction
    def write_db(w_task_id, state_change_time, fin_state, state_info=None):
        # RESET:今日尚未启动 STARTED:已启动 OK:运行成功 RUNTIME-ERR:运行错误 TIMEOUT-ERR:运行超时
        p = HotOrderLogic.find_by('id, policy_name', 'where id=?', '', w_task_id)
        OrderStateLogic.create(**dict(policy_task_id=w_task_id, policy_name=p[0].policy_name,
                                     state_change_time=state_change_time, state=fin_state,
                                     state_info=state_info))
        HotOrderLogic.update(w_task_id, **dict(state=fin_state))

    @classmethod
    def update_state(cls, **kw):
        policy_id, state = int(kw.get("task_id", 0)), str(kw.get("state", "")).upper()
        task_uuid, to, info = str(kw.get("task_uuid","")), float(kw.get("to_minute", .0)), str(kw.get("info", ""))

        logging.info("--[ENTRY]Active threads count--: %s" % threading.active_count())
        start_time = utc_8_now()
        to = to if 0 < to < 31 else 5  # 默认5分钟超时
        # 简单判断policy_id是否存在
        _p = HotOrderLogic.find_by('id, policy_name', 'where id=?', '', policy_id)
        if not _p and state != "RESET":
            raise AttributeError("Policy with id=[{}] not found.".format(policy_id))

        # 根据想要更新的状态判断逻辑
        fp = {
            'STARTED': lambda x: cls.started(policy_id, _p[0].policy_name, task_uuid, start_time, x, to),
            'OK': lambda x: cls.ended(policy_id, task_uuid, start_time, x, o_info='OK'),
            'ERR': lambda x: cls.ended(policy_id, task_uuid, start_time, 'RUNTIME-ERR', info),
            'RESET': lambda x: cls.reset(x)
        }
        fp[state](state)