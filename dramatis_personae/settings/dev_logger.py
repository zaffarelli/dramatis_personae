import os


#SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
#SITE_ROOT = os.path.abspath(os.path.dirname(__name__))

LOGPATH = "dramatis_personae/logs/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOGPATH+"dramatis_personae.log",
            'maxBytes': 50000000,
            'backupCount': 10,
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
