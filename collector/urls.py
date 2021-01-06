'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.conf.urls import url
from django.urls import path, re_path

from collector.views.characters import CharacterUpdateView, customize_ba, customize_bc, \
    customize_skill, customize_ba_del, customize_bc_del, skill_pick, attr_pick, customize_weapon, customize_weapon_del, \
    customize_armor, customize_armor_del, customize_shield, customize_shield_del, customize_ritual, customize_ritual_del
from collector.views.investigators import InvestigatorUpdateView
from collector.views.frontend import index, view_by_rid, toggle_public, toggle_spotlight, get_list, add_avatar, \
    get_storyline, conf_details, recalc_avatar, heartbeat, show_jumpweb, \
    show_todo, pdf_show, wa_export_character, show_orbital_map
from collector.views.backend import recalc, export, xls_update, pdf_character, gss_update, pdf_rules, roll_dice, campaign_css
from collector.views.misc_chart import get_chardar, get_population_statistics, get_keywords
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from collector.views.user import do_login, do_profile


urlpatterns = [
    path('', index, name='index'),
    re_path('^api/recalc/$', recalc, name='recalc'),
    re_path('^export/$', export, name='export'),
    re_path('^xls_update/$', xls_update, name='xls_update'),
    re_path('^gss_update/$', gss_update, name='gss_update'),
    re_path('^api/heartbeat/$', heartbeat, name='heartbeat'),


    # Campaign Specific
    re_path('^investigators/(?P<pk>\d+)/edit/$', InvestigatorUpdateView.as_view(), name='edit_investigator'),
    re_path('^characters/(?P<pk>\d+)/edit/$', CharacterUpdateView.as_view(), name='edit_character'),

    # Generic / Multi-campaign compliant
    re_path('^ajax/recalc/avatar/(?P<id>\d+)/$', recalc_avatar, name='recalc_avatar'),
    re_path('^ajax/add/avatar/(?P<slug>[\w-]+)/$', add_avatar, name='add_avatar'),

    re_path('^ajax/roll_dice/(?P<slug>[\w-]+)/$', roll_dice, name='roll_dice'),


    re_path('^ajax/wa_export/character/(?P<id>\d+)/$', wa_export_character, name='wa_export_character'),
    re_path('^ajax/pdf/character/(?P<id>\d+)/$', pdf_character, name='pdf_character'),
    re_path('^ajax/list/(?P<slug>[\w-]+)/(?P<id>\d+)/$', get_list, name='get_list'),
    re_path('^ajax/storyline/(?P<slug>[\w-]+)/$', get_storyline, name='get_storyline'),


    re_path('^ajax/conf_details/$', conf_details, name='conf_details'),


    re_path('^todo/show$', show_todo, name='show_todo'),
    re_path('^ajax/build_pdf_rules/$', pdf_rules, name='pdf_rules'),
    re_path('^api/chardar/(?P<id>\d+)/$', get_chardar, name='get_chardar'),
    re_path('^api/popstats/$', get_population_statistics, name='get_popstats'),
    re_path('^api/keywords/$', get_keywords, name='get_keywords'),
    re_path('^pdf/(?P<slug>[\w-]+)/$', pdf_show, name='pdf_show'),
    re_path('^toggle/(?P<id>\d+)/public$', toggle_public, name='toggle_public'),
    re_path('^toggle/(?P<id>\d+)/spotlight$', toggle_spotlight, name='toggle_spotlight'),
    re_path('^ajax/view/by_rid/(?P<slug>[\w-]+)/$', view_by_rid, name='view_by_rid'),
    re_path('^ajax/character/add/skill/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_skill,
                          name='customize_skill'),
    re_path('^ajax/character/add/ba/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ba,
                          name='customize_ba'),
    re_path('^ajax/character/add/bc/(?P<avatar>\d+)/(?P<item>\d+)/$', customize_bc, name='customize_bc'),
    re_path('^ajax/character/del/ba/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ba_del,
                          name='customize_ba_del'),
    re_path('^ajax/character/del/bc/(?P<avatar>\d+)/(?P<item>\d+)/$', customize_bc_del,
                          name='customize_bc_del'),
    re_path('^ajax/character/pick/skill/(?P<avatar>\d+)/(?P<item>\d+)/(?P<offset>\d+)/$', skill_pick,
                          name='skill_pick'),
    re_path('^ajax/character/pick/attr/(?P<avatar>\d+)/(?P<item>\w+)/(?P<offset>\d+)/$', attr_pick,
                          name='attr_pick'),
    re_path('^ajax/character/add/weapon/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_weapon,
                          name='customize_weapon'),
    re_path('^ajax/character/add/armor/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_armor,
                          name='customize_armor'),
    re_path('^ajax/character/add/shield/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_shield,
                          name='customize_shield'),
    re_path('^ajax/character/add/ritual/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ritual,
                          name='customize_ritual'),
    re_path('^ajax/character/del/weapon/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_weapon_del,
                          name='customize_weapon_del'),
    re_path('^ajax/character/del/armor/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_armor_del,name='customize_armor_del'),
    re_path('^ajax/character/del/shield/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_shield_del, name='customize_shield_del'),
    re_path('^ajax/character/del/ritual/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ritual_del, name='customize_ritual_del'),
    re_path('^ajax/login/$', do_login, name="login"),
    re_path('^ajax/profile/$', do_profile, name="profile"),
    re_path('^ajax/logout/$', LogoutView.as_view(), name="logout"),
    re_path('^jumpweb/show$', show_jumpweb, name='show_jumpweb'),
    re_path('^orbital_map/show/(?P<id>[\d]+)/$', show_orbital_map, name='show_orbital_map'),

    re_path('^collector/campaign.css$', campaign_css, name='campaign_css'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
