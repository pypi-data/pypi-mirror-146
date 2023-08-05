from pickle import TRUE
from .base import *
import os
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3')
    }
}
INSTALLED_APPS +=[
    'debug_toolbar',
    'pympler',
]

MIDDLEWARE +=[
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
}

INTERNAL_IPS = ['127.0.0.1']

##显示pympler
# DEBUG_TOOLBAR_PANELS = [
#     'pympler.panels.MemoryPanel',
# ]


# REDIS_URL = 'redis://127.0.0.1:6379/1'
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         # 设置为redis所在, 以及所用库序列
#         'LOCATION': REDIS_URL,
#         'TIMEOUT': 300,

#         'OPTIONS': {
#             #"PASSWORD": '',
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'PARSER_CLASS': 'redis.connection.HiredisParser',
#         },
#         'CONNECTION_POOL_CLASSS': 'redis.connection.BlockingConnectionPool',
#     }
# }