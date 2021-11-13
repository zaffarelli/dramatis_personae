from django.urls import re_path
from cartograph.views.starmaps import show_jumpweb, show_orbital_map


urlpatterns = [
    re_path('^ajax/jumpweb/$', show_jumpweb, name='go_jumpweb'),
    re_path('^ajax/orbital/(?P<slug>[\w-]+)/$', show_orbital_map, name='show_orbital_map'),
]