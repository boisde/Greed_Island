#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-09-07 15:19:48
# @Author  : Jim Zhang (jim.zoumo@gmail.com)
# @Github  : https://github.com/zoumo

import ujson as json
from schema import Schema, Or, SchemaError
from tornado import httpclient
from tornado.web import RequestHandler
from tornado.web import gen
from concurrent.futures import ThreadPoolExecutor
from tools_lib.core_api import CoreAPIStaff, CoreAPIShop
from ..http_code import (is_success,
                         HTTP_200_OK, HTTP_204_NO_CONTENT,
                         HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_403_FORBIDDEN,
                         HTTP_500_INTERNAL_SERVER_ERROR, HTTP_599_LOGIC_RESPONSE_FAILED
                         )
from . import async_requests

STR_OR_UNICODE = Or(str, unicode)
executor = ThreadPoolExecutor(8)


class BaseRequestHandler(RequestHandler):

    def options(self):
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        # self.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        pass

    def write_response(self, content=None, error_code=0, message="", status_code=HTTP_200_OK, reason=None):
        self.set_status(status_code, reason=reason)
        if status_code != HTTP_204_NO_CONTENT:
            # 如果是204的返回, http的标准是不能有body, 所以tornado的httpclient接收的时候会
            # 报错变成599错误
            self.write(dict(error_code=error_code, message=message, content=content))

    def write_error_response(self, content=None, error_code=103, message="UnknownError",
                             status_code=HTTP_400_BAD_REQUEST, reason=None):
        """
        错误响应
        :param error_code:
        :param message:
        :param status_code:
        :param content:
        :param reason:
        :return:
        """
        self.clear()
        if status_code == HTTP_422_UNPROCESSABLE_ENTITY and not reason:
            reason = message
        self.write_response(content=content, error_code=error_code, message=message,
                            status_code=status_code, reason=reason)

    def write_no_content_response(self):
        self.set_status(HTTP_204_NO_CONTENT)

    def write_not_found_entity_response(self, content=None):
        """
        查询id没有结果
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=101, message="NotFoundEntityError",
                                  status_code=HTTP_400_BAD_REQUEST)

    def write_multiple_results_found_response(self, content=None):
        """
        查询获取单个数据时，找到不止一个
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=102, message="MultipleResultsFound",
                                  status_code=HTTP_400_BAD_REQUEST)

    def write_unknown_error_response(self, content=None):
        """
        创建中的错误
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=103, message="UnknownError",
                                  status_code=HTTP_422_UNPROCESSABLE_ENTITY, reason="UNPROCESSABLE_ENTITY")

    def write_parse_args_failed_response(self, content=None):
        """
        参数解析错误
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=104, message="args parse failed",
                                  status_code=HTTP_400_BAD_REQUEST)

    def write_duplicate_entry(self, content=None):
        """
        插入操作，重复键值
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=1062, message="Duplicate entry",
                                  status_code=HTTP_500_INTERNAL_SERVER_ERROR, reason="Duplicate entry")

    def write_logic_error_response(self, content=None):
        """
        逻辑层返回错误
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=106, message="LogicResponseFailed",
                                  status_code=HTTP_422_UNPROCESSABLE_ENTITY, reason="logic response failed")

    def write_forbidden_response(self, content=None):
        """
        被禁止
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=107, message="Forbidden",
                                  status_code=HTTP_403_FORBIDDEN)

    def write_refund_money_error(self, content=None):
        """
        退款失败
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=108, message="RefundMoneyFailed",
                                  status_code=HTTP_422_UNPROCESSABLE_ENTITY, reason="RefundMoneyFailed")

    def write_cost_money_error(self, content=None):
        """
        扣款失败
        :param content:
        :return:
        """
        self.write_error_response(content=content, error_code=109, message="CostMoneyFailed",
                                  status_code=HTTP_422_UNPROCESSABLE_ENTITY, reason="RefundMoneyFailed")

    def set_headers(self, headers):
        if headers:
            for header in headers:
                self.set_header(header, headers[header])

    def get_token(self):
        try:
            token = self.request.headers.get("Authorization").split(' ')[1]
            return token
        except Exception:
            self.write_forbidden_response("Can't get token")
            return False

    @gen.coroutine
    def redirect_post(self, url, data=None, auto_write=True, **kwargs):
        response = yield async_requests.post(url, data=data, **kwargs)
        ret = self._handle_response(response)
        if auto_write:
            self.write_response(*ret)
        raise gen.Return(ret)

    @gen.coroutine
    def redirect_get(self, url, params=None, auto_write=True, **kwargs):
        response = yield async_requests.get(url, params=params, **kwargs)
        ret = self._handle_response(response)
        if auto_write:
            self.write_response(*ret)
        raise gen.Return(ret)

    @gen.coroutine
    def redirect_patch(self, url, data=None, auto_write=True, **kwargs):
        response = yield async_requests.patch(url, data=data, **kwargs)
        ret = self._handle_response(response)
        if auto_write:
            self.write_response(*ret)
        raise gen.Return(ret)

    @gen.coroutine
    def redirect_put(self, url, data=None, auto_write=True, **kwargs):
        response = yield async_requests.put(url, data=data, **kwargs)
        ret = self._handle_response(response)
        if auto_write:
            self.write_response(*ret)
        raise gen.Return(ret)

    def _handle_response(self, response):
        content, error_code, message = None, 0, ""
        if response.body:
            try:
                body = json.loads(response.body)
                content, error_code, message = body['content'], body['error_code'], body['message']
            except Exception:
                content, error_code, message = response.body, 500, "服务器开了会小差"
        code, reason = response.code, response.reason

        # copy headers
        for key in response.headers:
            if key in ('Date', 'Content-Length', 'Content-Type', 'Server'):
                continue
            self.add_header(key, response.headers[key])

        return (content, error_code, message, code, reason)


