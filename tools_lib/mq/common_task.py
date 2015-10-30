# -*- coding:utf-8 -*-
import sys
from celery_worker import app


def normal_task(func, *args, **kwargs):
    args_list = [sys.path, func.__module__, func.__name__]
    args_list.extend(args)
    app.send_task('common_async_task', args_list, **kwargs)
