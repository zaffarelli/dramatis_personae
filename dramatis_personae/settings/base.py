'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__,os.pardir))))

INSTALLED_APPS = [
    'scenarist.apps.ScenaristConfig',
    'collector.apps.CollectorConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'extra_views',
    'sass_processor',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

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
STATIC_ROOT = 'dp_static/'
MEDIA_ROOT = 'dp_media/'


ALLOWED_HOSTS = ['*']
