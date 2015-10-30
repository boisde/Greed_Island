# -*- coding:utf-8 -*-
# 封装 sentry python 客户端

import traceback
import platform
from raven import Client
from tools_lib.host_info import *


class SentryClient(object):
    COMMON = 'common'
    APP_USER_CENTER = 'app_user_center'
    APP_ORDER = 'app_order'
    APP_MALL = 'app_mall'
    APP_FINANCE = 'app_finance'
    CORE_SHOP = 'core_shop'
    BL_INVITE = 'bl_invite'

    SENTRY_DSN = {
        COMMON: 'http://38940e713fbd40eba36e0611315777fc:200885cd27de438fb1e42a194f0aa290@123.57.74.248:9000/4',
        APP_USER_CENTER: 'http://8d86a03891fb47bbb078bbec2923d0ae:eb64adf43afc42588c2edf83727b34a8@123.57.74.248:9000/2',
        APP_ORDER: 'http://7db7e669b13e43daac64864eda81b113:69d935c7c6a649e29f467e4a74a59485@123.57.74.248:9000/6',
        APP_MALL: 'http://784a3cc7c4de49168e64239f98e012ca:f40a5a91185945e2957c530da164d7eb@123.57.74.248:9000/5',
        APP_FINANCE: 'http://5b8886e48d2d40e79bdc90c2fe5fc7f3:7bfe37bc7b2048019f34d6ebde30c18b@123.57.74.248:9000/7',
        CORE_SHOP: 'http://86d5be7098dc4d87a4bae7942eb7aad0:ff14b804483746128590e69929a4307f@123.57.74.248:9000/8',
        BL_INVITE: 'http://7ccfc923e6554d3286d20a7579e7e907:14b2eba6919f424db11ca5e2c8314e1a@123.57.74.248:9000/16',
    }

    __client_pool = {}

    @classmethod
    def get_client(cls, client_name=COMMON):
        if client_name not in cls.SENTRY_DSN.keys():
            raise Exception('no such client name: %s' % client_name)
        if client_name not in cls.__client_pool:
            cls.__client_pool[client_name] = Client(cls.SENTRY_DSN[client_name])
        return cls.__client_pool[client_name]

    @classmethod
    def send_message(cls, client_name=COMMON, message='', **kwargs):
        """
        发送消息
        @param client_name:
        @param message:
        @param kwargs:
        @return:
        """
        try:
            if platform.node() in (
                TEST_CORE_API_NODE, TEST_BL_SERVICE_NODE, TEST_BL_API_GATEWAY_NODE,
                ONLINE_AL_171_NODE, BL_SERVICE_NODE, BL_API_GATEWAY_NODE
            ):
                sentry_client = cls.get_client(client_name)
                sentry_client.captureMessage(message, **kwargs)
        except:
            print traceback.format_exc()


