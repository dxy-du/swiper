from redis import Redis

from swiper.config import REDIS


rds = Redis(**REDIS)
