#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-09-07 15:19:48
# @Author  : Jim Zhang (jim.zoumo@gmail.com)
# @Github  : https://github.com/zoumo

import json
import requests
import traceback
import time
from requests.exceptions import Timeout
from random import randint
from tornado.web import gen
from ..geo.mercator import Mercator
from . import async_requests

AK_BUFFER = [
    "sUiLz1vjhG212GBTnd5lZ8qw",
    "fudo2FQT2a57BlYmG8TNtWR5",
    "MlCrreOLOENQ8g4diEcVYpnh",
    "BCxvz1Cj51ilaf76ULAF5Iva",
    "MIp3BbV0YmtGX2VDqYVu12II",
    "SyXl5mIxG1ZOrCaNDTdCDIfn",
    "GpPGxVwFP1eEH0UOQpk9Xgsu",
    "xkZDTrLXGioD2ajPrKTBdHon",
    "TiNWpHzFPO25W7a94dEwS0yX",
    "6r6w6wFKiao9626G09UNKS8O"
]


def _get_ak():
    return AK_BUFFER[randint(0, len(AK_BUFFER) - 1)]


@gen.coroutine
def async_get_distance(from_lat, from_lng, to_lat, to_lng, region, origin_region, dest_region, mode='walking'):
    """
    调用百度API获取不同模式下的距离
    百度API文档地址: http://developer.baidu.com/map/index.php?title=webapi/direction-api
    :param from_lat:
    :param from_lng:
    :param to_lat:
    :param to_lng:
    :param region:
    :param origin_region:
    :param dest_region:
    :param mode: 支持 walking(步行) / driving(驾车) / transit(公交)
    :return:
    """

    url = "http://api.map.baidu.com/direction/v1"
    params = {
        "mode": mode,
        "origin": "%f,%f" % (from_lat, from_lng),
        "destination": "%f,%f" % (to_lat, to_lng),
        "region": region,
        "origin_region": origin_region,
        "destination_region": dest_region,
        "output": "json",
        "ak": _get_ak()
    }

    response = yield async_requests.get(url, params=params)
    distance = 0
    if response.code == 200:
        response = json.loads(response.body)
        if response['status'] == 0:
            distance = response['result']['routes'][0]['distance']

    # # 如果获取百度不成功的话
    # if distance == 0:
    #     distance = 1.5 * Mercator.distance(from_lng, from_lat, to_lng, to_lat)
    raise gen.Return(distance)


@gen.coroutine
def aysnc_get_coordinates(city, district, address):
    """
    通过百度地图的API接口，将某个地址转换成经纬度坐标
    详情见：http://developer.baidu.com/map/webservice-placeapi.htm
    中的“5.2 Place检索示例”小节
    """

    address = "%s %s %s" % (city, district, address)
    url = r"http://api.map.baidu.com/geocoder/v2/"
    params = {
        "ak": _get_ak(),
        "output": "json",
        "address": address,
    }
    response = yield async_requests.get(url, params=params)
    lat = 0.0
    lng = 0.0
    if response.code == 200:
        data = json.loads(response.body)
        if data['status'] == 0:
            location = data.get("result").get("location")
            lat = location.get("lat")
            lng = location.get("lng")

    raise gen.Return((lng, lat))
