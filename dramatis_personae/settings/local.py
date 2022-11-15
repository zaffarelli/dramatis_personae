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

INSTANCE_NAME = 'ZOTZGI_DEV'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dramatis_personae',
        'USER': 'dp',
        'PASSWORD': 'dp',
        'HOST': '',
        'PORT': '',
        'CONN_MAX_AGE': None,
        'TEST': {
            'NAME': 'test_dramatis_personae',
        },
    },
}

# import sys
# if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
#     DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript;charset=utf-8", ".es6", True)
    mimetypes.add_type("application/javascript;charset=utf-8", ".js", True)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dramatis_personae.settings")

