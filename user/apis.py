from django.http import JsonResponse

from common import stat
from user import logics


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return JsonResponse({'code': stat.OK, 'data': None})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def submit_vcode(request):
    '通过验证码登录、注册'
    return


def get_profile(request):
    '获取个人资料'
    return


def set_profile(request):
    '修改个人资料'
    return


def upload_avatar(request):
    '头像上传'
    return
