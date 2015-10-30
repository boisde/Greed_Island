# coding: utf-8
__author__ = 'Qian Lei'

import json
from operator import concat
import platform

import requests

from tools_lib.host_info import *  # NOQA

# LOCALHOST_IP = '10.0.0.19'


class CoreAPI(object):
    """
    核心API调用类，核心层不同的模块分别继承该父类，每个模块的API都应该写成该类的一个方法供外部调用。
    """
    # 根据当前机器的主机名称确认目标主机
    node = platform.node()
    if node in [TEST_BL_SERVICE_NODE]:
        target = "test"
    elif node in [BL_SERVICE_NODE]:
        target = "online"
    elif node in [LOCAL_SGY_NODE]:
        target = 'online_outer'
        # target = 'localhost'
    else:
        target = "localhost"
    # 默认的协议
    Default_Http_Protocol = "http://"
    # 默认的接口端口
    Default_CoreAPI_Port = "5555"
    # 根据业务逻辑层的模块名判断应该使用哪台主机
    Hostname_Core_IP = {
        "shop": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", PROD_BL_CD_PORT]),
            "online_outer":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_OUTER_IP, ":", PROD_BL_CD_PORT]),
        },
        "slip": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", PROD_BL_CD_PORT])
        },
        "staff": {
            "localhost":
                # reduce(concat, [Default_Http_Protocol, '127.0.0.1', ":", '6002']),
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", PROD_BL_CD_PORT])
        },
        "account": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", PROD_BL_CD_PORT]),
            "online_outer":
                reduce(concat, [Default_Http_Protocol, '10.0.0.36', ":", '8001']),
        },
        "area": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", PROD_BL_CD_PORT])
        },
        "sms": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", PROD_BL_CD_PORT])
        },
        "gps": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                # gps没有测试服务器，暂时使用核心层
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_209_INNER_IP, ":", Default_CoreAPI_Port])
        },
        "empire": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", Default_CoreAPI_Port])
        },
        "log": {
            "localhost":
                reduce(concat, [Default_Http_Protocol, LOCALHOST_IP, ":", Default_CoreAPI_Port]),
            "test":
                reduce(concat, [Default_Http_Protocol, TEST_CORE_API_IP, ":", Default_CoreAPI_Port]),
            "online":
                reduce(concat, [Default_Http_Protocol, ONLINE_AL_171_INNER_IP, ":", Default_CoreAPI_Port]),
            "online_outer":
                reduce(concat, [Default_Http_Protocol, '10.0.0.19', ":", '8001']),
        },
    }
    # 要访问的模块名，需要在子类中重写
    Module_Name = ""
    # 要访问的核心API机器URL前缀，需要在子类中重写
    URL_Prefix = Hostname_Core_IP.get(Module_Name, {}).get(target)

    @classmethod
    def format_request_url(cls, relative_url):
        return concat(cls.URL_Prefix, relative_url)

    @staticmethod
    def get_request_info(request_url, request_method, request_data=None, headers=None, return_bool=False,
                         with_return_headers=False, request=None, error_info=None):

        # 3秒超时
        timeout_time = 3
        failed = False

        request_headers = {'Content-Type': "application/json"}
        if headers:
            request_headers = dict(request_headers.items() + headers.items())
        # 如果给了request，则提取token，不用手动生成带token的headers
        if request:
            request_headers["Authorization"] = request.META.get('HTTP_AUTHORIZATION', '')

        try:
            if request_method == "get":
                requests_info = requests.get(url=request_url, params=request_data, headers=request_headers,
                                             timeout=timeout_time)
            elif request_method == "post":
                requests_info = requests.post(url=request_url, data=json.dumps(request_data), headers=request_headers,
                                              timeout=timeout_time)
            elif request_method == "patch":
                requests_info = requests.patch(url=request_url, data=json.dumps(request_data), headers=request_headers,
                                               timeout=timeout_time)
            elif request_method == "delete":
                requests_info = requests.delete(url=request_url, data=json.dumps(request_data), headers=request_headers,
                                                timeout=timeout_time)
            elif request_method == "put":
                requests_info = requests.put(url=request_url, data=json.dumps(request_data), headers=request_headers,
                                             timeout=timeout_time)
            else:
                return failed
        except Exception, e:
            print e
            if isinstance(error_info, dict):
                error_info['code'] = 500
                error_info['msg'] = e
            return failed
        # 出现服务器错误
        if requests_info.status_code >= 400:
            print requests_info.content
            # 返回错误信息
            if isinstance(error_info, dict):
                error_info['msg'] = requests_info.content
                error_info['code'] = requests_info.status_code
            return failed
        # 成功调用，判断是否需要响应头
        # 如果不需要响应头，则直接返回数据
        # 如果需要响应头，则需要改变返回的数据结构
        if with_return_headers:
            return {"headers": dict(requests_info.headers), "data": True if return_bool else
                    json.loads(requests_info.content)}
        else:
            return True if return_bool else json.loads(requests_info.content)


