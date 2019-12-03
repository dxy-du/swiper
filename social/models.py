from django.db import models
from django.db.models import Q
from django.db.utils import IntegrityError

from common import stat


class Swiped(models.Model):
    '''滑动记录'''
    STYPE = (
        ('like', '右滑：喜欢'),
        ('superlike', '上滑：超级喜欢'),
        ('dislike', '左滑：不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的 ID')
    sid = models.IntegerField(verbose_name='被滑动者的 ID')
    stype = models.CharField(max_length=10, choices=STYPE, verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = [['uid', 'sid']]  # uid 和 sid 联合唯一，防止重复滑动

    @classmethod
    def swipe(cls, uid, sid, stype):
        '''添加一个滑动记录'''
        # 检查滑动类型
        if stype not in ['like', 'superlike', 'dislike']:
            raise stat.StypeErr

        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            raise stat.ReswipeErr

    @classmethod
    def is_liked(cls, uid, sid):
        '''
        检查是否喜欢过对方

        Returns:
            True : 喜欢
            False: 不喜欢
            None : 没滑过
        '''
        like_types = ['like', 'superlike']
        try:
            swp = cls.objects.get(uid=uid, sid=sid)
            return swp.stype in like_types
        except cls.DoesNotExist:
            return None


class Friend(models.Model):
    '''好友关系表'''
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='好友ID')

    class Meta:
        unique_together = [['uid1', 'uid2']]

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''创建好友关系'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.create(uid1=uid1, uid2=uid2)

    @classmethod
    def break_off(cls, uid1, uid2):
        '''绝交'''
        uid1, uid2 = (uid2, uid1) if uid1 > uid2 else (uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_id_list(cls, uid):
        '''获取自己好友 ID 列表'''
        fid_list = []
        condition = Q(uid1=uid) | Q(uid2=uid)
        for frd in cls.objects.filter(condition):
            fid = frd.uid1 if uid == frd.uid2 else frd.uid2
            fid_list.append(fid)
        return fid_list
