#coding=utf-8
__author__ = 'kk'
'''

WindChat v3 SDK

注意：

风信SDK仅能在业务层、聚合层服务器调用。
涉及业务、聚合层的redis和队列配置。

如需在其他层调用，请复制本文件并修改redis和队列的配置文件！

'''
import json
import platform
import requests
from tools_lib.host_info import *
from tools_lib.rabbitmq_client import RabbitMqCtlV2, EXCHANGE_WINDCHAT3
from logging import info, warn, error

class WindChatMessageTooLong(Exception): pass
class BadTalkerTypeException(Exception): pass
class BadTalkersType(Exception): pass

# 拼好了的exchange
EXCHANGE_WINDCHAT = EXCHANGE_WINDCHAT3 + PROD_AG_PORT

# 角色
ROLE_DELIVER = "DELIVER"    # 配送员
ROLE_CLIENT = "CLIENT"      # 客户

# 匿名客服ID
ANONYMOUS_STAFF_ID = "ANONYMOUS_STAFF"

# 默认系统消息频道ID
DEFAULT_INFO_CHANNEL_ID = 77

# = 风信类型 =
# 纯文本风信
PLAIN_TEXT_TYPE = 1
# 图片
IMAGE_TYPE = 2
# 稿件
POST_TYPE = 5


# 风信对话内容长度
WINDCHAT_MSG_MAX_LENGTH = 256

# http请求默认超时s
DEFAULT_TIMEOUT = 3

# 当前机器的hostname
node = platform.node()
# 选择当前机器对应的请求机器
if node in [LOCALHOST_NODE, TEST_BL_SERVICE_NODE]:
    q_node = TEST_BL_SERVICE_NODE
    request_prefix = "http://" + TEST_BL_SERVICE_IP + ":9393"
    server_node = TEST_WIND_CHAT

else:
    q_node = BL_SERVICE_NODE
    request_prefix = "http://" + BL_SERVICE_IP + ":5555"
    server_node = WIND_CHAT
    # TODO 端口

'''

    message body for rabbit mq and http requests:

    JSON({
        "data":[
            {windchat-object},...
        ]
        "with_push": true                           // 是否推送给客户端(缺省推送)
        "with_push_to_dg": false                    // 是否推送给帝国后台(缺省不推送)
        "talkers": [7766532, ...]                   // 仅替换user_id重复发送列表中的数据(原windchat_message.talker_id不会发送)
        "appendage": {                              // 附加信息（内部使用）
            "cover": "客户端频道列表右侧的图像url"
        }
    })


    {windchat-object} :

    {
        "channel_id":           // 频道ID
        "talker_id":            // 用户ID
        "talker_type":          // "DELIVER"配送员 "CLIENT"客户
        "participator_id":      // 客服ID，缺省为匿名客服
        "message":              // 对话内容
        "message_type":         // 内容类型 1普通文本
        "talker_name":          // 配送员、客户名
    }

'''

class windchat_message(object):
    """
    风信消息包装器
    """

    def __init__(self,
                 channel_id,
                 talker_id,
                 talker_type,
                 message,
                 message_type=PLAIN_TEXT_TYPE,
                 participator_id=ANONYMOUS_STAFF_ID,
                 talker_name=""
    ):
        # 检查长度
        if isinstance(message, unicode):
            test_s = message
        elif isinstance(message, str):
            try:
                test_s = message.decode("utf-8")
            except:
                raise UnicodeDecodeError("the message can't be decoded with utf-8.")
        else:
            raise TypeError("message should be a string or unicode.")

        print test_s

        if len(test_s) > WINDCHAT_MSG_MAX_LENGTH:
            raise WindChatMessageTooLong("length: %s" % len(message))

        if talker_type not in (ROLE_CLIENT, ROLE_DELIVER):
            # 检查talker_type
            # talker_type是直接丢进队列的，而队列消费者不会报任何错误，所以必须先处理问题
            raise BadTalkerTypeException("bad talker_type " + talker_type)

        if talker_type == ROLE_CLIENT:
            assert 0 # client not allowed

        self.data = {}
        d = self.data
        d["channel_id"] = channel_id
        d["talker_id"] = talker_id
        d["talker_type"] = talker_type
        d["talker_name"] =talker_name
        d["message"] = message
        d["message_type"] = message_type
        d["participator_id"] = participator_id

    def generate_dict(self):
        return self.data



