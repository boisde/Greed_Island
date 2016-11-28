#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
import time
import api_funcs as af


def end(gen):
    if gen['instance_id']:
        print('@@@ 注意: 如果实例在启动中, 指令发送了也删不掉哟~ @@@')
        af.Instance.stop(gen['instance_id'])

        # 1.1 等待实例停止
        print('等待实例停止...(先等1s)...')
        slept = 1
        time.sleep(slept)
        ins = af.Instance.status(gen['instance_id'])
        while ins and ins['Status'] != 'Stopped':
            print('等待中[%s]...' % slept)
            time.sleep(10)
            slept += 10
            ins = af.Instance.status(gen['instance_id'])
        else:
            if ins:
                print('实例已停止, 等5s缓冲...')
                time.sleep(5)
            else:
                print('此实例已经不存在.')

        print('开始删除实例, 镜像和快照...')
        af.Instance.delete(gen['instance_id'])
    else:
        pass
    af.Image.delete(gen['image_id'])
    af.Snapshot.delete(gen['snapshot_id'])
    return True


if __name__ == '__main__':
    with open('nodes.json', 'r+') as f:
        nodes_str = f.read()
        nodes = json.loads(nodes_str)
        for i, node in enumerate(nodes):
            end(node)
            print('[%s]==>>>' % (i+1))
            print(json.dumps(node, ensure_ascii=False, indent=2))
            print('[%s]==<<<' % (i+1))
