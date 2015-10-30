# -*- coding:utf-8 -*-

class APIResponse(object):
    SUCCESS = "SUCCESS"
    FAILED = "FALIED"

    @classmethod
    def create_response_content(cls, status=SUCCESS, msg="", data={}):
        """
        创建HTTP通信返回的数据结构
        @param status: 通信状态 SUCCESS/FALIED
        @param msg: 错误信息
        @param data: 数据
        @return: dict
        """
        if status not in (cls.SUCCESS, cls.FAILED):
            raise Exception('invalid status')
        return {
            "status": status,
            "message": msg,
            "data": data
        }
