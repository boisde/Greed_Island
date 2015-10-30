# -*- coding:utf-8 -*-

import json
import requests
from requests.auth import HTTPBasicAuth
from tools_lib.gedis.core_redis_key import key_sms_rate_limit
from tools_lib.gedis.gedis import Redis
from tools_lib.common_utils import check_tel

SEND_REGCODE_TOO_MUCH = 1
SEND_REGCODE_SUCCESS = 2
SEND_REGCODE_FAIL = 3

SEND_REGCODE_URL = "https://sms-api.luosimao.com/v1/send.json"
REGCODE_PASSED = "ca904c8c3c081149eb546abd4fae5156"

MRWIND = "【风先生】"
# 同一手机号60秒只能发一次短信
LIMIT_SEC = 60

redis_client = Redis()


def send_sms(tel, msg):
    # 控制短信发送频率
    key = key_sms_rate_limit.format(tel=tel)
    if redis_client.exists(key):
        return False
    redis_client.set(key, 1, ex=LIMIT_SEC)

    # 检查手机号合法性
    if not check_tel(tel):
        print "phone number error %s" % tel
        return False
    msg = check_msg(msg)

    return _send_regcode(tel, msg)


def check_msg(msg):
    return msg if MRWIND in msg else " ".join([msg, MRWIND])


def _send_regcode(tel, msg):
    tel = str(tel)
    url = SEND_REGCODE_URL
    key = "api"
    passwd = REGCODE_PASSED
    data = {
        "mobile": tel,
        "message": msg
    }
    auth = HTTPBasicAuth(key, passwd)
    response = requests.post(url, data=data, auth=auth)
    result = json.loads(response.content)
    print result

    if str(result.get("error")) == str(0):
        return SEND_REGCODE_SUCCESS
    else:
        # 云片的接口作为备用，在发送短信前请确认已经在云片的后台中增加了短信模板
        print u'发送短信失败，调用云片接口发送短信'
        return _yunpian_send_sms(tels=tel, msg=msg)


# 云片网络的短信接口
yunpian_apikey = 'f2331bfd85886e65ed198209a87df829'
yunpian_request_url = 'http://yunpian.com/v1/sms/send.json'
yunpian_request_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
yunpian_response_code_ok = 0


def _yunpian_send_sms(tels, msg):
    if not isinstance(tels, list):
        tels = [tels]
    request_body_data = {
        'apikey': yunpian_apikey,
        'mobile': ','.join([str(tel) for tel in tels]),
        'text': str(msg)
    }
    response = requests.post(
        url=yunpian_request_url,
        headers=yunpian_request_headers,
        data=request_body_data
    )
    ret_msg = json.loads(response.content)
    if ret_msg.get('code') is yunpian_response_code_ok:
        return SEND_REGCODE_SUCCESS
    else:
        print msg
        print ret_msg.get('detail')
        return SEND_REGCODE_FAIL
