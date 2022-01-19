"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
from .base import *
from .celery import *
import os


def get_bool_env(envvar, default = False):
    return os.getenv(envvar, default).lower() in ('true', '1', 't')


DEBUG = get_bool_env('DEBUG')
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

CELERY_BROKER_URL = 'amqp://guest@raspipink//'
SECRET_KEY = '6j@b*@a*k0-23vmk4@i%r@_5es5+8uy!23rl2+1^qx491898-b'

INSTANCE_NAME = 'Cosmic Mass'

STATIC_ROOT = os.getenv('WEB_PATH', '/') + 'dp_static/'
MEDIA_ROOT = os.getenv('WEB_PATH', '/') + 'dp_media/'


# STATIC_ROOT = os.path.join(BASE_DIR, 'dp_static/')
#MEDIA_ROOT = os.path.join(BASE_DIR, 'dp_media/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dramatis_personae',
        'USER': 'dp',
        'PASSWORD': 'dramatis_personae',
        'HOST': '',
        'PORT': '5432',
        },
}