class CoreAPIStaff(CoreAPI):
    """
    核心层Staff模块的API
    """
    Module_Name = "staff"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def batch_get_staff_info_given_org_and_info(cls, data):
        return cls.get_request_info(
            request_url=cls.format_request_url("/staff_join/org_info"), request_method="post", request_data=data
        )

    @classmethod
    def get_user_id_from_token(cls, request=None, token=None):
        """
        通过token获取配送员ID

        token: http headers里的Authorization的值，形如"uf2y4t894394g9p8ytyr89ryfb"
        request: django的request对象
        优先级：token -> request
        """
        if not request and not token:
            return 0
        elif request:
            auth = token
            if not auth:
                auth = request.META.get('HTTP_AUTHORIZATION')
            if not auth or 'token' not in auth:
                return 0
            token = auth.split(' ')[1]
        response_data = cls.get_request_info(
            request_url=cls.format_request_url("/staff/token/"+str(token)),
            request_method="get",
            request_data={"content": token},
        )
        return response_data.get("id", 0) if response_data is not False else 0

    @classmethod
    def get_user_ids_from_info(cls, kn, kv, is_not=False, page=1):
        if is_not:
            url_is_not = "1"
        else:
            url_is_not = "0"
        return cls.get_request_info(
            request_url=cls.format_request_url(
                "/staff_info/get_user_ids/"+str(kn)+"/"+str(kv)+"/"+str(url_is_not)+"/"+str(page)
            ),
            request_method="get",
            request_data={}
        )

    @classmethod
    def get_staff_info(cls, staff_id):
        return cls.get_request_info(
            request_url=cls.format_request_url("/staff_info/get_one/user/{staff_id}".format(staff_id=staff_id)),
            request_method="get",
            request_data={}
        )

    @classmethod
    def get_user_ids_from_org(cls, kn, kv, is_not=False, page=1):
        if is_not:
            url_is_not = "1"
        else:
            url_is_not = "0"
        return cls.get_request_info(
            request_url=cls.format_request_url(
                "/staff_org/get_user_ids/"+str(kn)+"/"+str(kv)+"/"+str(url_is_not)+"/"+str(page)
            ),
            request_method="get",
            request_data={}
        )


