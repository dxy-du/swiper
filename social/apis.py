from libs.http import render_json
from social import logics


def rcmd_users(request):
    '''推荐用户接口'''
    users = logics.rcmd(request.uid)
    rcmd_data = [user.to_dict() for user in users]
    return render_json(rcmd_data)
