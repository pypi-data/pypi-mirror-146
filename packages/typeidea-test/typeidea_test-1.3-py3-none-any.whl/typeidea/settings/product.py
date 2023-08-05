from .base import *


DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'wyh123456',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 5*60,
        'OPTIONS': {'charset':'utf8mb4'},
    },
}

ALLOWED_HOSTS = ['*']


REDIS_URL = '127.0.0.1:6379:1'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 设置为redis所在, 以及所用库序列
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,

        'OPTIONS': {
            #"PASSWORD": '',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASSS': 'redis.connection.BlockingConnectionPool',
    }
}