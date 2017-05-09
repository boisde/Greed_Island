#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
import sys


# '{A:B,C:{D:E},F:G}'
# {
#     'a': 'b',
#     'c':{
#             'd': 'e'
#         },
#     'f': 'g'
# }
def dumps(a):
    t = '\t'
    n = '\n'
    t_cnt = 0
    for c in a:
        if c == '{':
            t_cnt += 1
            s = '%s%s%s' % (c, n, (t * t_cnt))
            sys.stdout.write(s),
        elif c == ',':
            s = '%s%s%s' % (c, n, (t * t_cnt))
            sys.stdout.write(s)
        elif c == '}':
            t_cnt -= 1
            s = '%s%s%s' % (n, (t * t_cnt), c)
            sys.stdout.write(s)
        else:
            sys.stdout.write(c)


def recur_dumps(a, _indent_cnt):
    t = '\t'
    n = '\n'
    if not a:
        return
    elif a.startswith('{'):
        _indent_cnt += 1
        sys.stdout.write('{' + n + t * _indent_cnt)
        recur_dumps(a[1:], _indent_cnt)
    elif a.startswith('}'):
        _indent_cnt -= 1
        sys.stdout.write(n + t * _indent_cnt + '}')
        recur_dumps(a[1:], _indent_cnt)
    elif a.startswith(','):
        sys.stdout.write(',' + n + t * _indent_cnt)
        recur_dumps(a[1:], _indent_cnt)
    else:
        sys.stdout.write(a[0])
        recur_dumps(a[1:], _indent_cnt)


if __name__ == '__main__':
    s = '{A:B,C:{D:E},F:G}'
    dumps(s)
    recur_dumps(s, 0)
