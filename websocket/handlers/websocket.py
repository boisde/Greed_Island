#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import tornado.websocket

from models import channels

# we gonna store clients in dictionary..
clients = dict()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.client_id = None
        super(WebSocketHandler, self).__init__(application, request, **kwargs)

    def open(self, *args):
        print("WebSocket opened")
        self.client_id = self.get_argument("id")
        self.stream.set_nodelay(True)
        clients[self.client_id] = {"id": self.client_id, "object": self}
        print(clients)

    def on_message(self, message):
        """
        when we receive some message we want some message handler..
        for this example i will just print message to console
        """
        print("Client %s received a message : %s" % (self.id, message))
        self.write_message('You[%s] sent me: [%s]' % (self.id, message))

    def on_close(self):
        print("WebSocket closed")
        if self.id in clients:
            del clients[self.id]
