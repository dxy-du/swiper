'''各种缓存的 Key'''

VCODE_K = 'Vcode-%s'  # 验证的 Key，拼接用户的手机号
FIRST_RCMD_K = 'FIRST_RCMD_Q-%s'  # 优先推荐队列，拼接 uid
REWIND_K = 'Rewind-%s-%s'  # 反悔次数的 Key，拼接当天的日期 和 uid
PROFILE_K = 'Profile-%s'  # 个人资料缓存的 Key，拼接用户的 uid
MODEL_K = 'Model-%s-%s'  # 所有 model 的缓存的 Key，拼接 类的名字 和 model 的主键
HOT_RANK_K = 'HotRank'  # 热度积分排行
