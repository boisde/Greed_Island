#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals

from websocket import create_connection

ws = create_connection("ws://localhost:8888/web_socket?id=123")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result = ws.recv()
print("Received '%s'" % result)
ws.close()