class CoreAPIShop(CoreAPI):
    """
    核心层商户模块的API
    """
    Module_Name = "shop"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def get_shop_info_from_shop_id(cls, shop_id):
        return cls.get_request_info(
            request_url=cls.format_request_url('/shops/'+str(shop_id)),
            request_method='get'
        )

    @classmethod
    def get_shop_brief_info(cls, data=None, error_info=None):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops/brief"),
            request_method="get",
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_shop_detail_info(cls, data=None, error_info=None):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops/detail"),
            request_method="get",
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_shops_in_city(cls, data, error_info=None):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops"),
            request_method="get",
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_user_id_from_token(cls, request=None, token=None, error_info=None):
        """
        通过token获取客户（商户）ID

        token: http headers里的Authorization的值，形如"uf2y4t894394g9p8ytyr89ryfb"
        request: django的request对象
        优先级：token -> request
        """
        if not request and not token:
            return 0
        elif request:
            auth = token
            if not auth:
                auth = request.META.get('HTTP_AUTHORIZATION')
            if not auth or 'token' not in auth:
                return 0
            token = auth.split(' ')[1]
        response_data = cls.get_request_info(
            request_url=cls.format_request_url("/shops/tokens"),
            request_method="get",
            request_data={"content": token},
            error_info=error_info
        )
        return response_data.get("id", 0) if response_data is not False else 0

    @classmethod
    def create_shop(cls, data, error_info=None):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops"),
            request_method="post",
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_shop_info_from_user_id(cls, user_id):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops/owner/"+str(user_id)), request_method="get"
        )

    @classmethod
    def update_shop_info(cls, shop_id, data):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops/"+str(shop_id)),
            request_method="put",
            request_data=data
        )

    @classmethod
    def shop_event(cls, shop_id, event_num):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops/"+str(shop_id)+"/events"),
            request_method="post",
            request_data={"event": int(event_num)},
        )

    @classmethod
    def tel_exist(cls, tel):
        rst = cls.get_request_info(
            request_url=cls.format_request_url("/shops/brief"),
            request_method="get",
            request_data={"tel": str(tel)}
        )
        if isinstance(rst, list) and len(rst) == 0:
            return False
        elif isinstance(rst, list) and len(rst) != 0:
            return True
        else:
            raise Exception("core api error")

    @classmethod
    def create_token(cls, shop_owner_id):
        return cls.get_request_info(
            request_url=cls.format_request_url("/shops/tokens"),
            request_method="post",
            request_data={"shop_owner_id": shop_owner_id}
        )


