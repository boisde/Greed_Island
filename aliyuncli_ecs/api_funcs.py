#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
import requests
from util import get_ecs_api_url


class Snapshot(object):
    @staticmethod
    def status(snapshot_id):
        url = get_ecs_api_url('DescribeSnapshots', SnapshotIds=json.dumps([snapshot_id]))
        print('查询快照: %s' % url)
        resp_obj = requests.get(url)
        if 200 <= resp_obj.status_code < 300:
            resp = json.loads(resp_obj.content)
            print(json.dumps(resp, ensure_ascii=False, indent=2))
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
        url = get_ecs_api_url('DeleteSnapshot', SnapshotId=snapshot_id)
        print('删除快照: %s' % url)
        requests.get(url)
        print('删除快照指令已发送.')

if __name__ == '__main__':
    for i in range(1):
        s_list = Snapshot.list(SnapshotType='auto')  # auto/all/user
        # for s in s_list:
        #     Snapshot.delete(s['SnapshotId'])

