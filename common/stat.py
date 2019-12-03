'''
程序状态码
'''

OK = 0

class LogicError(Exception):
    code = None
    data = None

    def __init__(self, data=None):
        # if data:
        #     self.data = data
        # else:
        #     self.data = self.__class__.__name__
        self.data = data or self.__class__.__name__


def gen_logic_err(name, code):
    '''封装一个逻辑异常类'''
    return type(name, (LogicError,), {'code': code})


SendSmsErr = gen_logic_err('SendSmsErr', 1000)          # 发送短信异常
VcodeErr = gen_logic_err('VcodeErr', 1001)              # 状态码异常
LoginRequired = gen_logic_err('LoginRequired', 1002)    # 用户未登陆
UserFormErr = gen_logic_err('UserFormErr', 1003)        # 用户表单错误
ProfileFormErr = gen_logic_err('ProfileFormErr', 1004)  # 资料表单错误
StypeErr = gen_logic_err('StypeErr', 1005)              # 滑动类型错误
ReswipeErr = gen_logic_err('ReswipeErr', 1006)          # 重复滑动一个人
RewindLimit = gen_logic_err('RewindLimit', 1007)        # 反悔次数达到限制
RewindTimeout = gen_logic_err('RewindTimeout', 1008)    # 反悔超时
VipExpired = gen_logic_err('VipExpired', 1009)          # Vip 已过期
PermRequired = gen_logic_err('PermRequired', 1010)      # 没有该权限
