#!/usr/bin/env python
# coding:utf-8

import requests

url = "http://express.yqphh.com/login"

payload = "username=fxs1&password=i6l01v&return_url=&act=signin"
headers = {
    'cache-control': "no-cache",
    'Cookie': 'ci_session=3d62b4903808a5c4b684b8cc164c6269588957ff',
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)