class windchat_emitter(object):
    """
    风信发射器
    """
    def __init__(self,
        sample_or_list,
        with_push=True,
        with_push_to_dg=False,
        talkers=None,
        appendage=None
    ):

        self.ret = {}
        if isinstance(sample_or_list, windchat_message):
            self.ret["data"] = [sample_or_list.generate_dict()]
        elif isinstance(sample_or_list, list) and sample_or_list:
            self.ret["data"] = [i.generate_dict() for i in sample_or_list]
        else:
            raise Exception("not a sample or list")
        self.ret["with_push"] = with_push
        self.ret["with_push_to_dg"] = with_push_to_dg
        self.ret["appendage"] = appendage
        if talkers:
            # 判断是否要群发
            if not isinstance(talkers, list):
                raise BadTalkersType
            self.ret["talkers"] = talkers


    def send(self):
        """
        通过rabbit mq异步发送(推荐)
        """
        body = json.dumps(self.ret, ensure_ascii=False)
        info(body)
        RabbitMqCtlV2.basic_publish(exchange=EXCHANGE_WINDCHAT, body=body, server_node=server_node)


    def send_through_http(self):
        """
        通过http同步发送
        """
        requests.post(
            request_prefix + "/windchat/talker_tier/api/message",
            data=json.dumps(self.ret, ensure_ascii=False),
            timeout=DEFAULT_TIMEOUT
        )


def send_plain_text_to_delivers_shortcut(talker_id_list, message_text):
    """
    批量给配送员发送普通文本
    :param talker_id_list: 配送员ID列表
    :param message_text: 消息文本，<=256字
    :return:
    """
    windchat_emitter(
        windchat_message(
            channel_id=DEFAULT_INFO_CHANNEL_ID,
            talker_id=1,
            talker_type=ROLE_DELIVER,
            message=message_text
        ),
        talkers=talker_id_list
    ).send()


def send_image_to_delivers_shortcut(talker_id_list, image_url):
    """
    批量给配送员发送图片
    :param talker_id_list: 配送员ID列表
    :param message_text: URL，<=256字
    :return:
    """
    windchat_emitter(
        windchat_message(
            channel_id=DEFAULT_INFO_CHANNEL_ID,
            talker_id=2,
            talker_type=ROLE_DELIVER,
            message=image_url
        ),
        talkers=talker_id_list
    ).send()


def send_post_to_delivers_shortcut(talker_id_list, title, url, thumbnail, cover=""):
    """
    批量给配送员发送稿件
    :param talker_id_list: 配送员ID列表
    :param title: 标题
    :param url: 链接
    :param thumbnail: 缩略语
    :param cover: 题图
    :return:
    """
    windchat_emitter(
        windchat_message(
            channel_id=DEFAULT_INFO_CHANNEL_ID,
            talker_id=1,
            talker_type=ROLE_DELIVER,
            message=json.dumps({
                "title":title,
                "url":url,
                "thumbnail": thumbnail,
                "cover":cover
            },ensure_ascii=False)
        ),
        talkers=talker_id_list
    ).send()




if __name__=="__main__":
    # 测rabbitmq
    s = []
    s.append(windchat_message(channel_id=DEFAULT_INFO_CHANNEL_ID, talker_id=7792651, talker_type="DELIVER", message="测ut"))
    s.append(windchat_message(channel_id=DEFAULT_INFO_CHANNEL_ID, talker_id=7792615, talker_type="DELIVER", message="测ut haha"))
    windchat_emitter(s).send()
    s = []
    s.append(windchat_message(channel_id=DEFAULT_INFO_CHANNEL_ID, talker_id=999, talker_type="DELIVER", message="测ut2333"))
    windchat_emitter(s, talkers=[7792615,7792612,7792651]).send()
    # 测http
    # TODO