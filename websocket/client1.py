#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import json
from websocket import create_connection

ws = create_connection("ws://localhost:8888/web_socket?id=1&m_type=man")
print("Sending 'Hello, World'...")
msg1 = {
    'channel': '001',
    'text': 'hello world! from 1'
}
ws.send(json.dumps(msg1))
print("Sent")
print("Receiving...")
result = ws.recv()
print("1 Received '%s'" % result)
ws.close()

# ws2 = create_connection("ws://localhost:8888/web_socket?id=2&m_type=man")
# msg2 = {
#     'channel': '001',
#     'text': 'hello world! from 2'
# }
# ws2.send(json.dumps(msg2))
# result2 = ws2.recv()
# print("2 Received '%s'" % result2)
#
#
# ws3 = create_connection("ws://localhost:8888/web_socket?id=a&m_type=staff")
# msg3 = {
#     'channel': '001',
#     'text': 'hello world! from a'
# }
# ws3.send(json.dumps(msg3))
# result3 = ws3.recv()
# print("a Received '%s'" % result3)
