import random

import requests

from swiper import config


def gen_random_code(length=6):
    '''产生指定长度的随机码'''
    # 香平解法
    # return str(random.randint(10 ** (length - 1), 10 ** length - 1))

    # 建港解法
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def send_vcode(mobile):
    '''
    发送短信验证码

    用户 -> 自己服务器 -> 短信平台 -> 发送短信
    '''
    vcode = gen_random_code()  # 产生验证码
    print('状态码:', vcode)

    args = config.YZX_SMS_ARGS.copy()  # 浅拷贝全局配置
    args['param'] = vcode
    args['mobile'] = mobile

    # 调用第三方接口发送验证码
    response = requests.post(config.YZX_SMS_API, json=args)

    # 检查结果
    if response.status_code == 200:
        result = response.json()
        if result['msg'] == 'OK':
            return True
    return False
