#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import traceback
import time
import json
import api_funcs as af
import config as ac

gen = {
    'snapshot_id': "",
    'image_id': "",
    'instance_id': "",
    'ip': "",
}


def start(disk_id):
    # 1. 创建快照: 如 69 python 系统盘
    snapshot_id = af.Snapshot.create(disk_id)
    gen['snapshot_id'] = snapshot_id

    # 1.1 等待快照ready
    print('等待快照创建...(先等30s)...')
    slept = 30
    time.sleep(slept)
    s = af.Snapshot.status(snapshot_id)
    while not s or s['Status'] != 'accomplished':
        print('等待中[%s]...' % slept)
        time.sleep(20)
        slept += 20
        s = af.Snapshot.status(snapshot_id)
    else:
        print('快照ready了, 等10s缓冲...\n')
        time.sleep(10)

    # 2. 创建镜像
    image_id = af.Image.create(snapshot_id)
    gen['image_id'] = image_id
    # 1.1 等待镜像ready
    print('等待镜像创建...(先等30s)...')
    slept = 30
    time.sleep(slept)
    im = af.Image.status(image_id)
    while not im or im['Status'] != 'Available':
        print('等待中[%s]...' % slept)
        time.sleep(10)
        slept += 10
        im = af.Image.status(image_id)
    else:
        print('镜像ready了, 等10s缓冲...')
        time.sleep(10)

    # 3. 根据镜像导入实例: 要先有一个profile文件 InstanceId
    instance_id = af.Instance.create(image_id, snapshot_id)
    gen['instance_id'] = instance_id

    # 4. 分配公网ip
    ip = af.Instance.allocate_ip(instance_id)
    gen['ip'] = ip

    # 5. 开启实例
    # af.Instance.start(instance_id)


if __name__ == '__main__':
    file_name = 'nodes.json'

    # 0. 先清理文件
    with open(file_name, 'w') as f:
        f.write(b'[')

    try:
        for i, disk in enumerate(ac.disk_ids.values()):
            print('[%s]===' % (i + 1))
            # 1. 真正做事情
            start(disk)

            # 2. 记录到文件里呀
            print(json.dumps(gen, ensure_ascii=False, indent=2))
            with open(file_name, 'a+') as f:
                f.write(b',')
                f.write(json.dumps(gen, ensure_ascii=False, indent=2))
            print('[%s]===\n\n' % (i + 1))
    except:
        print(traceback.format_exc())
    # 3. 记录终结]
    with open(file_name, 'a+') as f:
        f.write(b']')
