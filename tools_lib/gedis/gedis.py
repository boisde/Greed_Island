# -*- coding:utf-8 -*-

import platform
from tools_lib.host_info import *
import core_gedis
import logic_gedis
import old_redis

gedis_dict = {
    LOCALHOST_NODE: (core_gedis.Redis, core_gedis.REDIS_SERVERS),
    TEST_CORE_API_NODE: (core_gedis.Redis, core_gedis.REDIS_SERVERS),
    ONLINE_AL_171_NODE: (core_gedis.Redis, core_gedis.REDIS_SERVERS),
    BL_SERVICE_NODE: (logic_gedis.Redis, logic_gedis.REDIS_SERVERS),
    TEST_BL_SERVICE_NODE: (logic_gedis.Redis, logic_gedis.REDIS_SERVERS),
    LOGGING_CENTER_NODE: (core_gedis.Redis, core_gedis.REDIS_SERVERS),
}

# 根据不同平台选择合适的Redis
Redis, redis_config_dict = gedis_dict.get(platform.node(), gedis_dict[LOCALHOST_NODE])
redis_config = redis_config_dict.get(platform.node(), redis_config_dict[LOCALHOST_NODE])

# 获取原系统的redis
def get_old_redis():
    return old_redis.Redis()
