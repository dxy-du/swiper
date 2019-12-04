import logging

from django.core.cache import cache

from common import stat
from common import keys
from libs.cache import rds
from user import logics
from user.models import User
from user.models import Profile
from user.forms import UserForm
from user.forms import ProfileForm
from libs.http import render_json

inf_log = logging.getLogger('inf')


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    status = logics.send_vcode(phonenum)
    if status:
        return render_json()
    else:
        raise stat.SendSmsErr


def submit_vcode(request):
    '''通过验证码登录、注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    cached_vcode = cache.get(keys.VCODE_K % phonenum)  # 取出缓存的验证码

    # 检查验证码是否正确
    if vcode and vcode == cached_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
            inf_log.info('%s login with id %s' % (user.nickname, user.id))
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum)  # 创建用户
            inf_log.info('new user: %s' % user.id)

        # 执行登陆过程
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        raise stat.VcodeErr


def get_profile(request):
    '''获取个人资料'''
    key = keys.PROFILE_K % request.uid
    result = rds.get(key)
    print('从缓存获取: %s' % result)

    if result is None:
        profile, _ = Profile.objects.get_or_create(id=request.uid)
        result = profile.to_dict()
        print('从数据库获取: %s' % result)

        rds.set(key, result, 1000)  # 将数据写入缓存
        print('将数据写入缓存')
    return render_json(result)


def set_profile(request):
    '''修改个人资料'''
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 检查数据有效性
    if not user_form.is_valid():
        raise stat.UserFormErr(user_form.errors)

    if not profile_form.is_valid():
        raise stat.ProfileFormErr(profile_form.errors)

    # 保存数据
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)
    Profile.objects.filter(id=request.uid).update(**profile_form.cleaned_data)

    # 删除旧的缓存
    key = keys.PROFILE_K % request.uid
    rds.delete(key)

    # 文强 + 程超 的思路
    # user = User.objects.get(id=request.uid)
    # user.__dict__.update(user_form.cleaned_data)
    # user.save()

    return render_json()


def upload_avatar(request):
    '''
    头像上传

    1. 保存到本地
    2. 上传到七牛云
    3. 保存 URL
    4. 删除本地文件
    '''
    avatar_file = request.FILES.get('avatar')
    logics.upload_avatar.delay(request.uid, avatar_file)
    return render_json()
