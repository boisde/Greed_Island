#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import time
import requests
import json
from util import get_ecs_api_url
import api_funcs as af
import config as ac

gen = {
    'snapshot_id': None,
    'image_id': None,
    'instance_id': None,
    'ip': None,
}


def start():
    # 1. 创建快照: 如 69 python 系统盘
    url = get_ecs_api_url('CreateSnapshot', DiskId=ac.Node.disk_ids[ac.Node.PYTHON_API])
    print('创建快照: %s' % url)
    resp_obj = requests.get(url)
    resp = json.loads(resp_obj.content)
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    snapshot_id = resp['SnapshotId']
    if not snapshot_id:
        print('创建快照失败!')
        return False
    gen['snapshot_id'] = snapshot_id
    # 1.1 等待快照ready
    slept = 5
    time.sleep(slept)
    s = af.Snapshot.status(snapshot_id)
    while s['Status'] != 'accomplished' and slept < 60:
        print('等待中...')
        time.sleep(5)
        slept += 5
        s = af.Snapshot.status(snapshot_id)

    # 2. 创建镜像
    url = get_ecs_api_url('CreateImage', RegionId=ac.REGION, SnapshotId=snapshot_id)
    print('创建镜像: %s' % url)
    resp_obj = requests.get(url)
    resp = json.loads(resp_obj.content)
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    image_id = resp['ImageId']
    if not image_id:
        print('创建镜像失败, 开始删除快照...')
        url = get_ecs_api_url('DeleteSnapshot', SnapshotId=snapshot_id)
        requests.get(url)
        print('删除快照指令已发送.')
        return False
    gen['image_id'] = image_id

    # 3. 根据镜像导入实例: 要先有一个profile文件 InstanceId
    profile = {
        "RegionId": ac.REGION,
        "ZoneId": ac.ZONE,
        "SecurityGroupId": "G1023804984578217",
        "IoOptimized": "none",

        "InstanceChargeType": "PostPaid",
        "InternetChargeType": "PayByTraffic",
        "InternetMaxBandwidthOut": 1,
        "InternetMaxBandwidthIn": 1,

        "Description": "",
        "InstanceName": "TeaParty001",
        "HostName": "TeaParty001",

        "ImageId": image_id,

        "InstanceNetworkType": "classic",
        "InstanceType": "ecs.s1.small",

        "Password": ac.DEFAULT_PASS
    }
    url = get_ecs_api_url('CreateInstance', **profile)
    print('创建实例: %s' % url)
    resp_obj = requests.get(url)
    resp = json.loads(resp_obj.content)
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    instance_id = resp['InstanceId']
    if not instance_id:
        print('创建实例失败, 开始删除镜像和快照...')
        url = get_ecs_api_url('DeleteImage', ImageId=image_id, RegionId=ac.REGION)
        requests.get(url)
        print('删除镜像指令已发送.')
        url = get_ecs_api_url('DeleteSnapshot', SnapshotId=snapshot_id)
        requests.get(url)
        print('删除快照指令已发送.')
        return False
    gen['instance_id'] = instance_id

    # 4. 分配公网ip
    url = get_ecs_api_url('AllocatePublicIpAddress', InstanceId=instance_id)
    print('分配公网ip: %s' % url)
    resp_obj = requests.get(url)
    resp = json.loads(resp_obj.content)
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    ip = resp['IpAddress']
    gen['ip'] = ip

    # 5. 开启实例
    url = get_ecs_api_url('StartInstance', InstanceId=instance_id)
    print('开启实例中: %s' % url)
    requests.get(url)


def end():
    print('开始停止实例...')
    url = get_ecs_api_url('StopInstance', InstanceId=gen['instance_id'])
    requests.get(url)

    print('开始删除实例, 镜像和快照...')
    url = get_ecs_api_url('DeleteInstance', InstanceId=gen['instance_id'])
    requests.get(url)
    print('删除实例指令已发送.')
    url = get_ecs_api_url('DeleteImage', ImageId=gen['image_id'], RegionId=ac.REGION)
    requests.get(url)
    print('删除镜像指令已发送.')
    url = get_ecs_api_url('DeleteSnapshot', SnapshotId=gen['snapshot_id'])
    requests.get(url)
    print('删除快照指令已发送.')
    return True


if __name__ == '__main__':
    start()
