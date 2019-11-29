from django.utils.deprecation import MiddlewareMixin

from common import stat
from libs.http import render_json


class AuthMiddleware(MiddlewareMixin):
    '''用户登录验证中间件'''
    path_white_list = [
        '/api/user/get_vcode',
        '/api/user/submit_vcode',
    ]

    def process_request(self, request):
        # 检查当前路径是否在白名单中
        if request.path not in self.path_white_list:
            uid = request.session.get('uid')
            if not uid:
                return render_json(code=stat.LOGIN_REQUIRED)
            else:
                request.uid = uid
