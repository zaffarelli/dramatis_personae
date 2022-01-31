"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
from .base import *
from .celery import *

DEBUG = True
ALLOWED_HOSTS = ['*']
CELERY_BROKER_URL = 'amqp://guest@zotzgi//'
SECRET_KEY = 'yhx#rfagghedua&l_5d+@&f!kf)%s%2^*ztun25n+xuokjkfw!'

INSTANCE_NAME = 'ZOTZGI DEV'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dramatis_personae',
        'USER': 'dp',
        'PASSWORD': 'dp',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': None,
        },
}



