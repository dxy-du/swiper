from django.core.cache import cache

from common import stat
from user import logics
from user.models import User
from user.models import Profile
from libs.http import render_json


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return render_json()
    else:
        return render_json(code=stat.SEND_SMS_ERR)


def submit_vcode(request):
    '''通过验证码登录、注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cached_vcode = cache.get('Vcode-%s' % phonenum)  # 取出缓存的验证码

    # 检查验证码是否正确
    if vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum)  # 创建用户

        # 执行登陆过程
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(code=stat.VCODE_ERR)


def get_profile(request):
    '''获取个人资料'''
    profile, _ = Profile.objects.get_or_create(id=request.uid)
    return render_json(profile.to_dict())


def set_profile(request):
    '修改个人资料'
    return


def upload_avatar(request):
    '头像上传'
    return
