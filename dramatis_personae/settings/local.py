"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
from .base import *
from .celery import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '192.168.0.70', '192.168.0.60', '192.168.0.61', '192.168.0.90', 'phasma', 'galliard', 'zotzgi', '192.168.0.23']
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