class CoreAPIAccount(CoreAPI):
    Module_Name = "account"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def get_accounts(cls, data=None, error_info=None):
        """ 批量查询账户信息 """
        return cls.get_request_info(
            request_url=cls.format_request_url("/accounts"),
            request_method='get',
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_one_account(cls, owner_id, data=None, error_info=None):
        """ 查询某人的账户信息 """
        if data is None:
            data = {'owner_ids': [owner_id]}
        else:
            data['owner_ids'] = [owner_id]
        rst = cls.get_request_info(
            request_url=cls.format_request_url("/accounts"),
            request_method='get',
            request_data=data,
            error_info=error_info
        )
        if rst is not False:
            if len(rst) is 0:
                rst = False
                if isinstance(error_info, dict):
                    error_info.update({'msg': '', 'code': 404})
            elif len(rst) > 1:
                rst = False
                if isinstance(error_info, dict):
                    error_info.update({'msg': 'more than one account', 'code': 409})
            else:
                rst = rst[0]
        return rst

    @classmethod
    def get_charge_records(cls, owner_id, data=None, error_info=None):
        """ 查询充值记录 """
        return cls.get_request_info(
            request_url=cls.format_request_url("/accounts/{owner_id}/charges".format(owner_id=owner_id)),
            request_method='get',
            request_data=data,
            error_info=error_info,
            with_return_headers=True
        )

    @classmethod
    def get_cashback_records(cls, owner_id, data=None, error_info=None):
        """ 查询返现记录 """
        return cls.get_request_info(
            request_url=cls.format_request_url("/accounts/{owner_id}/cashbacks".format(owner_id=owner_id)),
            request_method='get',
            request_data=data,
            error_info=error_info,
            with_return_headers=True
        )

    @classmethod
    def get_cost_records(cls, owner_id, data=None, error_info=None):
        """ 查询消费记录 """
        return cls.get_request_info(
            request_url=cls.format_request_url("/accounts/{owner_id}/bills".format(owner_id=owner_id)),
            request_method='get',
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_cost_detail_records(cls, owner_id, bill_id, data=None, error_info=None):
        """ 查询消费明细记录 """
        return cls.get_request_info(
            request_url=cls.format_request_url(
                "/accounts/{owner_id}/bills/{bill_id}".format(owner_id=owner_id, bill_id=bill_id)
            ),
            request_method='get',
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_cost_info(cls, data=None, error_info=None):
        """ 查询消费数据 """
        return cls.get_request_info(
            request_url=cls.format_request_url("/accounts/costinfo"),
            request_method='get',
            request_data=data,
            error_info=error_info
        )

    @classmethod
    def get_statistic(cls, owner_id, data=None, error_info=None):
        """ 查询某人的统计数据 """
        if data is None:
            data = {'owner_ids': [owner_id]}
        else:
            data['owner_ids'] = [owner_id]

        rst = cls.get_request_info(
            request_url=cls.format_request_url("/accounts/statistic"),
            request_method='get',
            request_data=data,
            error_info=error_info
        )
        if rst is not False:
            return rst[owner_id] if owner_id in rst else rst[str(owner_id)]
        return rst


class CoreAPIArea(CoreAPI):
    """
    核心层区域服务的API
    """
    Module_Name = "area"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def transfer_code_name(cls, transfer_type, province=None, city=None, district=None):
        # transfer_type == 1: code转name
        # transfer_type == 2: name转code
        if transfer_type == 1:
            default_value = 0
        else:
            default_value = ""
        if not province:
            province = default_value
        if not city:
            city = default_value
        if not district:
            district = default_value
        return cls.get_request_info(
            request_url=cls.format_request_url(
                "/area/{province}/{city}/{district}".format(province=str(province), city=str(city),
                                                            district=str(district))
            ),
            request_method="get"
        )


class CoreAPISms(CoreAPI):
    """
    核心层短信服务的API
    """
    Module_Name = "sms"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def verify_captcha(cls, tel, code):
        return cls.get_request_info(
            request_url=cls.format_request_url(
                "/service/smscode/{tel}/{code}".format(tel=tel, code=code)
            ),
            request_method="get",
            return_bool=True
        )


class CoreAPIGps(CoreAPI):
    """
    gps服务
    """
    Module_Name = "gps"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def search(cls, longitude, latitude, radius, time, city_code):
        return cls.get_request_info(
            request_url=cls.format_request_url('/apps/gps/user/search'),
            request_method='post',
            request_data={
                "longitude": float(longitude),
                "latitude": float(latitude),
                "radius": float(radius),
                "time": int(time),
                "city_code": int(city_code)
            }
        )


class CoreAPIEmpire(CoreAPI):
    """
    帝国系统的核心层接口
    """
    Module_Name = 'empire'
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def get_user_id_from_token(cls, request=None, token=None, error_info=None):
        """
        通过token获取客户（商户）ID

        token: http headers的Authorization的值，除去'token '部分，形如"uf2y4t894394g9p8ytyr89ryfb"
        request: django的request对象
        优先级：token -> request
        """
        if not request and not token:
            return 0
        elif request:
            auth = token
            if not auth:
                auth = request.META.get('HTTP_AUTHORIZATION')
            if not auth or 'token' not in auth:
                return 0
            token = auth.split(' ')[1]
        response_data = cls.get_request_info(
            request_url=cls.format_request_url("/shops/tokens"),
            request_method="get",
            request_data={"content": token},
            error_info=error_info
        )
        return response_data.get("id", 0) if response_data is not False else 0


class CoreAPILog(CoreAPI):
    """
    日志系统的核心层接口
    """
    Module_Name = "log"
    URL_Prefix = CoreAPI.Hostname_Core_IP.get(Module_Name, {}).get(CoreAPI.target)

    @classmethod
    def get_user_logs(cls, data=None, error_info=None):
        return cls.get_request_info(
            request_url=cls.format_request_url("/logsys/staff/logs"),
            request_method='get',
            request_data=data,
            error_info=error_info,
            with_return_headers=True
        )
