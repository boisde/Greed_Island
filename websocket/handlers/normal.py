#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import tornado.web
from tornado.gen import coroutine


class IndexHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        # self.write("This is your response")
        self.render("index.html")
        # we don't need self.finish() because self.render() is fallowed by self.finish() inside tornado
        # self.finish()
