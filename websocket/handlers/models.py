#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals

_channels = [
    {
        'name': '系统通知',
        'man': [
            {
                'id': '1',
                'name': '1',
                'avatar': '1',
                'unread': 0,
            },
            {
                'id': '2',
                'name': '2',
                'avatar': '2',
                'unread': 0,
            },
        ],
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
