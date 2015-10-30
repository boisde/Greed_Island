# coding: utf-8

import sys
import platform
import hashlib
from StringIO import StringIO

import qiniu.conf
import qiniu.rs
import qiniu.rsf
import qiniu.io
import qiniu.fop
import qiniu.resumable_io as rio
from tools_lib.host_info import *


node = platform.node()

# 七牛的空间域名
IMAGE_URL_DOMAINS = {
    'AY14072213291500867dZ': "7qn9s9.com2.z0.glb.qiniucdn.com",
    'NEW-API': "7qnajq.com2.z0.glb.qiniucdn.com",
    'localhost': "7qnajq.com2.z0.glb.qiniucdn.com",
    'BOX-NEW': "7qnajq.com2.z0.glb.qiniucdn.com",
    'CLOUD': "7qnajq.com2.z0.glb.qiniucdn.com",
    'iZ2590fp6bkZ': "7qn9s9.com2.z0.glb.qiniucdn.com",
    "iZ25cisdo69Z": "7qn9s9.com2.z0.glb.qiniucdn.com",
    'VM_158_113_centos': "7qn9s9.com2.z0.glb.qiniucdn.com",
    TEST_BL_SERVICE_NODE: "7qnajq.com2.z0.glb.qiniucdn.com",
    TEST_BL_API_GATEWAY_NODE: "7qnajq.com2.z0.glb.qiniucdn.com",
    BL_SERVICE_NODE: "7qn9s9.com2.z0.glb.qiniucdn.com",
    BL_API_GATEWAY_NODE: "7qn9s9.com2.z0.glb.qiniucdn.com",
}

IMAGE_URL_DOMAIN = IMAGE_URL_DOMAINS.get(node, IMAGE_URL_DOMAINS['localhost'])

BUCKETS = {
    'AY14072213291500867dZ': "mrwind",
    'NEW-API': "dev-mrwind",
    'localhost': "dev-mrwind",
    'BOX-NEW': "dev-mrwind",
    'CLOUD': "dev-mrwind",
    'iZ2590fp6bkZ': "mrwind",
    'iZ25cisdo69Z': "mrwind",
    'VM_158_113_centos': "mrwind",
    TEST_BL_SERVICE_NODE: "dev-mrwind",
    TEST_BL_API_GATEWAY_NODE: "dev-mrwind",
    BL_SERVICE_NODE: "mrwind",
    BL_API_GATEWAY_NODE: "mrwind",
}

BUCKET = BUCKETS.get(node, BUCKETS['localhost'])


def get_image_url(image):
    return qiniu.rs.make_base_url(IMAGE_URL_DOMAIN, image) if image else None


def get_image_obj(image):
    # 使用七牛
    if image:
        return {
            "id": image,
            "url": get_image_url(image)
        }
    else:
        return {}


class QiniuUtil(object):
    """
    七牛相关 pip install qiniu
    文档地址: http://developer.qiniu.com/docs/v6/sdk/python-sdk.html
    """
    AK = 'zVxhvVY8ggEUftanwKVdmqNLvoi2IXrOTZG9NwMT'
    SK = 'IIiL9fdiVOHqmiixrF6NYY-pRMVU5Gjo5UfnYPUE'

    def __init__(self):
        qiniu.conf.ACCESS_KEY = self.AK
        qiniu.conf.SECRET_KEY = self.SK

    def get_uptoken(self, bucket_name=BUCKET):
        policy = qiniu.rs.PutPolicy(bucket_name)
        uptoken = policy.token()
        return uptoken

    # 上传本地文件
    def upload_file(self, file_path, bucket_name=BUCKET, key=""):
        policy = qiniu.rs.PutPolicy(bucket_name)
        uptoken = policy.token()
        if not key:
            key = hashlib.md5(open(file_path).read()).hexdigest()
        result, err = qiniu.io.put_file(uptoken, key, file_path)
        if err is not None:
            sys.stderr.write("error: %s" % err)

    # 上传二进制流
    def upload_stream(self, bucket_name=BUCKET, mimetype="text/plain", key="", io_stream=None):
        policy = qiniu.rs.PutPolicy(bucket_name)
        uptoken = policy.token()
        extra = rio.PutExtra(bucket_name)
        extra.mimetype = mimetype
        result, err = rio.put(uptoken, key, StringIO(io_stream), len(io_stream), extra)
        if err is not None:
            sys.stderr.write("error: %s" % err)
        return result

    def get_file_url(self, key, domain=IMAGE_URL_DOMAIN):
        return qiniu.rs.make_base_url(domain, key)

    # 获取文件信息
    def get_file_info(self, key, bucket_name=BUCKET):
        result, err = qiniu.rs.Client().stat(bucket_name, key)
        if err is not None:
            sys.stderr.write("error: %s" % err)
        return result

    # 删除文件
    def delete_file(self, key, bucket_name=BUCKET):
        result, err = qiniu.rs.Client().mark_deleted(bucket_name, key)
        if err is not None:
            sys.stderr.write("error: %s" % err)
        return result

    # 遍历bucket
    def list_all(self, bucket_name=BUCKET, prefix=None, limit=None):
        rs = qiniu.rsf.Client()
        marker = None
        err = None
        item_list = []
        while err is None:
            result, err = rs.list_prefix(bucket_name, prefix=prefix, limit=limit, marker=marker)
            marker = result.get('marker', None)
            item_list.extend(result['items'])
        if err is not qiniu.rsf.EOF:
            # 错误处理
            sys.stderr.write("error: %s" % err)
        return item_list

    # 查看图像属性
    def get_image(self, pic_key, domain=IMAGE_URL_DOMAIN):
        # 生成 base_url
        url = qiniu.rs.make_base_url(domain, pic_key)
        # 生成fop_url
        image_info = qiniu.fop.ImageInfo()
        url = image_info.make_request(url)
        return url