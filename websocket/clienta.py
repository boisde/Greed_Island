#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
from websocket import create_connection

ws3 = create_connection("ws://localhost:8888/web_socket?id=a&m_type=staff")
msg3 = {
    'channel': '001',
    'text': 'hello world! from a'
}
ws3.send(json.dumps(msg3))
result3 = ws3.recv()
print("a Received '%s'" % result3)
