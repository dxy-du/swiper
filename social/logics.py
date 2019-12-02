import datetime

from common import keys
from libs.cache import rds
from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friend


def first_rcmd(uid):
    '''从 Redis 的优先推荐列表中获取要推荐的用户'''
    uid_list = rds.lrange(keys.FIRST_RCMD_K % uid, 0, 19)
    uid_list = [int(uid) for uid in uid_list]  # 将 uid_list 中的 bytes 强转成 int
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num, exclude_ids=()):
    '''从数据库中获取要推荐的用户'''
    profile, _ = Profile.objects.get_or_create(id=uid)  # 获取用户的交友资料

    today = datetime.date.today()
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    # 取出已经滑过的人的 ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)
    exclude_ids = list(exclude_ids) + list(sid_list)

    # 取出需要的用户，同时排除已经滑过的用户
    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    ).exclude(id__in=exclude_ids)[:num]

    return users


def rcmd(uid):
    '''推荐接口'''
    first_users = first_rcmd(uid)  # 首先从优先推荐队列取出用户
    count = 20 - len(first_users)  # 计算需要从数据库取出的用户数量
    first_user_id_list = [u.id for u in first_users]
    db_users = rcmd_from_db(uid, count, first_user_id_list)  # 从数据库取出用户
    return list(first_users) + list(db_users)


def like_someone(uid, sid):
    '''喜欢某人'''
    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='like')

    # 将 sid 从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 检查对方有没有右滑或者上滑过自己
    if Swiped.is_liked(sid, uid):
        # 如果对方喜欢过自己，匹配成好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢某人'''
    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='superlike')

    # 将 sid 从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 检查对方有没有右滑或者上滑过自己
    liked_me = Swiped.is_liked(sid, uid)
    if liked_me:
        # 如果对方喜欢过自己，匹配成好友
        Friend.make_friends(uid, sid)
        return True
    elif liked_me == False:
        return False
    else:
        # 对方没有滑动过自己，需要将将自己的 uid 添加到对方的 “优先推荐队列”
        rds.rpush(keys.FIRST_RCMD_K % sid, uid)
        return False
