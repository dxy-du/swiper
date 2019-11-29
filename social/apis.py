from libs.http import render_json
from social import logics


def rcmd_users(request):
    '''推荐用户接口'''
    users = logics.rcmd(request.uid)
    rcmd_data = [user.to_dict() for user in users]
    return render_json(rcmd_data)


def like(request):
    '''右滑：喜欢'''
    return render_json()


def superlike(request):
    '''上滑：超级喜欢'''
    return render_json()


def dislike(request):
    '''左滑：不喜欢'''
    return render_json()


def rewind(request):
    return render_json()


def who_liked_me(request):
    return render_json()


def friend_list(request):
    return render_json()
