from libs.http import render_json
from social import logics


def rcmd_users(request):
    '''推荐用户接口'''
    users = logics.rcmd(request.uid)
    rcmd_data = [user.to_dict() for user in users]
    return render_json(rcmd_data)


def like(request):
    '''右滑：喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def superlike(request):
    '''上滑：超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''左滑：不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


def rewind(request):
    '''
    反悔操作

    传参处理:
        1. 客户端传来的任何东西都不可信
        2. 所有客户端传来的东西，都需要经过验证才可以使用
        3. 能不依赖客户端的数据，尽量不让客户端传
    '''
    logics.rewind_swipe(request.uid)
    return render_json()


def who_liked_me(request):
    return render_json()


def friend_list(request):
    return render_json()
