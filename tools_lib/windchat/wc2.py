#coding=utf-8
__author__ = 'kk'
'''
WARNING!!!

注意：

风信SDK仅能在业务层、聚合层服务器调用。
涉及业务、聚合层的redis和队列配置。

如需在其他层调用，请复制本文件并修改redis和队列的配置文件！

'''

import platform
import requests
from tools_lib.gtz import TimeZone
from tools_lib.host_info import *
from tools_lib.rabbitmq_client import RabbitMqCtlV2, EXCHANGE_WINDCHAT

try:
    import simplejson as json
except:
    import json

try:
    import cPickle as pickle
except:
    import pickle

class WindChatMessageTooLong(Exception): pass
class BadTargetTypeException(Exception): pass

# 角色
ROLE_DELIVER = "DELIVER"    # 配送员
ROLE_CLIENT = "CLIENT"      # 客户

# 匿名客服ID
ANONYMOUS_STAFF_ID = "ANONYMOUS_STAFF"
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
    request_prefix = "http://" + BL_SERVICE_IP + ":9393"
    server_node = WIND_CHAT



class windchat_message(object):
    """
    base wind chat message

    message body for rabbitmq and http requests:

    pickled-object({
        "data":{                    // 风信消息实际数据
            "target_user_id":       // 配送员、客户ID
            "target_type":          // "DELIVER"配送员 "CLIENT"客户
            "message":              // 对话内容
            "target_name":          // 配送员、客户名
            "participator_id":      // 客服ID(如果这条消息是客服回复的)(传"ANONYMOUS_STAFF"使用匿名客服)
            "participator_name":    // 客服名
            "read_operator":        // 已读标记人ID
            "create_time":          // 创建时间utc
            "update_time":          // 更新时间utc
        },
        "with_push": true           // 是否推送给客户端(缺省推送)
        "with_push_to_dg": false    // 是否推送给帝国后台(缺省不推送)
    })
    """

    def __init__(self,
                 target_user_id,
                 target_type,
                 message,
                 target_name="",
                 participator_id=ANONYMOUS_STAFF_ID,
                 participator_name="",
                 read_operator=0,
                 create_time=None,
                 update_time=None
    ):
        # 为了检查长度
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

        if target_type not in ("DELIVER", "CLIENT"):
            # 检查target_type
            # target_type是直接丢进队列的，而队列消费者不会报任何错误，所以必须先处理问题
            raise BadTargetTypeException("bad target_type " + target_type)

        self.data = {}
        d = self.data
        d["target_user_id"] = target_user_id
        d["target_type"] = target_type
        d["message"] = message
        d["target_name"] = target_name
        d["participator_id"] = participator_id
        d["participator_name"] = participator_name
        d["read_operator"] = read_operator
        d["create_time"] = create_time
        d["update_time"] = update_time


    @staticmethod
    def pack_q_msg(data, with_push, with_push_to_dg):
        """
        包装rabbit mq(或者扔给接口)中的结构
        @param kwargs:
        @return:
        """
        # TODO 必须保持和windchat.utils.chat_utils中同名函数一样的返回
        return {
            "data": data,
            "with_push":with_push,
            "with_push_to_dg":with_push_to_dg
        }


    def send(self, with_push=True, with_push_to_dg=False):
        """
        通过rabbitmq异步发送(推荐)

        @param with_push: 是否推送
        @param with_push_to_dg: 是否推送给帝国
        """
        body = pickle.dumps(windchat_message.pack_q_msg(
            data=self.data,
            with_push=with_push,
            with_push_to_dg=with_push_to_dg
        ))
        RabbitMqCtlV2.basic_publish(exchange=EXCHANGE_WINDCHAT, body=body, server_node=server_node)


    def send_to_all(self, with_push=True):
        """
        发给全部人
        @param with_push:
        @return:
        """
        # TODO
        return


    def send_through_http(self, with_push=True, with_push_to_dg=False):
        """
        通过http同步发送(必须异步调用)

        @param with_push: 是否推送给客户端
        @param with_push_to_dg: 是否推送给帝国
        """
        requests.post(request_prefix + "/windchat/api/send_chat", data=pickle.dumps(windchat_message.pack_q_msg(
            data=self.data,
            with_push=with_push,
            with_push_to_dg=with_push_to_dg
        )), timeout=DEFAULT_TIMEOUT)


    def send_to_all_through_http(self, with_push=True):
        """
        通过http发送数据给所有人

        @param with_push: 是否推送给客户端
        """
        # TODO
        return



