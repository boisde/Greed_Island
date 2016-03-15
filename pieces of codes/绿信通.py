#!/usr/bin/env python
# coding:utf-8

import requests

url = "http://api.china95059.net:8080/sms/query"

querystring = {"name": "fxs", "pwd": "fxs001"}

response = requests.request("GET", url, params=querystring)

print(response.text)
