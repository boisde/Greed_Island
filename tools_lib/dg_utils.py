#coding=utf-8
__author__ = 'kk'

import json
import traceback
import platform
import requests
from tools_lib.gedis.logic_gedis import Redis
from tools_lib.gedis.logic_redis_key import key_staff_info
from tools_lib.host_info import ONLINE_AL_147_NODE, ONLINE_AL_171_NODE, BL_SERVICE_NODE, TEST_BL_SERVICE_NODE


class HostUnknownException(Exception): pass

REDIS_EXPIRE_TIME = 60*60*12 # redis过期时间（秒）
redisc = Redis()
PLATFORM_NODE = platform.node()

if PLATFORM_NODE in (
        "localhost",
        "BOX-NEW",
        "CLOUD",
        "NEW-API",
        TEST_BL_SERVICE_NODE
):
    NODE_PREFIX = "http://10.0.0.246:8888"
    NODE_TIMEOUT = 9 # 超时时间（秒）
    persaved_token = "19aeb3b12092beba1cca1744b6175ca8"

elif PLATFORM_NODE in (
        ONLINE_AL_147_NODE,
        "iZ25cisdo69Z",  # 248
        ONLINE_AL_171_NODE,
        BL_SERVICE_NODE
):
    NODE_PREFIX = "http://10.170.203.30:8888"
    NODE_TIMEOUT = 3 # 超时时间（秒）
    persaved_token = "02720675976a53db40b828443f197a2f"

else:
    raise HostUnknownException("unknown hostname "+PLATFORM_NODE)



def get_staff_info(user_id = None, user_ids = None, term = "", department_id = 0, token = None):
    '''
    获取公司员工信息（包括配送经理、人事经理）
    :param user_id: 单个user_id, 优先使用这个参数
    :param user_ids: user_id列表
    :param term:姓名关键字
    :param department_id:部门ID，默认不搜索，如果搜索无部门人员，ID为0
    :param token: 请求该接口的token，当前用过期的token也没事
    :return:
    '''
    def save_redis(resp_json):
        try:
            for i in resp_json:
                redisc.set(key_staff_info.format(user_id = i["auth_id"]), json.dumps(i), ex = REDIS_EXPIRE_TIME)
        except:
            print "error occurs when saving to redis."

    def get_redis(user_id):
        return redisc.get(key_staff_info.format(user_id = user_id))

    if not token: token = persaved_token

    headers = {
        "Authorization": "token " + token
    }

    if user_id:
        try:
            # 单个获取，检查是否在redis缓存，是则直接返回
            redis_cache = get_redis(user_id)
            if redis_cache:
                # print "NOTICE: now extract staff info(%s) cache from redis." % user_id
                return json.loads(redis_cache)
        except:
            print "WARNING: error occurs when extract staff info(%s) from redis." % user_id

        if department_id:
            params = {
                "user_id" : str(user_id),
                "term": term,
                "department_id": department_id,
                "active":"true"
            }
        else:
            params = {
                "user_id" : str(user_id),
                "term": term,
                "active":"true"
            }
        resp_body_json = requests.get(
            NODE_PREFIX+"/nc/user",
            params = params,
            timeout = NODE_TIMEOUT,
            headers = headers
        ).json()
        save_redis(resp_body_json)
        if resp_body_json: return resp_body_json[0]

    elif user_id==0:
        return {}

    elif department_id:
        # 仅搜索某个部门的全部ID
        params = {
            "department_id": department_id
        }
        resp_body_json = requests.get(
            NODE_PREFIX+"/nc/user",
            params = params,
            timeout = NODE_TIMEOUT,
            headers = headers
        ).json()
        save_redis(resp_body_json)
        if resp_body_json: return resp_body_json


    else:
        # 批量获取的时候，就不检查redis缓存了。
        if not user_ids: # 兼容什么ID都不传为了获取所有信息的情况
            params = {
                "term": term,
                "active":"true"
            }
        else:
            params = {
                "user_ids": ",".join([str(i) for i in user_ids if i]),
                "term": term,
                "active":"true"
            }
        resp_body_json = requests.get(
            NODE_PREFIX+"/nc/user",
            params = params,
            timeout = NODE_TIMEOUT,
            headers = headers
        ).json()
        save_redis(resp_body_json)
        return resp_body_json


def get_user_id_from_token(token):
    """
    获取帝国用户的ID，wrapper
    :param token:
    :return:
    """
    from tools_lib.core_api import CoreAPIStaff
    return CoreAPIStaff.get_user_id_from_token(token=token)