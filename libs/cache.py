from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from redis import Redis as _Redis

from swiper.config import REDIS


class Redis(_Redis):
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        '''带序列化处理的 set 方法'''
        pickled_value = dumps(value, HIGHEST_PROTOCOL)
        return super().set(name, pickled_value, ex, px, nx, xx)

    def get(self, name, default=None):
        '''带反序列化处理和默认值的 get 方法'''
        pickled_value = super().get(name)
        if not pickled_value:
            return default
        else:
            try:
                return loads(pickled_value)
            except UnpicklingError:
                return pickled_value


rds = Redis(**REDIS)
