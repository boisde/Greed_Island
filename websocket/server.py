#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)

# we gonna store clients in dictionary..
clients = dict()


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # self.write("This is your response")
        self.render("index.html")
        # we don't need self.finish() because self.render() is fallowed by self.finish() inside tornado
        # self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("WebSocket opened")
        self.id = self.get_argument("id")
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
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


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
    import logging
    parse_command_line()

    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(options.port)
    logging.info("I am working at port %s" % options.port)

    io_loop_ = tornado.ioloop.IOLoop.current()
    try:
        io_loop_.start()
    except KeyboardInterrupt:
        io_loop_.stop()
