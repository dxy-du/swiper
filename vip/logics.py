from common import stat
from user.models import User


def require_permission(perm_name):
    '''权限检查装饰器'''
    def wrapper1(view_func):
        def wrapper2(request, *args, **kwargs):
            user = User.objects.get(id=request.uid)

            if user.is_vip_expired():
                raise stat.VipExpired

            if user.vip.has_permission(perm_name):
                response = view_func(request, *args, **kwargs)  # 计算原函数的结果
                return response
            else:
                raise stat.PermRequired
        return wrapper2
    return wrapper1
