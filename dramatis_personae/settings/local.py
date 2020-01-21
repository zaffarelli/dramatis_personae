'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
from .base import *

SECRET_KEY = '6j@b*@a*k0-23vmk4@i%r@_5es5+8uy!23rl2+1^qx491898-b'
DEBUG = True
INSTANCE_NAME = 'GALLIARD DEV'

LOGPATH = "dramatis_personae/logs/"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s|%(levelname)s] %(message)s",  # [%(name)s:%(lineno)s
            'datefmt' : "%Y%m%d%H%M%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOGPATH+"dramatis_personae.log",
            'maxBytes': 1000000000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'collector': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'scenarist': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
