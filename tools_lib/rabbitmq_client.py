# -*- coding:utf-8 -*-

import pika
import pika_pool
import platform
from tools_lib.host_info import *
try:
    import cPickle as pickle
except:
    import pickle

#####################################################
# exchange 名称
EXCHANGE_PUSH_MSG = 'push_msg'
EXCHANGE_SEND_SMS = 'send_sms'
EXCHANGE_POST_GPS = 'post_gps'
EXCHANGE_NEW_TOKEN = 'new_token'
EXCHANGE_REQUEST = 'request'
EXCHANGE_WINDCHAT = 'windchat'
EXCHANGE_WINDCHAT3 = 'windchat3'
EXCHANGE_LOGGING = 'logging'

#####################################################
# queue 名称
QUEUE_PUSH_MSG = 'q_push_msg'
QUEUE_SEND_SMS = 'q_send_sms'
QUEUE_POST_GPS = 'q_post_gps'
QUEUE_NEW_TOKEN = 'q_new_token'

#####################################################
# binding key
# API 调用统计
BINDING_KEY_API = 'bk_api'

#####################################################
# type 类型
# 广播
TYPE_FANOUT = 'fanout'
# 单播
TYPE_DIRECT = 'direct'
# 组播
TYPE_TOPIC = 'topic'


RABBITMQ_SERVER = {
    TEST_CORE_API_NODE: {
        "host": TEST_CORE_API_IP,
        "port": 5672,
    },
    TEST_BL_SERVICE_NODE: {
        "host": TEST_CORE_API_IP,
        "port": 5672,
    },
    LOCALHOST_NODE: {
        "host": TEST_CORE_API_IP,
        "port": 5672,
    },
    ONLINE_AL_171_NODE: {
        "host": ONLINE_AL_171_INNER_IP,
        "port": 5672,
    },
    BL_SERVICE_NODE: {
        "host": ONLINE_AL_171_INNER_IP,
        "port": 5672,
    },
    WIND_CHAT: {
        "host": PROD_BL_134_INNER_IP,
        "port": 5672
    },
    TEST_WIND_CHAT: {
        "host": TEST_BL_SERVICE_IP,
        "port": 5672
    },
    LOGGING: {
        "host": ONLINE_AL_171_INNER_IP,
        "port": 5672,
    },
    TEST_LOGGING: {
        "host": TEST_CORE_API_IP,
        "port": 5672,
    },
    LOGGING_CENTER: {
        "host": LOGGING_CENTER_INNER_IP,
        # "host": LOGGING_CENTER_OUTER_IP,
        "port": 5672,
    },
    LOCAL_SGY_NODE: {
        "host": TEST_CORE_API_IP,
        "port": 5672,
    },
}
node = platform.node()
if node not in RABBITMQ_SERVER.keys():
    node = LOCALHOST_NODE

class RabbitMqCtl(object):
    def __init__(self, exchange='', type='fanout', queue=''):
        """
        @param exchange:
        @param type:
        @return:
        """
        self.exchange = exchange
        self.type = type
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(**RABBITMQ_SERVER[node])
        )
        self.channel = self.connection.channel()
        if self.exchange != '':
            self.channel.exchange_declare(exchange=exchange, type=type)
        if queue != '':
            self.channel.queue_declare(queue=queue, durable=True)

    def __del__(self):
        """
        销毁对象实例时关闭连接
        @return:
        """
        self.connection.close()

    def basic_publish(self, exchange='', routing_key='', body=''):
        if exchange == '':
            exchange = self.exchange
        if routing_key == '':
            routing_key = QUEUE_PUSH_MSG
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,    # make message persistent
            )
        )

class RabbitMqCtlV2(object):
    """ 使用连接池 """
    __pool_dict = {}

    @classmethod
    def basic_publish(cls, exchange='', routing_key='', body='', server_node=None):
        """
        消息发送
        @param exchange:
        @param routing_key:
        @param body:
        @param server_node: 要连接到的rabbitmq服务器node
        @return:
        """
        if server_node is None:
            server_node = node
        if server_node not in cls.__pool_dict:
            cls.__pool_dict[server_node] = pika_pool.QueuedPool(
                create=lambda: pika.BlockingConnection(pika.ConnectionParameters(**RABBITMQ_SERVER[server_node])),
                max_size=10,
                max_overflow=10,
                timeout=5,
                recycle=3600,
                stale=60,
            )
        with cls.__pool_dict[server_node].acquire() as connection:
            connection.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,    # make message persistent
                )
            )


