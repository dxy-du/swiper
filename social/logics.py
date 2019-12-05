import datetime

from swiper import config
from common import keys
from common import stat
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
    Swiped.swipe(uid, sid, 'like')

    # 将 sid 从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 调整对方的滑动积分
    score = config.HOT_RANK_SCORE['like']
    rds.zincrby(keys.HOT_RANK_K, score, sid)

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
    Swiped.swipe(uid, sid, 'superlike')

    # 将 sid 从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 调整对方的滑动积分
    score = config.HOT_RANK_SCORE['superlike']
    rds.zincrby(keys.HOT_RANK_K, score, sid)

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


def dislike_someone(uid, sid):
    '''不喜欢的操作'''
    # 添加滑动记录
    Swiped.swipe(uid, sid, 'dislike')

    # 将 sid 从自己的优先推荐队列中删除
    rds.lrem(keys.FIRST_RCMD_K % uid, 1, sid)

    # 调整对方的滑动积分
    score = config.HOT_RANK_SCORE['dislike']
    rds.zincrby(keys.HOT_RANK_K, score, sid)


def rewind_swipe(uid):
    '''
    反悔一次滑动

    每天允许反悔 3 次，反悔的记录只能是五分钟之内的
    '''
    now = datetime.datetime.now()  # 当前时间

    # 取出当天的反悔次数
    rewind_k = keys.REWIND_K % (now.date(), uid)
    rewind_times = rds.get(rewind_k, 0)  # 当天反悔次数，取不到时默认为 0
    # 检查当前反悔次数
    if rewind_times >= config.REWIND_TIMES:
        raise stat.RewindLimit

    # 取出最后一次的滑动记录
    latest_swipe = Swiped.objects.filter(uid=uid).latest('stime')
    # 检查滑动记录的时间是否超过 5 分钟
    pass_time = now - latest_swipe.stime
    if pass_time.total_seconds() > config.REWIND_TIMEOUT:
        raise stat.RewindTimeout

    # 如果是超级喜欢，需要将自己从对方优先推荐队列删除
    # 如果之前是喜欢或超级喜欢，需要撤销好友关系
    if latest_swipe.stype == 'superlike':
        rds.lrem(keys.FIRST_RCMD_K % latest_swipe.sid, 1, uid)
        Friend.break_off(uid, latest_swipe.sid)
    elif latest_swipe.stype == 'like':
        Friend.break_off(uid, latest_swipe.sid)

    # 调整对方的滑动积分
    score = config.HOT_RANK_SCORE[latest_swipe.stype]
    rds.zincrby(keys.HOT_RANK_K, -score, latest_swipe.sid)

    # 将滑动记录删除
    latest_swipe.delete()

    # 更新反悔次数
    rds.set(rewind_k, rewind_times + 1, 86400)


def users_liked_me(uid):
    '''
    喜欢过或者超级喜欢过我的用户

    查询条件：
        - 我还没有滑过对方
        - 对方右滑或者上滑过自己
    '''
    # 取出已经滑过的人的 ID
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    like_types = ['like', 'superlike']
    uid_list = Swiped.objects.filter(sid=uid, stype__in=like_types)\
                             .exclude(uid__in=sid_list)\
                             .values_list('uid', flat=True)

    users = User.objects.filter(id__in=uid_list)
    return users


def get_top_n(num):
    '''
    获取人气排行前 N 的用户数据

    先开发，再优化，再美化
    '''
    origin_data = rds.zrevrange(keys.HOT_RANK_K, 0, num - 1, withscores=True)  # 取出原始排行数据
    cleaned = [[int(uid), int(score)] for uid, score in origin_data]  # 对原始数据进行清洗
    uid_list = [uid for uid, _ in cleaned]  # 取出所有的 uid
    users = User.objects.filter(id__in=uid_list)  # 取出所有用户
    users = sorted(users, key=lambda user: uid_list.index(user.id))  # 调整 user 的顺序

    # 组装数据
    rank_data = {}
    for idx, user in enumerate(users):
        user_info = user.to_dict('phonenum', 'birthday', 'location', 'vip_id', 'vip_end')
        user_info['score'] = cleaned[idx][1]
        rank = idx + 1
        rank_data[rank] = user_info

    return rank_data
