#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals


class Dict(dict):
    """
    Simple dict but support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


M_TYPE = Dict({'MAN': 'man', 'STAFF': 'staff'})

# 放db
_channels = [
    {
        '_id': '001',
        'name': '系统通知',
        # 听众
        'man': [
            {
                'id': '1',
                'name': '1',
                'avatar': '1',
                # 'm_type': M_TYPE.MAN,
                'unread': 0,
            },
            {
                'id': '2',
                'name': '2',
                'avatar': '2',
                'unread': 0,
            },
        ],
        # 客服
        'staff': [
            {
                'id': 'a',
                'name': 'a',
                'avatar': 'a',
                'unread': 0,
            },
        ],
    }
]

channels = {c['name']: 1 for c in _channels}

receivers = {}
for c in _channels:
    receivers[c['_id']] = {'man': {}, 'staff': {}}
    for m in c['man']:
        receivers[c['_id']]['man'][m['id']] = m
    for s in c['staff']:
        receivers[c['_id']]['staff'][s['id']] = s