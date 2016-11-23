#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
import requests
from util import get_ecs_api_url
import config as ac


class Snapshot(object):
    @staticmethod
    def create(disk_id):
        # 1. 创建快照: 如 69 python 系统盘
        url = get_ecs_api_url('CreateSnapshot', DiskId=disk_id)
        print('创建快照: %s' % url)
        resp_obj = requests.get(url)
        resp = json.loads(resp_obj.content)
        print(json.dumps(resp, ensure_ascii=False, indent=2))

        snapshot_id = resp.get('SnapshotId')
        if not snapshot_id:
            print('创建快照失败!')
            return False
        return snapshot_id

    @staticmethod
    def status(snapshot_id):
        url = get_ecs_api_url('DescribeSnapshots', SnapshotIds=json.dumps([snapshot_id]))
        print('快照状态: %s' % url)
        resp_obj = requests.get(url)
        if 200 <= resp_obj.status_code < 300:
            resp = json.loads(resp_obj.content)
            # print(json.dumps(resp, ensure_ascii=False, indent=2))
            return resp['Snapshots']['Snapshot'][0] if resp['TotalCount'] == 1 else None
        else:
            print(json.dumps(resp_obj.content, ensure_ascii=False, indent=2))
            return None

    @staticmethod
    def list(**params):
        url = get_ecs_api_url('DescribeSnapshots', **params)
        print('查询快照: %s' % url)
        resp_obj = requests.get(url)
        if 200 <= resp_obj.status_code < 300:
            resp = json.loads(resp_obj.content)
            # print(json.dumps(resp, ensure_ascii=False, indent=2))
            print(resp['TotalCount'])
            return resp['Snapshots']['Snapshot']
        else:
            print(json.dumps(resp_obj.content, ensure_ascii=False, indent=2))
            return None

    @staticmethod
    def delete(snapshot_id):
        if snapshot_id:
            url = get_ecs_api_url('DeleteSnapshot', SnapshotId=snapshot_id)
            print('删除快照: %s' % url)
            requests.get(url)
            print('删除快照指令已发送.')
        else:
            print('要删除的快照id为空哟.')


class Image(object):
    @staticmethod
    def create(snapshot_id):
        url = get_ecs_api_url('CreateImage', RegionId=ac.REGION, SnapshotId=snapshot_id)
        print('创建镜像: %s' % url)
        resp_obj = requests.get(url)
        resp = json.loads(resp_obj.content)
        print(json.dumps(resp, ensure_ascii=False, indent=2))

        image_id = resp.get('ImageId')
        if not image_id:
            print('创建镜像失败, 开始删除快照...')
            url = get_ecs_api_url('DeleteSnapshot', SnapshotId=snapshot_id)
            requests.get(url)
            print('删除快照指令已发送.')
            raise ValueError('镜像创建失败')
        else:
            return image_id

    @staticmethod
    def status(image_id):
        url = get_ecs_api_url('DescribeImages', ImageId=image_id)
        print('镜像状态: %s' % url)
        resp_obj = requests.get(url)
        if 200 <= resp_obj.status_code < 300:
            resp = json.loads(resp_obj.content)
            # print(json.dumps(resp, ensure_ascii=False, indent=2))
            return resp['Images']['Image'][0] if resp['TotalCount'] == 1 else None
        else:
            print(json.dumps(resp_obj.content, ensure_ascii=False, indent=2))
            return None

    @staticmethod
    def delete(image_id):
        if image_id:
            url = get_ecs_api_url('DeleteImage', ImageId=image_id, RegionId=ac.REGION)
            requests.get(url)
            print('删除镜像指令已发送.')
        else:
            print('要删除的镜像id为空哟.')


class Instance(object):
    @staticmethod
    def status(instance_id):
        if not instance_id:
            print('要查询状态的实例id为空哦.')
            return
        url = get_ecs_api_url('DescribeInstances', InstanceIds=json.dumps([instance_id]))
        print('实例状态: %s' % url)
        resp_obj = requests.get(url)
        if 200 <= resp_obj.status_code < 300:
            resp = json.loads(resp_obj.content)
            # print(json.dumps(resp, ensure_ascii=False, indent=2))
            return resp['Instances']['Instance'][0] if resp['TotalCount'] == 1 else None
        else:
            print(json.dumps(resp_obj.content, ensure_ascii=False, indent=2))
            return None

    @staticmethod
    def create(image_id, snapshot_id=None):
        # 3. 根据镜像导入实例: 要先有一个profile文件 InstanceId
        profile = {
            "RegionId": ac.REGION,
            "ZoneId": ac.ZONE,
            "SecurityGroupId": "G1023804984578217",

            "InstanceChargeType": "PostPaid",
            "InternetChargeType": "PayByTraffic",
            "InternetMaxBandwidthOut": '1',
            "InternetMaxBandwidthIn": '1',

            # "Description": "",
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

        instance_id = resp.get('InstanceId')
        if not instance_id:
            print('创建实例失败, 开始删除镜像和快照...')
            url = get_ecs_api_url('DeleteImage', ImageId=image_id, RegionId=ac.REGION)
            requests.get(url)
            print('删除镜像指令已发送.')
            if snapshot_id:
                url = get_ecs_api_url('DeleteSnapshot', SnapshotId=snapshot_id)
                requests.get(url)
                print('删除快照指令已发送.')
            return None
        return instance_id

    @staticmethod
    def allocate_ip(instance_id):
        # 分配公网ip
        url = get_ecs_api_url('AllocatePublicIpAddress', InstanceId=instance_id)
        print('分配公网ip: %s' % url)
        resp_obj = requests.get(url)
        resp = json.loads(resp_obj.content)
        print(json.dumps(resp, ensure_ascii=False, indent=2))

        ip = resp.get('IpAddress')
        return ip

    @staticmethod
    def start(instance_id):
        if not instance_id:
            print('要启动的实例id为空哟.')
            return False

        # 开启实例
        url = get_ecs_api_url('StartInstance', InstanceId=instance_id)
        print('开启实例中: %s' % url)
        requests.get(url)

    @staticmethod
    def stop(instance_id):
        if not instance_id:
            print('要停止的实例id为空哟.')
            return False
        print('开始停止实例...')
        url = get_ecs_api_url('StopInstance', InstanceId=instance_id)
        requests.get(url)

    @staticmethod
    def delete(instance_id):
        if instance_id:
            url = get_ecs_api_url('DeleteInstance', InstanceId=instance_id)
            requests.get(url)
            print('删除实例指令已发送.')
        else:
            print('实例id为空哟')


if __name__ == '__main__':
    for i in range(1):
        s_list = Snapshot.list(SnapshotType='auto')  # auto/all/user
        # for s in s_list:
        #     Snapshot.delete(s['SnapshotId'])
