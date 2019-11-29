import datetime

from user.models import User
from user.models import Profile


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
