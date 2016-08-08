#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import tornado.websocket

from models import channels, receivers

# we gonna store clients in dictionary..
clients = dict()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.client_id = None
        self.m_type = None
        super(WebSocketHandler, self).__init__(application, request, **kwargs)

    def open(self, *args):
        print("WebSocket opened")
        self.client_id = self.get_argument("id")
        self.m_type = self.get_argument("m_type")
        self.stream.set_nodelay(True)
        clients[self.client_id] = {"id": self.client_id, "m_type": self.m_type, "object": self}
        print(clients)

    def on_message(self, m_obj):
        """
        找到这个client_id所在的channel里所有应该收到的人的id, 向他们的socket丢一条信息.
        message := {
            'channel': '001',
            'text': 'hello world!'
        }
        """
        # 1. 找到receivers, 记录message, sender, receivers
        ch_id = m_obj['channel']
        m_type = self.m_type
        rs = {}
        if m_type == 'man':
            rs = receivers[ch_id]['staff']
        elif m_type == 'staff':
            rs = receivers[ch_id]['man']

        # 2. 向receivers丢消息
        print("Client %s received a message : %s" % (self.client_id, m_obj))
        for r in rs:
            r_socket = clients.get(r)
            if r_socket:
                self.write_message('Someone[%s] sent me: [%s]' % (r_socket, m_obj['text']))

    def on_close(self):
        print("WebSocket closed")
        if self.client_id in clients:
            del clients[self.client_id]
