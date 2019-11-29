import datetime

from user.models import User
from user.models import Profile
from social.models import Swiped
from social.models import Friend


def rcmd(uid):
    profile, _ = Profile.objects.get_or_create(id=uid)  # 获取用户的交友资料

    today = datetime.date.today()
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)  # 最早出生日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)  # 最晚出生日期

    users = User.objects.filter(
        gender=profile.dating_gender,
        location=profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday,
    )[:20]

    # TODO: 排除已经滑过的用户

    return users


def like_someone(uid, sid):
    '''喜欢某人'''
    # 添加滑动记录
    Swiped.objects.create(uid=uid, sid=sid, stype='like')

    # 检查对方有没有右滑或者上滑过自己
    if Swiped.is_liked(sid, uid):
        # 如果对方喜欢过自己，匹配成好友
        Friend.make_friends(uid, sid)
        return True
    else:
        return False
