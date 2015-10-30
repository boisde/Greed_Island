# -*- coding:utf-8 -*-
__author__ = 'Qian Lei'


# 公司内部员工信息缓存（数据源:node.js服务）
key_staff_info = "mrwind_inc_staff_info:{user_id}"

# 配送员简要信息
key_deliver_info = "DELIVER:INFO:{user_id}"

# 配送员邀请商户的邀请码
key_staff_invite_shop_code = "staff:{id}:invite_shop_code:{code}"
# 商户邀请商户的邀请码
key_shop_invite_shop_code = "shop:{id}:invite_shop_code:{code}"

# 商户某月累计奖励金额
key_shop_invite_reward = "mall:shop:{shop_id}:invite_shop_reward:{year}:{month}"
# 商户某日是否已有过邀请奖励
key_shop_invite_reward_flag = "mall:shop:{shop_id}:invite_shop_reward:{year}:{month}:{day}:flag"

# 风信v2的自动缓存(以此打头)
key_windchat_2_cache = "SimpleCache-WindChat*"

# 风信v3的自动缓存(以此打头)
key_windchat_3_cache = "SimpleCache-WindChat3*"