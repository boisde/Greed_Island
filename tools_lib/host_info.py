# -*- coding:utf-8 -*-

# 所有涉及机器号及机器IP的都在这里配置，不要在其他配置文件中硬编码

###############################################################
# 机器号
LOCALHOST_NODE = "localhost"
TEST_CORE_DB_NODE = "core-db"
TEST_CORE_API_NODE = "core-service"
TEST_BL_DB_NODE = 'bl-DB'
TEST_BL_SERVICE_NODE = 'bl-service'
# TEST_BL_API_GATEWAY_NODE = 'bl-gateway'
TEST_BL_API_GATEWAY_NODE = 'bl-service'
ONLINE_AL_147_NODE = "AY14072213291500867dZ"
ONLINE_AL_171_NODE = "iZ25r5p59paZ"
ONLINE_AL_CORE_DB_NODE = "iZ256ki220lZ"
ONLINE_AL_CORE_SALVE1_DB_NODE = "iZ25p6i2m59Z"

BL_DB_NODE = 'iZ25ps4uw4tZ'
BL_SERVICE_NODE = 'iZ2590fp6bkZ'
BL_API_GATEWAY_NODE = 'iZ2590fp6bkZ'
LOGGING_CENTER_NODE = 'iZ25po9nyqtZ'

# 老机器
TEST_DEV_APP = 'BOX-NEW'

# 线上风信服务器
WIND_CHAT = 'wind_chat'
# 测试风信服务器
TEST_WIND_CHAT = 'test_wind_chat'
# 线上日志服务器
LOGGING = 'logging'
# 测试日志服务器
TEST_LOGGING = 'test_logging'
# 线上日志中心服务器
LOGGING_CENTER = 'logging_center'
# 测试日志中心服务器
TEST_LOGGING_CENTER = TEST_LOGGING

###########################
# 本地机器
###########################
LOCAL_NOBODY_NODE = 'nobody'
LOCAL_SGY_NODE = 'HARRISONT430'

###############################################################
# 机器IP
LOCALHOST_IP = '127.0.0.1'
TEST_CORE_DB_IP = '10.0.0.233'
TEST_CORE_API_IP = '10.0.0.234'
TEST_BL_DB_IP = '10.0.0.235'
TEST_BL_SERVICE_IP = '10.0.0.240'
TEST_BL_API_GATEWAY_IP = '10.0.0.241'
BL_DB_IP = '10.170.171.199'
BL_SERVICE_IP = '123.57.40.134'
BL_API_GATEWAY_IP = '123.57.40.134'
BL_DB_OUTER_IP = '123.56.117.75'
PROD_BL_134_INNER_IP = '10.173.14.210'
PROD_BL_134_OUTER_IP = '123.57.40.134'
ONLINE_AL_147_OUTER_IP = '182.92.109.147'
ONLINE_AL_147_INNER_IP = '10.171.133.108'
ONLINE_AL_171_OUTER_IP = '182.92.232.171'
ONLINE_AL_171_INNER_IP = '10.171.99.129'
ONLINE_AL_209_OUTER_IP = '123.57.45.209'
ONLINE_AL_209_INNER_IP = '10.173.1.31'
ONLINE_AL_MONGODB_INNER_IP = '10.170.203.30'
ONLINE_AL_MONGODB_OUTER_IP = '123.56.94.138'
ONLINE_AL_CORE_DB_OUTER_IP = '182.92.158.10'
ONLINE_AL_CORE_DB_INNER_IP = '10.171.133.162'
ONLINE_AL_CORE_SALVE1_DB_OUTER_IP = '182.92.166.43'
ONLINE_AL_CORE_SALVE1_DB_INNER_IP = '10.172.197.197'
LOGGING_CENTER_INNER_IP = "10.171.125.72"
LOGGING_CENTER_OUTER_IP = "182.92.115.196"

###########################
# 老机器
###########################
TEST_DEV_APP_IP = '10.0.0.212'

###########################
# 本地机器
###########################
LOCAL_SGY_IP = '10.0.0.160'

###############################################################
# 请求服务端口 (用于线上部署6555/5555切换)
PROD_BL_CD_PORT, PROD_AG_PORT = '5555', '5556'
import os.path
if os.path.exists(os.path.join(os.path.dirname(__file__), os.path.pardir, 'IM_ROLLBACK')):
    PROD_BL_CD_PORT, PROD_AG_PORT = '6555', '6556'
    print "IM ROLLBACK"
    import logging
    logging.info("IM ROLLBACK")
else:
    PROD_BL_CD_PORT, PROD_AG_PORT = '5555', '5556'
    print "IM ACTIVE"
    import logging
    logging.info("IM ACTIVE")
