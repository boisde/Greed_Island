#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import copy
import datetime
from urllib import urlencode, quote
import traceback
import config as ac


def get_ecs_api_url(action, **kwargs):
    """

    """
    try:
        params = copy.copy(ac.params)
        # 基本参数
        params['Timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        # 操作参数
        params['Action'] = action  # 如 'DescribeInstanceStatus'
        params.update(kwargs)

        params, raw = params_filter(params)
        # 签名
        params['Signature'] = sign(ac.ALIYUN_ACCESS_KEY_SECRET + '&', raw)

        return ac.ECS_URI + urlencode(params)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return None


def params_filter(params):
    """
    对字典排序并剔除数组中的空值和签名参数
    :param params: 待排序的字典
    :return: 字典和字符串
    """
    ks = params.keys()
    ks.sort()
    new_params = dict()
    str_to_sign = 'GET&%2F&'
    canonical_str = ''
    for k in ks:
        v = params[k]
        # 对键进行编码
        k_quoted = quote(k, safe='')
        # 不签名sign和sign_type参数，并且参数值不为空
        if k not in ('Signature', '') and v:
            # 对值进行编码
            v_quoted = quote(v, safe='')
            new_params[k_quoted] = v_quoted
            canonical_str += '%s=%s&' % (k_quoted, v_quoted)
    # 剔除末尾的&
    canonical_str = canonical_str[:-1]
    # 编码以后, 再加上奇怪的头
    str_to_sign += quote(canonical_str, safe='')
    return params, str_to_sign


def sign(key, raw):
    """
    签名, 目前只支持HMAC-SHA1签名
    :param raw: 待签名的字符串
    :param key: 支付宝交易安全检验码
    :return: 签名后的字符串
    """
    from hashlib import sha1
    import hmac

    # print("SIGN (%s).........." % raw)
    hashed = hmac.new(str(key), raw, sha1)
    # The signature
    return hashed.digest().encode("base64").rstrip('\n')
