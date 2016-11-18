#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import requests
import json
from util import get_ecs_api_url
from config import Node


# # 1. 创建快照: 69 python 系统盘
# aliyuncli ecs CreateSnapshot --DiskId d-254h1jttk
# # 2. 创建镜像
# aliyuncli ecs CreateImage --RegionId --SnapshotId s-2zehhsvq2dx2wij34qk5
# # 3. 根据镜像导入实例: 要先有一个profile文件
# aliyuncli ecs ImportInstance --filename test_206 --instancecount 1 --allocatepublicip yes
# # 4. 启动这个实例
# aliyuncli ecs StartInstance --InstanceId i-2ze9g61svzdbznlv1fgm
# # 5. 查看实例们的状态
# aliyuncli ecs DescribeInstanceStatus
#
#
#
# # 6. 关闭这个实例
# aliyuncli ecs StopInstance --InstanceId i-2ze9g61svzdbznlv1fgm
# # 7. 删除这个实例
# aliyuncli ecs DeleteInstance --InstanceId i-2ze9g61svzdbznlv1fgm
# # 8. 删除这个镜像
# aliyuncli ecs DeleteImage --ImageId m-2ze13d17jpw2s3roln73
# # 9. 删除这个快照
# aliyuncli ecs DeleteSnapshot --SnapshotId s-2zehhsvq2dx2wij34qk5

def start():
    url = get_ecs_api_url('CreateSnapshot', DiskId=Node.disk_ids[Node.PYTHON_API])
    print('创建快照: %s' % url)
    resp_obj = requests.get(url)
    print(json.dumps(resp_obj.content, ensure_ascii=False, indent=2))

    url = get_ecs_api_url('')


def end():
    pass


if __name__ == '__main__':
    # url = get_ecs_api_url('DescribeInstanceStatus', RegionId='cn-beijing')
    # print(url)
    # resp_obj = requests.get(url)
    # print(resp_obj.content)
    pass
