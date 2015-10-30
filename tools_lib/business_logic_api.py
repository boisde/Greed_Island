# coding: utf-8
__author__ = 'Qian Lei'

import requests
import json
import platform
import socket
from host_info import *  # NOQA

node = platform.node()
if node in ["NEW-API", "BOX-NEW", "bl-service"]:
    url = "http://10.0.0.240:5555"
elif node in ["iZ2590fp6bkZ", "iZ25cisdo69Z", "iZ255xsf5qrZ"]:
    url = "http://10.173.14.210:" + PROD_BL_CD_PORT
elif node in [LOCAL_SGY_NODE]:
    # url = "http://" + PROD_BL_134_OUTER_IP + ":" + str(5555)
    url = "http://" + socket.gethostbyname(socket.gethostname()) + ":" + str(8001)
else:
    # url = "http://localhost:5555"
    url = "http://10.0.0.240:5555"


def get_request_info(request_url, request_method, request_data=None, headers=None, return_bool=False,
                     with_return_headers=False, request=None, error_info=None):
    print url + request_url
    # 2秒超时
    timeout_time = 5
    failed = False

    request_headers = {'Content-Type': "application/json"}
    if headers:
        request_headers = dict(request_headers.items() + headers.items())
    # 如果给了request，则提取token，不用手动生成带token的headers
    if request:
        request_headers["Authorization"] = request.META.get('HTTP_AUTHORIZATION', '')

    try:
        if request_method == "get":
            requests_info = requests.get(url=url+request_url, params=request_data, headers=request_headers,
                                         timeout=timeout_time)
        elif request_method == "post":
            requests_info = requests.post(url=url+request_url, data=json.dumps(request_data), headers=request_headers,
                                          timeout=timeout_time)
        elif request_method == "patch":
            requests_info = requests.patch(url=url+request_url, data=json.dumps(request_data), headers=request_headers,
                                           timeout=timeout_time)
        elif request_method == "put":
            requests_info = requests.put(url=url+request_url, data=json.dumps(request_data), headers=request_headers,
                                         timeout=timeout_time)
        elif request_method == "delete":
            requests_info = requests.delete(url=url+request_url, data=json.dumps(request_data), headers=request_headers,
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


class BusinessLogicDevice(object):
    @classmethod
    def device_model_method(cls, data):
        return get_request_info(request_url='/device/model_method', request_method='post', request_data=data)

    @classmethod
    def device_instance_save(cls, data):
        return get_request_info('/device/instance_save', 'post', data, True)

    @classmethod
    def device_login(cls, data, headers):
        return get_request_info(request_url='/device/login', request_method='post', request_data=data, headers=headers)

    @classmethod
    def device_v2_login(cls, data, headers):
        return get_request_info(request_url='/device/v2/login', request_method='post', request_data=data,
                                headers=headers)

    @classmethod
    def device_v2_windwatch_upload_data(cls, data, error_info=None):
        return get_request_info(request_url='/device/v2/windwatch/sensor/data', request_method='post',
                                request_data=data, error_info=error_info)

    @classmethod
    def device_update_device_app_relation(cls, data, headers={}):
        return get_request_info(request_url='/device/info/device_info', request_method='patch', request_data=data,
                                return_bool=True, headers=headers)

    @classmethod
    def device_create_or_update_device_info(cls, data, headers):
        return get_request_info(request_url='/device/info/device_info', request_method='post', request_data=data,
                                headers=headers)

    @classmethod
    def device_create_or_update_device_token(cls, data, headers):
        return get_request_info(request_url='/device/info/token', request_method='post', request_data=data,
                                headers=headers, return_bool=True)

    @classmethod
    def device_push_msg_to_user_id(cls, data):
        return get_request_info(request_url='/device/msg/pushing', request_method='post', request_data=data,
                                return_bool=True)

    @classmethod
    def device_batch_push_msgs_to_user_ids(cls, data):
        return get_request_info(request_url='/device/msg/batch_pushing', request_method='post', request_data=data,
                                return_bool=True)

    @classmethod
    def device_get_app_versions(cls, data):
        return get_request_info(request_url='/app/version', request_method='get', request_data=data)

    @classmethod
    def device_upload_app_package(cls, data):
        return get_request_info(request_url='/app/version', request_method='post', request_data=data)

    @classmethod
    def device_app_expire_checking(cls):
        return get_request_info(request_url='/app/expire_checking', request_method='get')

    @classmethod
    def device_download_app_package(cls, type, app_type, package_name):
        from tools_lib.response import RedirectResponse
        return RedirectResponse(redirect_to=url+"/app/downloads/android/"+type+"/"+package_name+"?app_type="+app_type)

    @classmethod
    def device_get_latest_app_version(cls, data):
        return get_request_info(request_url='/app/android/version', request_method='get', request_data=data)

    @classmethod
    def device_get_app_history_info(cls, data):
        return get_request_info(request_url='/app/android/history', request_method='get', request_data=data)

    @classmethod
    def device_active_app_version(cls, data):
        return get_request_info(request_url='/app/android/active_version', request_method='post', request_data=data,
                                return_bool=True)

    @classmethod
    def device_stop_update_version(cls, data):
        return get_request_info(request_url='/app/android/stop_update_version', request_method='post',
                                request_data=data, return_bool=True)


class BusinessLogicNews(object):
    @classmethod
    def get_shop_news(cls, data, with_return_headers=True):
        return get_request_info(request_url='/news/shop', request_method='get', request_data=data,
                                with_return_headers=with_return_headers)

    @classmethod
    def create_shop_news(cls, data):
        return get_request_info(request_url='/news/shop', request_method='post', request_data=data)

    @classmethod
    def update_shop_news(cls, news_id, data):
        return get_request_info(request_url='/news/shop/'+str(news_id), request_method='patch', request_data=data)

    @classmethod
    def delete_shop_news(cls, news_id):
        return get_request_info(request_url='/news/shop/'+str(news_id), request_method='delete')

    @classmethod
    def get_staff_news(cls, data, with_return_headers=True):
        return get_request_info(request_url='/news/staff', request_method='get', request_data=data,
                                with_return_headers=with_return_headers)

    @classmethod
    def create_staff_news(cls, data):
        return get_request_info(request_url='/news/staff', request_method='post', request_data=data)

    @classmethod
    def update_staff_news(cls, news_id, data):
        return get_request_info(request_url='/news/staff/'+str(news_id), request_method='patch', request_data=data)

    @classmethod
    def delete_staff_news(cls, news_id):
        return get_request_info(request_url='/news/staff/'+str(news_id), request_method='delete')


class BusinessLogicNotice(object):
    @classmethod
    def get_shop_bulletin(cls, data, with_return_headers):
        return get_request_info(request_url='/notice/shop/bulletin', request_method='get', request_data=data,
                                with_return_headers=with_return_headers)

    @classmethod
    def get_single_shop_bulletin(cls, bulletin_id):
        r = requests.get(url=url+"/notice/shop/bulletin/"+str(bulletin_id))
        return r.content

    @classmethod
    def create_shop_bulletin(cls, data):
        return get_request_info(request_url='/notice/shop/bulletin', request_method='post', request_data=data)

    @classmethod
    def update_shop_bulletin(cls, bulletin_id, data):
        return get_request_info(request_url='/notice/shop/bulletin/'+str(bulletin_id), request_method='patch',
                                request_data=data)

    @classmethod
    def get_shop_notice(cls, data, with_return_headers):
        return get_request_info(request_url='/notice/shop/personal_notice', request_method='get', request_data=data,
                                with_return_headers=with_return_headers)

    @classmethod
    def create_shop_notice(cls, data):
        return get_request_info(request_url='/notice/shop/personal_notice', request_method='post', request_data=data)

    @classmethod
    def get_shop_unread_num(cls, data):
        return get_request_info(request_url='/notice/shop/personal_notice/unread_num', request_method='get',
                                request_data=data)

    @classmethod
    def read_shop_notice(cls, notice_id, data):
        return get_request_info(request_url='/notice/shop/personal_notice/'+str(notice_id), request_method='patch',
                                request_data=data)

    @classmethod
    def get_staff_bulletin(cls, data, with_return_headers):
        return get_request_info(request_url='/notice/staff/bulletin', request_method='get', request_data=data,
                                with_return_headers=with_return_headers)

    @classmethod
    def get_single_staff_bulletin(cls, bulletin_id):
        r = requests.get(url=url+"/notice/staff/bulletin/"+str(bulletin_id))
        return r.content

    @classmethod
    def create_staff_bulletin(cls, data):
        return get_request_info(request_url='/notice/staff/bulletin', request_method='post', request_data=data)

    @classmethod
    def update_staff_bulletin(cls, bulletin_id, data):
        return get_request_info(request_url='/notice/staff/bulletin/'+str(bulletin_id), request_method='patch',
                                request_data=data)

    @classmethod
    def get_staff_notice(cls, data, with_return_headers):
        return get_request_info(request_url='/notice/staff/personal_notice', request_method='get', request_data=data,
                                with_return_headers=with_return_headers)

    @classmethod
    def create_staff_notice(cls, data):
        return get_request_info(request_url='/notice/staff/personal_notice', request_method='post', request_data=data)

    @classmethod
    def get_staff_unread_num(cls, data):
        return get_request_info(request_url='/notice/staff/personal_notice/unread_num', request_method='get',
                                request_data=data)

    @classmethod
    def read_staff_notice(cls, notice_id, data):
        return get_request_info(request_url='/notice/staff/personal_notice/'+str(notice_id), request_method='patch',
                                request_data=data)


class BusinessLogicInvite(object):
    # 创建邀请商户的记录
    @classmethod
    def create_invite_shop_records(cls, data, error_info=None):
        return get_request_info(
            request_url='/invite/shop/records',
            request_method='post',
            request_data=data,
            error_info=error_info
        )

    # 查询邀请商户的记录
    @classmethod
    def get_invite_shop_records(cls, data, error_info=None):
        return get_request_info(
            request_url="/invite/shop/records",
            request_method='get',
            request_data=data,
            error_info=error_info
        )

    # 查询邀请商户的记录(后台版)
    @classmethod
    def cloud_get_invite_shop_records(cls, data, error_info=None):
        return get_request_info(
            request_url="/invite/shop/simple/records",
            request_method='get',
            request_data=data,
            error_info=error_info,
            with_return_headers=True
        )

    # 更新商户邀请记录
    @classmethod
    def update_invite_shop_record(cls, record_id, data, error_info=None):
        return get_request_info(
            request_url="/invite/shop/records/{id}".format(id=record_id),
            request_method='patch',
            request_data=data,
            error_info=error_info
        )

    # 创建邀请商户链接
    @classmethod
    def create_invite_shop_resources(cls, data, error_info=None):
        return get_request_info(
            request_url="/invite/shop/resources",
            request_method="post",
            request_data=data,
            error_info=error_info
        )

    # 访问商户邀请链接
    @classmethod
    def get_invite_shop_resource(cls, data, error_info=None):
        return get_request_info(
            request_url="/invite/shop/resources",
            request_method="get",
            request_data=data,
            error_info=error_info
        )

    # 获取邀请相关短信文案
    @classmethod
    def get_sms_content(cls, data, error_info=None):
        return get_request_info(
            request_url="/invite/sms_content",
            request_method="get",
            request_data=data,
            error_info=error_info
        )


class BusinessLogicShop(object):
    @classmethod
    def get_shop_info(cls, shop_owner_id, info_type='base', shop_id=None):
        """
        info_type == "base": 获取简要信息
        info_type == "full": 获取全部信息
        """
        assert info_type in ('base', 'full')
        return get_request_info(
            request_url='/shop/info',
            request_method='get',
            request_data={"info_type": info_type, "shop_owner_id": shop_owner_id, "shop_id": shop_id}
        )

    @classmethod
    def update_shop_info(cls, data):
        return get_request_info(request_url='/shop/info', request_method='patch', request_data=data)

    @classmethod
    def get_business_scope(cls):
        return get_request_info(request_url='/shop/info/business_scope', request_method='get', request_data={})

    @classmethod
    def modify_shop_location(cls, shop_id, data):
        return get_request_info(request_url='/shop/info/'+str(shop_id)+'/location', request_method='post',
                                request_data=data)

    @classmethod
    def update_shop_to_vip(cls, data):
        return get_request_info(request_url='/shop/info/apply_vip', request_method='post', request_data=data)

    @classmethod
    def shop_update_log_record(cls, data, with_return_headers=True):
        return get_request_info(
            request_url='/shop/info/update_log',
            request_method='get',
            request_data=data,
            with_return_headers=with_return_headers
        )

    @classmethod
    def review_shop_update(cls, shop_update_log_id, data):
        return get_request_info(request_url='/shop/info/update_log/'+str(shop_update_log_id), request_method='post',
                                request_data=data)

    @classmethod
    def shop_allow(cls, data):
        return get_request_info(request_url='/shop/info/checking/allow', request_method='post', request_data=data)

    @classmethod
    def shop_deny(cls, data):
        return get_request_info(request_url='/shop/info/checking/deny', request_method='post', request_data=data)

    @classmethod
    def get_shop_stats(cls):
        return get_request_info(request_url='/shop/info/stats', request_method='get', request_data={})

    @classmethod
    def get_shop_list(cls, data, with_return_headers=False):
        return get_request_info(
            request_url='/shop/info/list',
            request_method='get',
            request_data=data,
            with_return_headers=with_return_headers
        )

    @classmethod
    def user_login(cls, data, error_info=None):
        return get_request_info(request_url='/shop/login', request_method='post', request_data=data,
                                error_info=error_info)

    @classmethod
    def check_tel_exist(cls, data):
        return get_request_info(request_url='/shop/login/tel/checking', request_method='get', request_data=data)

    @classmethod
    def get_nearby_deliver_num(cls, shop_id, data):
        return get_request_info(request_url='/shop/location/nearby_delivers_num/'+str(shop_id), request_method='post',
                                request_data=data)

    @classmethod
    def update_shop_rule_id(cls, data):
        return get_request_info(request_url='/shop/info/rule/update', request_method='patch', request_data=data)

    @classmethod
    def get_mall_rules_list(cls, data):
        return get_request_info(request_url='/shop/rules', request_method='get', request_data=data)

    @classmethod
    def create_mall_rules(cls, data):
        return get_request_info(request_url='/shop/rules', request_method='post', request_data=data)

    @classmethod
    def update_mall_rules(cls, rule_id, data):
        return get_request_info(request_url='/shop/rules/'+str(rule_id), request_method='patch', request_data=data)

    @classmethod
    def delete_mall_rules(cls, rule_id, data):
        return get_request_info(request_url='/shop/rules/'+str(rule_id), request_method='delete', request_data=data)

    @classmethod
    def get_rule_info_from_shop_id(cls, shop_id):
        return get_request_info(request_url='/shop/rules/shop/'+str(shop_id), request_method='get')

    @classmethod
    def get_mall_rule_catalog(cls):
        return get_request_info(request_url='/shop/rules/catalog', request_method='get')

    @classmethod
    def create_or_update_mall_rule_catalog(cls, data):
        return get_request_info(request_url='/shop/rules/catalog', request_method='post', request_data=data)

    @classmethod
    def calculate_fee(cls, shop_id, data):
        return get_request_info(request_url='/shop/rules/shop/'+str(shop_id)+'/fee', request_method='post',
                                request_data=data)


class BusinessLogicSchedule(object):
    @classmethod
    def get_network_type_list(cls):
        rst = get_request_info(request_url='/schedule/logic/network/node_type', request_method='get')
        if rst is False:
            return False
        else:
            return rst.get('content', [])

    @classmethod
    def get_closest_network(cls, longitude, latitude):
        rst = get_request_info(request_url='/schedule/logic/network/node/geo_search', request_method='get',
                               request_data={"lng": longitude, "lat": latitude})
        if rst is False:
            return False
        else:
            return rst['content'][0]
