#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import os
import sys

# 模块自己的PYTHON_PATH, 让代码找到正确的tools_lib. =>要在所有import前做!!!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from tools_lib.common_util.log import init_log

# 配置全局logging. => 配完PYTHON_PATH,在所有的import前做!!!
init_log(os.path.dirname(os.path.abspath(__file__)))

import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
from tornado.options import define, options, parse_command_line

from tools_lib.host_info import DEBUG
from handlers import normal, websocket

urls = [
    (r'/', normal.IndexHandler),
    (r'/web_socket', websocket.WebSocketHandler),
]


class Application(tornado.web.Application):
    def __init__(self):
        if DEBUG is True:
            settings = {
                "debug": True,
                "autoreload": True,
            }
        else:
            settings = {
                "autoreload": False,
            }
        tornado.web.Application.__init__(self, urls, **settings)

    def log_request(self, handler):
        """Writes a completed HTTP request to the logs.

        By default writes to the python root logger.  To change
        this behavior either subclass Application and override this method,
        or pass a function in the application settings dictionary as
        ``log_function``.
        """
        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = logging.info
        elif handler.get_status() < 500:
            log_method = logging.warning
        else:
            log_method = logging.error
        request_time = 1000.0 * handler.request.request_time()
        log_method("[timeit] [%s] [%s][%s][%s bytes] [%s]: [%d msecs]" %
                   (handler.request.remote_ip, handler.request.method, handler.request.uri,
                    handler._headers._dict.get('Content-Length', 0), handler.get_status(), request_time))


if __name__ == '__main__':
    define("port", default=8888, type=int)
    parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(options.port)

    io_loop_ = tornado.ioloop.IOLoop.current()
    try:
        logging.info('application (%s) will start at %s:%s...' % (os.path.abspath(__file__), '0.0.0.0', options.port))
        io_loop_.start()
    except KeyboardInterrupt:
        io_loop_.stop()
