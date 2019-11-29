from qiniu import Auth, put_file

from swiper import config


def upload_to_qiniu(filename, filepath):
    '''上传到七牛云'''
    # 构建鉴权对象
    qn_auth = Auth(config.QN_AK, config.QN_SK)

    # 生成上传 Token, 可以指定过期时间等
    token = qn_auth.upload_token(config.QN_BUCKET_NAME, filename, 3600)

    # 要上传文件的本地路径
    put_file(token, filename, filepath)

    url = '%s/%s' % (config.QN_BASE_URL, filename)
    return url
