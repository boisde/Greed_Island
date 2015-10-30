# -*- coding:utf-8 -*-
__author__ = 'Harrison'

import platform

node = platform.node()

# 平台NODE
AY_APP = "AY14072213291500867dZ"
AY_MONITOR = "iZ25cisdo69Z"
GPS_138 = "iZ255xsf5qrZ"
# 负载2
AY_APP_2 = 'iZ2590fp6bkZ'
DEV_APP = "BOX-NEW"
DEV_MONITOR = "NEW-API"
DEV_BL_SERVICE = 'bl-service'


# GPS服务器地址
GPS_SERVER_POOL = {
    DEV_APP: "http://10.0.0.212:5555",
    DEV_BL_SERVICE: "http://10.0.0.212:5555",
    AY_APP: 'http://10.173.1.31:5555',
    AY_APP_2: 'http://10.173.1.31:5555',
}
GPS_SERVER = GPS_SERVER_POOL.get(node, GPS_SERVER_POOL[DEV_APP])

GPS_SEARCH_URL = GPS_SERVER + '/apps/gps/user/search'
# 获取一定时间范围风先生轨迹(不跨天)
GPS_GET_COORDINATES_URL = GPS_SERVER + '/apps/gps/get_coordinates'

# 调度中心服务器地址
SCHEDULE_SERVER_POOL = {
    DEV_APP: "http://10.0.0.212:5555/",
    AY_APP: 'http://127.0.0.1:5555/',
}
SCHEDULE_SERVER = SCHEDULE_SERVER_POOL.get(node, SCHEDULE_SERVER_POOL[DEV_APP])
# 创建单笔发货单
SCHEDULE_NEW_ORDER_CREATE_URL = SCHEDULE_SERVER + 'schedule/shop/call/new_order'
# 完成单笔发货单
SCHEDULE_DELIVER_FINISH_ORDER_URL = SCHEDULE_SERVER + 'schedule/mrwind/{mrwind_id}/call/finish_order'
# 取消单笔发货单
SCHEDULE_SHOP_CANCEL_ORDER = SCHEDULE_SERVER + 'schedule/shop/{shop_id}/call/close_call'
# 取货单笔饭货单
SCHEDULE_DELIVER_SEND_ORDER_URL = SCHEDULE_SERVER + 'schedule/call/call_status'
