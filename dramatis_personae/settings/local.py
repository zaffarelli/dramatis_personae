"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
from .base import *
from .celery import *

DEBUG = True
ALLOWED_HOSTS = ['*']
CELERY_BROKER_URL = 'amqp://guest@localhost//'
SECRET_KEY = 'yhx#rgigghedua&l_5d+@&f!kf)%s%2^*ztun25n+xuokjkfw!'

INSTANCE_NAME = 'RAGABASH DEV'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'dramatis_personae',
#         'USER': 'dp',
#         'PASSWORD': 'dp',
#         'HOST': '',
#         'PORT': '',
#         'CONN_MAX_AGE': None,
#         },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dramatis_personae.sqlite3',  # This is where you put the name of the db file.
        # If one doesn't exist, it will be created at migration time.
    }
}

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".es6", True)
    mimetypes.add_type("application/javascript", ".js", True)
