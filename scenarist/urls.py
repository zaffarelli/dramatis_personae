from django.conf.urls import url
from django.urls import path, re_path

from scenarist.views.events import *

urlpatterns = [
  re_path('^events/(?P<id>\d+)/edit$', edit_event, name='edit_event'),
  re_path('^events/(?P<id>\d+)/view$', view_event, name='view_event'),  
]

