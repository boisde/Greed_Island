#!/usr/bin/env python
# coding:utf-8
import unittest

import os
import sys
# 模块自己的PYTHON_PATH, 让代码找到正确的tools_lib. =>要在所有import前做!!!
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from model_logics.transwarp import db
from model_logics import config

# init db: Always use 'test' for UT
config.CONFIGS['db']['database'] = 'test'
db.create_engine(**config.CONFIGS.db)

if __name__ == '__main__':
    unittest.main()