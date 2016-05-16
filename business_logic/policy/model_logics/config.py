#!/usr/bin/env python
# coding:utf-8
import platform
from tools_lib.host_info import TEST_BL_DB_IP, BL_SERVICE_NODE, BL_DB_IP

NODE = platform.node()

"""DB configurations."""
DB = {
    'default': {
        'host': TEST_BL_DB_IP,
        'port': 3306,
        'user': 'fengdev',
        'password': 'qaz123',
        'database': 'bl_policy',
    },
    # PROD CI
    'iZ25nnfsyvhZ': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'database': 'test',
    },
    # PROD
    BL_SERVICE_NODE: {
        'host': BL_DB_IP,
        'port': 3306,
        'user': 'fengbusiness',
        'password': 'bu3l%si6u&w9*bn',
        'database': 'bl_policy'
    }
}


"""Default configurations."""
DB_CONF = DB.get(NODE, DB['default'])
DEFAULT_CONFIGS = {
    'db': {
        'host': DB_CONF['host'],
        'port': 3306,
        'user': DB_CONF['user'],
        'password': DB_CONF['password'],
        'database': DB_CONF['database']
    }
}


class Dict(dict):
    """
    Simple dict but support access as x.y style.
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


def merge(defaults, override):
    result = {}
    for key, val in defaults.iteritems():
        if key in override:
            if isinstance(val, dict):
                result[key] = merge(val, override[key])
            else:
                result[key] = override[key]
        else:
            result[key] = val
    return result


def to_dict(raw_dict):
    result_dict = Dict()
    for key, val in raw_dict.iteritems():
        result_dict[key] = to_dict(val) if isinstance(val, dict) else val
    return result_dict


CONFIGS = to_dict(DEFAULT_CONFIGS)

# 打印最终的配置
if __name__ == "__main__":
    print "platform.node()=[%s]" % platform.node()
    print "Configure using:\n%s" % CONFIGS
