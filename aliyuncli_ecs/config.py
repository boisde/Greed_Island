#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals

ECS_URI = 'https://ecs.aliyuncs.com/?'

ALIYUN_ACCESS_KEY_SECRET = 'x85FtYeQmOJr3QoB6Ss6TCvqn273zi'
ALIYUN_ACCESS_KEY_ID = 'LTAIDYCTJM81cxtl'
REGION = 'cn-beijing'

SIGN_TYPE = 'HMAC-SHA1'
VERSION = '2014-05-26'
FORMAT = 'json'
SIGNATURE_VERSION = '1.0'

params = {
    ##################################################
    #  基本参数
    'Format': 'json',
    'Version': '2014-05-26',
    'AccessKeyId': ALIYUN_ACCESS_KEY_ID,
    'SignatureMethod': SIGN_TYPE,
    'SignatureVersion': SIGNATURE_VERSION,

    # 'Timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    # 'SignatureNonce': 'randomly generated',
    # 'Signature': None,
    ##################################################
    # 操作参数
    "Action": 'DescribeInstanceStatus',
    "RegionId": REGION,
}


class Node(object):
    PYTHON_API = 'python-69'

    disk_ids = {
        PYTHON_API: 'd-254h1jttk',
    }
