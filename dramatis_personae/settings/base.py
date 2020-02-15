'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__,os.pardir))))
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS = [
    'optimizer.apps.OptimizerConfig',
    'scenarist.apps.ScenaristConfig',
    'collector.apps.CollectorConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'crispy_forms',
    'extra_views',
    'sass_processor',
]

#CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
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
    ],
  },
},]

WSGI_APPLICATION = 'dramatis_personae.wsgi.application'



STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

LOGPATH = os.path.join(BASE_DIR,'logs/')
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

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },{
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },{
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR,'dp_static/')
MEDIA_ROOT = os.path.join(BASE_DIR,'dp_media/')