class AGRequestHandler(BaseRequestHandler):
    asyncHTTPClient = httpclient.AsyncHTTPClient()

    def write_ag_response(self, code, body, headers=None):
        # 写入请求头
        self.set_headers(headers)

        if code == HTTP_204_NO_CONTENT:
            self.write_response(status_code=HTTP_204_NO_CONTENT)
            return True
        if is_success(code):
            rst, data = self.parse_response_content(body)
            if rst is True:
                self.write_response(status_code=code, content=data['content'], message=data['message'])
                return True
            else:
                self.write_parse_args_failed_response(data)
                return None
        elif code == HTTP_599_LOGIC_RESPONSE_FAILED:
            self.write_logic_error_response(body)
            return None
        else:
            parse_rst, parse_data = self.parse_response_content(body)
            if parse_rst is True:
                self.write_error_response(
                    error_code=body['error_code'], message=body['message'], status_code=code, content=body['content']
                )
                return None
            else:
                self.write_parse_args_failed_response(parse_data)
                return None

    def return_ag_response_values(self, code, body, headers=None):
        """
        解析请求返回的信息，并返回数据，常用于错误信息返回（不使用headers）
        :param code:
        :param body:
        :return:
        """
        if headers is not None:
            for i in ["X-Resource-Count"]:
                self.set_header(i, headers.get(i, ""))
            # for header in headers:
            #     self.add_header(header, headers[header])

        if code == HTTP_204_NO_CONTENT:
            self.write_response(status_code=HTTP_204_NO_CONTENT)
            return None
        elif is_success(code):
            rst, data = self.parse_response_content(body)
            if rst is True:
                return data
            else:
                self.write_parse_args_failed_response(data)
                return None
        elif code == HTTP_599_LOGIC_RESPONSE_FAILED:
            self.write_logic_error_response(body)
            return None
        else:
            parse_rst, parse_data = self.parse_response_content(body)
            if parse_rst is True:
                self.write_error_response(
                    error_code=body['error_code'], message=body['message'], status_code=code, content=body['content']
                )
                return None
            else:
                self.write_logic_error_response(parse_data)
                return None

    @gen.coroutine
    def get_response(self, request):
        """
        异步，获取单个request请求
        :param request: tornado.httpclient.HTTPRequest
        :return:
        """
        try:
            # response = yield httpclient.AsyncHTTPClient().fetch(request)
            response = yield self.asyncHTTPClient.fetch(request)
            code = response.code
            headers = response.headers
            headers.pop('Content-Length')
            if response.error:
                code, body = [HTTP_599_LOGIC_RESPONSE_FAILED, response.error.message]
            elif response.body:
                # print response.body
                body = json.loads(response.body)
            else:
                body = None
        except httpclient.HTTPError as http:
            # 失败请求4xx, 5xx
            code = http.code
            headers = None
            if http.response is None:
                body = http.message
            else:
                body = json.loads(http.response.body)

        raise gen.Return([code, body, headers])

    @gen.coroutine
    def get_response_list(self, request_list):
        """
        异步，获取列表中的request请求
        :param request_list: [tornado.httpclient.HTTPRequest, ...]
        :return:
        """
        # http_client = httpclient.AsyncHTTPClient()
        response_list = yield [self.asyncHTTPClient.fetch(request) for request in request_list]
        raise gen.Return(response_list)

    @gen.coroutine
    def get_response_dict(self, request_dict):
        """
        异步，获取字典中的request请求
        :param request_dict: {"key": tornado.httpclient.HTTPRequest, ...}
        :return:
        """
        # http_client = httpclient.AsyncHTTPClient()
        response_dict = yield {key: self.asyncHTTPClient.fetch(value) for key, value in request_dict.items()}
        raise gen.Return(response_dict)

    @staticmethod
    def parse_response_content(response_body):
        """
        解析返回内容
        :param response_body:
        :return:
        """
        try:
            data = Schema({
                "content": Or(dict, None, STR_OR_UNICODE, list),
                "message": STR_OR_UNICODE,
                "error_code": int
            }).validate(response_body)
        except SchemaError as e:
            return False, e.message
        else:
            return True, data

    @gen.coroutine
    def get_deliver_id_from_token(self):
        """
        根据token获取风先生id
        :return:
        """
        try:
            token = self.request.headers.get("Authorization").split(' ')[1]
            user_id = yield executor.submit(CoreAPIStaff.get_user_id_from_token, token=token)
        except Exception as e:
            self.write_forbidden_response("Can't get token")
            raise gen.Return(None)
        else:
            raise gen.Return(user_id)

    @gen.coroutine
    def get_deliver_info_from_staff_id(self, staff_id):
        """
        通过 staff_id 获取配送员信息
        :return:
        """
        info = yield executor.submit(CoreAPIStaff.get_staff_info, staff_id)
        raise gen.Return(info)

    @gen.coroutine
    def get_shop_owner_id_from_token(self):
        """
        根据 token 获取 商户所有人id
        :return:
        """
        try:
            token = self.request.headers.get("Authorization").split(' ')[1]
            user_id = yield executor.submit(CoreAPIShop.get_user_id_from_token, token=token)
            # print user_id, "<<<<<<<<<<<<<<<<"
        except Exception:
            # self.write_forbidden_response("Can't get token")
            raise gen.Return(None)
        else:
            raise gen.Return(user_id)

    @gen.coroutine
    def get_shop_id_list_from_user_id(self, user_id):
        """
        根据user_id获取拥有的商户id列表
        :param user_id:
        :return:
        """
        try:
            shop_info = yield executor.submit(CoreAPIShop.get_shop_detail_info, data=dict(shop_owner_ids=user_id))
            shop_info = [shop['id'] for shop in shop_info]
            # print ">>>>>>>>>>>>>>>>>>>>", shop_info
        except Exception:
            raise gen.Return(None)
        else:
            raise gen.Return(shop_info)

    @gen.coroutine
    def get_shop_info_from_token(self):
        """
        从token获取 user_id(shop_owner_id商户所有人id) 和 shop_id_list(拥有的商户id列表)
        :return:
        """
        # 验证token和user_id
        user_id = yield self.get_shop_owner_id_from_token()
        if not user_id:
            self.write_forbidden_response("wrong token")
            raise gen.Return([None, None])
        # 验证商户信息
        shop_id_list = yield self.get_shop_id_list_from_user_id(user_id)
        # print shop_id_list
        if not shop_id_list:
            self.write_forbidden_response("no shop for user:{}".format(user_id))
            raise gen.Return([user_id, None])
        raise gen.Return([user_id, shop_id_list])

    def get_query_args(self):
        """
        获取query_arguments，只取值列表最后一个
        :return:
        """
        return {key: value[-1] for key, value in self.request.query_arguments.iteritems()}

    @gen.coroutine
    def check_staff(self, staff_id=None):
        """
        检查配送员信息
        :param staff_id: 与获取到的user_id做对比
        :return:
        """
        user_id = yield self.get_deliver_id_from_token()
        if not user_id:
            self.write_forbidden_response("wrong token")
            raise gen.Return(False)

        if staff_id:
            # arguments = self.get_query_args()
            if str(user_id) != str(staff_id):
                self.write_forbidden_response("wrong token got user_id not in args")
                raise gen.Return(False)

        raise gen.Return(user_id)

    @gen.coroutine
    def check_shop(self, shop_id):
        user_id, shop_id_list = yield self.get_shop_info_from_token()
        if user_id is None or shop_id_list is None:
            raise gen.Return(False)
        if shop_id not in shop_id_list:
            # app_log.error("user_id:{}, shop_info:{}, args:{}".format(user_id, shop_id_list, arguments))
            self.write_forbidden_response()
            raise gen.Return(False)

        raise gen.Return(True)
