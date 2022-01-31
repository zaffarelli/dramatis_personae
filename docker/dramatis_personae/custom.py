"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
from .base import *
from .celery import *
import os



DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")

CELERY_BROKER_URL = 'amqp://guest@raspipink//'
SECRET_KEY = '6j@b*@a*k0-23vmk4@i%r@_5es5+8uy!23rl2+1^qx491898-b'

INSTANCE_NAME = 'Cosmic Mass'

STATIC_ROOT = os.environ.get('WEB_PATH') + 'static/'
MEDIA_ROOT = os.environ.get('WEB_PATH') + 'media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
        },
}
