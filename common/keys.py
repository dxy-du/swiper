'''各种缓存的 Key'''

VCODE_K = 'Vcode-%s'  # 验证的 Key，拼接用户的手机号
FIRST_RCMD_K = 'FIRST_RCMD_Q-%s'  # 优先推荐队列，拼接 uid
REWIND_K = 'Rewind-%s-%s'  # 反悔次数的 Key，拼接当天的日期 和 uid
