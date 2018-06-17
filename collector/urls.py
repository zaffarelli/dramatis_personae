from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	re_path('^recalc/$', views.recalc, name='recalc'),
	#re_path('^by_keyword/persona/(?P<keyword>\w+)/$', views.by_keyword_personae, name='by_keyword'),
	#re_path('^by_alliance/persona/(?P<alliancehash>\w+)/$', views.by_alliance_personae, name='by_alliance'),
	#re_path('^by_species/persona/(?P<species>\w+)/$', views.by_species_personae, name='by_species'),
	re_path('^export/$', views.export, name='export'),
	#re_path('^add/persona/$', views.add_persona, name='add_persona'),
	#re_path('^edit/persona/(?P<id>\d+)/$', views.edit_persona, name='edit_persona'),
  re_path('^ajax/edit/character/(?P<id>\d+)/$', views.edit_character, name='edit_character'),
  re_path('^ajax/update/character/$', views.edit_character, name='update_character'),
#	re_path('^drop/persona/(?P<id>\d+)/$', views.CharacterDelete.as_view(), name='drop_persona'),
	#re_path('^view/persona/(?P<id>\d+)/$', views.view_persona, name='view_persona'),
  re_path('^ajax/pdf/character/(?P<id>\d+)/$', views.pdf_character, name='pdf_character'),
  re_path('^ajax/view/character/(?P<id>\d+)/$', views.view_character, name='view_character'),
  re_path('^ajax/list/(?P<slug>[\w-]+)/(?P<id>\d+)/$', views.get_list, name='get_list'),
  re_path('^ajax/skill_touch/$', views.skill_touch, name='skill_touch'),
  re_path('^ajax/add/character/$', views.add_character, name='add_character'),  
	#re_path('^pdf/persona/(?P<id>\d+)/$', views.persona_as_pdf, name='persona_as_pdf'),
]
