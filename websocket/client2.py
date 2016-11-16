#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
from websocket import create_connection

ws2 = create_connection("ws://localhost:8888/web_socket?id=2&m_type=man")
msg2 = {
    'channel': '001',
    'text': 'hello world! from 2'
}
ws2.send(json.dumps(msg2))
result2 = ws2.recv()
print("2 Received '%s'" % result2)
