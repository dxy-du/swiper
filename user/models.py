'''程序设计要有前瞻性，但是不要过早优化'''

import datetime

from django.db import models

from vip.models import Vip


class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATION = (
        ("北京", "北京"),
        ("上海", "上海"),
        ("深圳", "深圳"),
        ("郑州", "郑州"),
        ("西安", "西安"),
        ("成都", "成都"),
        ("沈阳", "沈阳"),
    )
    phonenum = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=20, default='匿名用户', verbose_name='昵称')
    gender = models.CharField(max_length=6, choices=SEX, default='male', verbose_name='性别')
    birthday = models.DateField(default='1990-01-01', verbose_name='生日')
    location = models.CharField(max_length=15, choices=LOCATION, default='上海', verbose_name='常居地')
    avatar = models.CharField(max_length=256, verbose_name='个人形象')

    vip_id = models.IntegerField(default=1, verbose_name='用户对应的会员 ID')
    vip_end = models.DateTimeField(default='3000-1-1', verbose_name='会员过期时间')

    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        if not hasattr(self, '_vip'):
            self._vip = Vip.objects.get(id=self.vip_id)
        return self._vip

    def is_vip_expired(self):
        '''检查自己的会员是否已经过期'''
        return datetime.datetime.now() >= self.vip_end


class Profile(models.Model):
    '''个人资料'''
    dating_gender = models.CharField(max_length=6, choices=User.SEX, default='male', verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=15, choices=User.LOCATION, default='上海', verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让未匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')