class plain_message(windchat_message):
    """
    发送普通消息
    """
    def __init__(self, **kwargs):
        super(plain_message,self).__init__(**kwargs)


class img(windchat_message):
    """
    发送图片
    """
    def __init__(self, url, **kwargs):
        self.data = kwargs
        self.data["message"] = "[img]%s[/img]" % url
        super(img, self).__init__(**self.data)



if node in [LOCALHOST_NODE, TEST_BL_SERVICE_NODE]:
    evaluation_prefix = "http://data.123feng.com:8885"
elif node in [BL_SERVICE_NODE]:
    evaluation_prefix = "http://www.123feng.com:8885"

class evaluation(windchat_message):
    """
    发送评价邀请
    """
    def __init__(self, deliver_name, deliver_id, date, **kwargs):
        """
        @:param num: 待评价数
        @:param date: 本地日期
        @:param client_id: 客户ID
        """
        self.data = kwargs
        self.data["message"] = json.dumps({
            "title": "请对%s的服务进行评价" % deliver_name,
            "date": TimeZone.date_to_str(date),
            "url": evaluation_prefix + \
                "/deliver-app/deliver-detail?owner_id={owner_id}&staff_id={deliver_id}&work_date={year}-{month}-{day}".format(
                    owner_id=kwargs["target_user_id"],
                    deliver_id=deliver_id,
                    year=date.year,
                    month=date.month,
                    day=date.day
            ),
            "content": "您{year}年{month}月{day}日的配送服务已完成，请对给您服务的风先生进行匿名评价".format(
                year=date.year,
                month=date.month,
                day=date.day
            )
        },ensure_ascii=False)
        self.data["message"] = "[evaluation]%s[/evaluation]" % self.data["message"]
        super(evaluation,self).__init__(**self.data)


class notice(windchat_message):
    """
    发通知
    """
    def __init__(self, title, content, **kwargs):
        """
        @:param to_user_id: 目标ID,
        @:param to_role: 目标角色(见最上)
        @:param title: 标题
        @:param content: 内容
        """
        self.data = kwargs
        self.data["message"] = json.dumps({
            "title":title,
            "content":content
        },ensure_ascii=False)
        self.data["message"] = "[notice]%s[/notice]" % self.data["message"]
        super(notice, self).__init__(**self.data)


class common_web_view_msg(windchat_message):
    """
    通用web view信息
    """
    def __init__(self, title, url, content="", datetime=None, **kwargs):
        """
        @param to_user_id: 目标ID,
        @param to_role: 目标角色(见最上)
        @param title: 标题
        @param content: 内容
        """
        if not datetime: datetime = TimeZone.utc_now()
        self.data = kwargs
        self.data["message"] = json.dumps({
            "create_time": TimeZone.datetime_to_str(datetime),
            "url": url,
            "content": content,
            "title": title
        },ensure_ascii=False)
        self.data["message"] = "[other]%s[/other]" % self.data["message"]
        super(common_web_view_msg, self).__init__(**self.data)




if __name__=="__main__":
    from datetime import date
    a=evaluation(num=3,date=date.today(),target_user_id=123,target_type="CLIENT")
    a.send()
    b=notice(target_user_id=123,target_type="DELIVER",title="t",content="c")
    b.send()
    c=common_web_view_msg(target_user_id=323, target_type="DELIVER", title="testgg",content="lala", url="http://qweasd")
    c.send()
