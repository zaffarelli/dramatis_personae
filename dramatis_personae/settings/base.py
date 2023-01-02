"""
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))

INSTALLED_APPS = [
    'channels',
    'optimizer.apps.OptimizerConfig',
    'scenarist.apps.ScenaristConfig',
    'cartograph.apps.CartographConfig',
    'collector.apps.CollectorConfig',
    'zapp.apps.ZappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'extra_views',
    'sass_processor',
    'colorfield'
    # 'bootstrap_datepicker_plus',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'scenarist.exceptions.middleware.ExceptionMiddleware',
]

ROOT_URLCONF = 'dramatis_personae.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'collector/templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'collector.context_processors.commons',
            'collector.context_processors.users',
        ],
    },
}]

ASGI_APPLICATION = 'dramatis_personae.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ['127.0.0.1', '6379']
        },
    },
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# LOGPATH = os.path.join(BASE_DIR,'logs/')
LOGPATH = '/var/log/dramatis_personae/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s|%(levelname)8s] %(message)s",  # [%(name)s:%(lineno)s
            'datefmt': "%Y%m%d%H%M%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGPATH + "dramatis_personae.log",
            'maxBytes': 1000000,
            'backupCount': 9,
            'formatter': 'standard',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
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
        'cartograph': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'optimizer': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },

        'scenarist': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'dp_static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'dp_media/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "collector/static")
]

LOGIN_REDIRECT_URL = '/'

MAX_CHAR = 20
RELEASE = '1.3.0'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dramatis_personae.settings')
