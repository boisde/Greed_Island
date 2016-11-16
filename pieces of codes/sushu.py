#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import requests
import json

if __name__ == '__main__':
    # # 1. 获取code
    # APP_KEY = '21792177'
    # url = 'https://oauth.taobao.com/authorize'
    # params = {
    #     'client_id': APP_KEY,  # 等同与app-key
    #     'response_type': 'code',
    #     # 'redirect_uri': 'http://api.gomrwind.com:5000/oauth/taobao/call_back'
    #     'redirect_uri': 'http://www.sf-ecs.com/oauth/top/call_back'
    # }
    # resp_obj = requests.get(url, params=params)
    # print(resp_obj.text)

    summary = {}
    other = 0
    with open('recently_sent.log', 'r+') as f:
        lines = f.readlines()

        for line in lines:
            if line.startswith(b'[09-'):
                day = line[1:6]
                if day not in summary:
                    summary[day] = 0
                summary[day] += 1
            else:
                other += 1

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
