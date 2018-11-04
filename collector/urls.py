from django.conf.urls import url
from django.urls import path, re_path
from collector.views.basic import index,recalc,export,xls_update,edit_character,pdf_character,view_character,get_list, skill_touch, add_character
from collector.views.misc_chart import get_chardar

urlpatterns = [
	path('', index, name='index'),
	re_path('^recalc/$', recalc, name='recalc'),
	#re_path('^by_keyword/persona/(?P<keyword>\w+)/$', views.by_keyword_personae, name='by_keyword'),
	#re_path('^by_alliance/persona/(?P<alliancehash>\w+)/$', views.by_alliance_personae, name='by_alliance'),
	#re_path('^by_species/persona/(?P<species>\w+)/$', views.by_species_personae, name='by_species'),
	re_path('^export/$', export, name='export'),
  re_path('^xls_update/$', xls_update, name='xls_update'),
	#re_path('^add/persona/$', views.add_persona, name='add_persona'),
	#re_path('^edit/persona/(?P<id>\d+)/$', views.edit_persona, name='edit_persona'),
  re_path('^ajax/edit/character/(?P<id>\d+)/$', edit_character, name='edit_character'),
  re_path('^ajax/update/character/$', edit_character, name='update_character'),
#	re_path('^drop/persona/(?P<id>\d+)/$', views.CharacterDelete.as_view(), name='drop_persona'),
	#re_path('^view/persona/(?P<id>\d+)/$', views.view_persona, name='view_persona'),
  re_path('^ajax/pdf/character/(?P<id>\d+)/$', pdf_character, name='pdf_character'),
  re_path('^ajax/view/character/(?P<id>\d+)/$', view_character, name='view_character'),
  re_path('^ajax/list/(?P<slug>[\w-]+)/(?P<id>\d+)/$', get_list, name='get_list'),
  re_path('^ajax/skill_touch/$', skill_touch, name='skill_touch'),
  re_path('^ajax/add/character/$', add_character, name='add_character'),
  re_path('^api/chardar/(?P<id>\d+)/$', get_chardar, name='get_chardar'),  
	#re_path('^pdf/persona/(?P<id>\d+)/$', views.persona_as_pdf, name='persona_as_pdf'),
]
