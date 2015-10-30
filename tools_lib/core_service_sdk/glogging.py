# -*- coding:utf-8 -*-

try:
    import cPickle as pickle
except:
    import pickle
import json
import traceback
import platform
from tools_lib.host_info import *
from tools_lib.rabbitmq_client import RabbitMqCtlV2, EXCHANGE_LOGGING, BINDING_KEY_API


class Client(object):
    node = platform.node()

    @classmethod
    def get_server_node(cls):
        if cls.node in (ONLINE_AL_171_NODE, BL_SERVICE_NODE, BL_API_GATEWAY_NODE, ONLINE_AL_147_NODE):
            return LOGGING
        return TEST_LOGGING

    @classmethod
    def push(cls, data):
        """
        推送数据
        @param data:
            {
                "type": 1,
                "data": {}
            }
        @return:
        """
        try:
            RabbitMqCtlV2.basic_publish(
                exchange=EXCHANGE_LOGGING,
                body=pickle.dumps(data),
                server_node=cls.get_server_node()
            )
        except:
            print traceback.format_exc()


class APILogClient(Client):
    @classmethod
    def get_server_node(cls):
        if cls.node in (ONLINE_AL_171_NODE, BL_SERVICE_NODE, BL_API_GATEWAY_NODE, ONLINE_AL_147_NODE, LOCAL_SGY_NODE):
            return LOGGING_CENTER
        return TEST_LOGGING_CENTER

    @classmethod
    def push(cls, data):
        """
        推送数据
        @param data:
            {
                "ip": "192.168.1.1",
                "create_time": "2015-08-08T12:22:22Z",
                "user_id": 7740959,
                "type": 1,
                "url": "/xxx/xxxxx/xxx",
                "method": "get",
                "params": {}
            }
        @return:
        """
        try:
            RabbitMqCtlV2.basic_publish(
                exchange=EXCHANGE_LOGGING,
                routing_key=BINDING_KEY_API,
                body=json.dumps(data),
                server_node=cls.get_server_node()
            )
        except:
            print traceback.format_exc()

