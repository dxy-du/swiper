from django.db import models


class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=10, unique=True, verbose_name='会员名称')
    level = models.IntegerField(default=0, verbose_name='会员等级')
    price = models.FloatField(default=0.0, verbose_name='会员价格')
    days = models.IntegerField(default=0, verbose_name='天数')


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=20, unique=True, verbose_name='权限名称')
    desc = models.TextField(verbose_name='权限描述')


class VipPermRelation(models.Model):
    vip_id = models.IntegerField(verbose_name='会员 ID')
    perm_id = models.IntegerField(verbose_name='权限 ID')
