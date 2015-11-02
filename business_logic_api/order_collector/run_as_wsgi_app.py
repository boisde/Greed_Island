#!/usr/bin/env python
# coding:utf-8

"""
A WSGI application entry.
"""
import os

from transwarp.log import init_log
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

WSGI_APP.add_module(rest_api)

if __name__ == '__main__':
    WSGI_APP.run(5011, host='0.0.0.0')
else:
    # init log does not work here.
    print "\n@@@ uWSGI @@@\n"
    application = WSGI_APP.get_wsgi_application()
