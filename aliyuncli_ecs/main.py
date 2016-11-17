#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import requests
from util import describe_instance_status


def act(action, **params):
    pass


if __name__ == '__main__':
    url = describe_instance_status()
    print(url)
    resp_obj = requests.get(url)
    print(resp_obj.content)
