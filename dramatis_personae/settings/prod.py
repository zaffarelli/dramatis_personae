"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
from .base import *
from .celery import *

DEBUG = False
ALLOWED_HOSTS = ['*']
CELERY_BROKER_URL = 'amqp://guest@raspipink//'
SECRET_KEY = '6j@b*@a*k0-23vmk4@i%r@_5es5+8uy!23rl2+1^qx491898-b'

INSTANCE_NAME = 'RASPIPINK PROD'

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



