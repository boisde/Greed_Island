#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
import time
import api_funcs as af


def run(gen):

    print('开始运行实例...(指令发送后会等待3s)...')
    af.Instance.start(gen['instance_id'])
    time.sleep(3)
    return True


if __name__ == '__main__':
    with open('nodes.json', 'r+') as f:
        nodes_str = f.read()
        nodes = json.loads(nodes_str)
        for i, node in enumerate(nodes):
            run(node)
            print('[%s]==>>>' % (i+1))
            print(json.dumps(node, ensure_ascii=False, indent=2))
            print('[%s]==<<<' % (i+1))
