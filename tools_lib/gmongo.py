# -*- coding:utf-8 -*-

import platform
from pymongo import MongoClient
from tools_lib.host_info import *

MongoDB_SERVERS = {
    LOCALHOST_NODE: {
        "host": TEST_DEV_APP_IP,
        "port": 27017
    },
    TEST_CORE_API_NODE: {
        "host": TEST_DEV_APP_IP,
        "port": 27017
    },
    ONLINE_AL_171_NODE: {
        "host": BL_DB_IP,
        "port": 27017
    },
    LOCAL_SGY_NODE: {
        "host": TEST_DEV_APP_IP,
        "port": 27017
    },
    LOGGING_CENTER_NODE: {
        "host": LOGGING_CENTER_INNER_IP,
        "port": 27017
    },
}
node = platform.node()
if node not in MongoDB_SERVERS.keys():
    node = LOCALHOST_NODE


class GMongoClient(MongoClient):
    def __init__(self, *args, **kwargs):
        kwargs.update(MongoDB_SERVERS[node])
        # kwargs['max_pool_size'] = 200
        # kwargs['waitQueueTimeoutMS'] = 100
        super(GMongoClient, self).__init__(*args, **kwargs)



