#!/usr/bin/env python
# coding:utf-8

"""
A WSGI application entry.
"""
import sys

import os

# 模块自己的PYTHON_PATH, 让代码找到正确的tools_lib. =>要在所有import前做!!!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)))

from tools_lib.log import init_log
# 配置全局logging. => 配完PYTHON_PATH,在所有的import前做!!!
init_log(os.path.dirname(os.path.abspath(__file__)))

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
    WSGI_APP.run(5009, host='0.0.0.0')
else:
    # init log does not work here.
    print "\n@@@ uWSGI @@@\n"
    application = WSGI_APP.get_wsgi_application()
