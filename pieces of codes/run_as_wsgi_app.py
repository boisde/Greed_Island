#!/usr/bin/env python
# coding:utf-8

"""
A WSGI application entry.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))

from tools_lib.transwarp import db
from tools_lib.transwarp.web import WSGIApplication
from model_logics.config import CONFIGS
import rest_api

# init db:
db.create_engine(**CONFIGS.db)

# init wsgi app:
WSGI_APP = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))

# wsgi.add_interceptor(api.user_interceptor)
# wsgi.add_interceptor(api.manage_interceptor)
WSGI_APP.add_module(rest_api)

if __name__ == '__main__':
    WSGI_APP.run(5006, host='0.0.0.0')
else:
    # init log does not work here.
    print "\n@@@ uWSGI @@@\n"
    application = WSGI_APP.get_wsgi_application(os.path.abspath(os.path.dirname(__file__)))
