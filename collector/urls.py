'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.conf.urls import url
from django.urls import path, re_path
from collector.views.basic import pdf_show
from collector.views.characters import CharacterDetailView, CharacterUpdateView, customize_ba, customize_bc, customize_skill, customize_ba_del, customize_bc_del, skill_pick, attr_pick, customize_weapon, customize_weapon_del, customize_armor, customize_armor_del, customize_shield, customize_shield_del
from collector.views.frontend import index, view_by_rid, toggle_public, get_list, add_character, get_storyline, conf_details, recalc_character, update_messenger, show_jumpweb #, recalc_pa_character, recalc_skills_character
from collector.views.backend import recalc,export,xls_update,pdf_character, gss_update, pdf_rules
from collector.views.misc_chart import get_chardar, get_population_statistics, get_keywords


urlpatterns = [
	path('', index, name='index'),
	re_path('^recalc/$', recalc, name='recalc'),
	re_path('^export/$', export, name='export'),
    re_path('^xls_update/$', xls_update, name='xls_update'),
    re_path('^gss_update/$', gss_update, name='gss_update'),
    re_path('^ajax/messenger/$', update_messenger, name='update_messenger'),
    re_path('^characters/(?P<pk>\d+)/edit/$', CharacterUpdateView.as_view(), name='edit_character'),
    re_path('^characters/(?P<pk>\d+)/view/$', CharacterDetailView.as_view(), name='view_character'),

    re_path('^ajax/recalc/character/(?P<id>\d+)/$', recalc_character, name='recalc_character'),
    # re_path('^ajax/recalc_pa/character/(?P<id>\d+)/$', recalc_pa_character, name='recalc_pa_character'),
    # re_path('^ajax/recalc_skills/character/(?P<id>\d+)/$', recalc_skills_character, name='recalc_skills_character'),
    re_path('^ajax/pdf/character/(?P<id>\d+)/$', pdf_character, name='pdf_character'),
    re_path('^ajax/list/(?P<slug>[\w-]+)/(?P<id>\d+)/$', get_list, name='get_list'),
    re_path('^ajax/storyline/(?P<slug>[\w-]+)/$', get_storyline, name='get_storyline'),

    re_path('^ajax/add/character/(?P<slug>[\w-]+)/$', add_character, name='add_character'),
    re_path('^ajax/conf_details/$', conf_details, name='conf_details'),
    re_path('^jumpweb/show$', show_jumpweb, name='show_jumpweb'),
    re_path('^ajax/build_pdf_rules/$', pdf_rules, name='pdf_rules'),
    re_path('^api/chardar/(?P<id>\d+)/$', get_chardar, name='get_chardar'),
    re_path('^api/popstats/$', get_population_statistics, name='get_popstats'),
    re_path('^api/keywords/$', get_keywords, name='get_keywords'),
    re_path('^pdf/(?P<slug>[\w-]+)/$', pdf_show, name='pdf_show'),
    re_path('^toggle/(?P<id>\d+)/public$', toggle_public, name='toggle_public'),
    re_path('^ajax/view/by_rid/(?P<slug>[\w-]+)/$', view_by_rid, name='view_by_rid'),
    re_path('^ajax/character/add/skill/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_skill,name='customize_skill'),
    re_path('^ajax/character/add/ba/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_ba,name='customize_ba'),
    re_path('^ajax/character/add/bc/(?P<avatar>\d+)/(?P<item>\d+)/$',customize_bc,name='customize_bc'),
    re_path('^ajax/character/del/ba/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_ba_del,name='customize_ba_del'),
    re_path('^ajax/character/del/bc/(?P<avatar>\d+)/(?P<item>\d+)/$',customize_bc_del,name='customize_bc_del'),
    re_path('^ajax/character/pick/skill/(?P<avatar>\d+)/(?P<item>\d+)/(?P<offset>\d+)/$',skill_pick,name='skill_pick'),
    re_path('^ajax/character/pick/attr/(?P<avatar>\d+)/(?P<item>\w+)/(?P<offset>\d+)/$',attr_pick,name='attr_pick'),
    re_path('^ajax/character/add/weapon/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_weapon,name='customize_weapon'),
    re_path('^ajax/character/add/armor/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_armor,name='customize_armor'),
    re_path('^ajax/character/add/shield/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_shield,name='customize_shield'),
    re_path('^ajax/character/del/weapon/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_weapon_del,name='customize_weapon_del'),
    re_path('^ajax/character/del/armor/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_armor_del,name='customize_armor_del'),
    re_path('^ajax/character/del/shield/(?P<avatar>[\d]+)/(?P<item>\d+)/$',customize_shield_del,name='customize_shield_del'),
]
