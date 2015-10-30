# -*- coding:utf-8 -*-

import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.status import *
from api_response import APIResponse


class MyJsonEncoder(json.JSONEncoder):
    """
    支持序列化 datetime 类型和 ObjectId 类型的 json writter 以及 OrderedDict 类型
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


encode_json = lambda i: json.dumps(i, cls=MyJsonEncoder)


class JsonResponse(HttpResponse):
    """
    格式为json的HttpResponse类
    """
    def __init__(self, status=APIResponse.SUCCESS, msg="", data={}, status_code=HTTP_200_OK):
        HttpResponse.__init__(self, encode_json(data), content_type='application/json', status=status_code)


class ErrorResponse(HttpResponse):
    """发生错误时，按要求返回错误信息"""

    def __init__(self, status=APIResponse.FAILED, msg="", data={}, status_code=HTTP_400_BAD_REQUEST):
        HttpResponse.__init__(self, msg, content_type='text/plain; charset=utf-8', status=status_code)


class RedirectResponse(HttpResponseRedirect):
    """
    重定向
    """
    def __init__(self, redirect_to=None):
        if redirect_to is not None:
            HttpResponseRedirect.__init__(self, redirect_to=redirect_to)
        else:
            HttpResponse.__init__(self, content='redirect url is None', status=HTTP_400_BAD_REQUEST)


class CompatibleJsonResponse(HttpResponse):
    """格式为json的HttpResponse类"""

    def __init__(self, obj=None, status=HTTP_200_OK):
        if obj is None and status == HTTP_200_OK:
            status = HTTP_204_NO_CONTENT
        HttpResponse.__init__(self, encode_json(obj), mimetype='application/json', status=status)
