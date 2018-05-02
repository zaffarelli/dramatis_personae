from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	re_path('^refs/$', views.refs, name='refs'),
	re_path('^personae/$', views.personae, name='personae'),
	re_path('^recalc/$', views.recalc, name='recalc'),
	re_path('^add/persona/$', views.add_persona, name='add_persona'),
	re_path('^edit/persona/(?P<id>\d+)/$', views.edit_persona, name='edit_persona'),
	re_path('^view/persona/(?P<id>\d+)/$', views.view_persona, name='view_persona'),
]
