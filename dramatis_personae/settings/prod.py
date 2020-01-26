'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
from .base import *

SECRET_KEY = 'v3epeshymug89ti5kd%l1^e(vx&8!xkv^58sp=ju+1pg47qd8v'
DEBUG = False
INSTANCE_NAME = 'PRODUCTION'

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Zaffarelli','zaffarelli@gmail.com') ,
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dp.sqlite3'),
    }
}
