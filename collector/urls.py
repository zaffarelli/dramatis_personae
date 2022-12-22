"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.urls import re_path
from collector.views.characters import CharacterUpdateView, customize_ba, customize_bc, \
    customize_skill, customize_ba_del, customize_bc_del, skill_pick, attr_pick, customize_weapon, customize_weapon_del, \
    customize_armor, customize_armor_del, customize_shield, customize_shield_del, customize_ritual, customize_ritual_del

from collector.views.frontend import index, toggle_public, toggle_spotlight, get_list, add_avatar, \
    get_storyline, conf_details, recalc_avatar, heartbeat, \
    show_todo, pdf_show, wa_export_character, tile_avatar, ghostmark_test, display_sheet, display_sessionsheet, switch_epic, deep_toggle, all_epics,  all_spaceships, grab_avatar, handle_cards
from collector.views.backend import export, xls_update, pdf_character, gss_update, gss_summary, pdf_rules, roll_dice, \
    bloke_selector, run_audit, epic_deck, svg_to_pdf, save_sequence, load_sequence
from collector.views.misc_chart import get_population_statistics, get_keywords
from django.contrib.auth.views import LogoutView
from collector.views.user import do_login, do_profile, user_friends, user_foes, user_others, user_persystem

urlpatterns = [
    re_path('^$', index, name='index'),
    # re_path('^ajax/recalc/$', recalc, name='recalc'),
    re_path('^ajax/export/$', export, name='export'),
    re_path('^ajax/xls_update/$', xls_update, name='xls_update'),
    re_path('^ajax/gss_update/$', gss_update, name='gss_update'),
    re_path('^ajax/gss_summary/$', gss_summary, name='gss_summary'),

    # re_path('^investigators/(?P<pk>\d+)/edit/$', InvestigatorUpdateView.as_view(), name='edit_investigator'),
    re_path('^ajax/edit/avatar/(?P<pk>\d+)/$', CharacterUpdateView.as_view(), name='edit_character'),
    re_path('^ajax/sheet/avatar/(?P<pk>\d+)/$', display_sheet, name='display_sheet'),
    re_path('^ajax/sessionsheet/(?P<slug>\w+)/$', display_sessionsheet, name='display_sessionsheet'),
    re_path('^ajax/tile/avatar/(?P<pk>\d+)/$', tile_avatar, name='tile_avatar'),
    re_path('^ajax/recalc/avatar/(?P<id>\d+)/$', recalc_avatar, name='recalc_avatar'),
    re_path('^ajax/grab/avatar/(?P<id>\d+)/$', grab_avatar, name='grab_avatar'),
    re_path('^ajax/add_avatar/(?P<slug>[\w+]+)/$', add_avatar, name='add_avatar'),
    re_path('^ajax/deep_toggle/(?P<slug>[\w+]+)/(?P<id>\d+)/$', deep_toggle, name='deep_toggle'),

    re_path('^ajax/epic/(?P<id>[\d+]+)/$', switch_epic, name='switch_epic'),

    re_path('^ajax/roll_dice/(?P<slug>[\w-]+)/$', roll_dice, name='roll_dice'),
    re_path('^ajax/wa_export/character/(?P<id>\d+)/$', wa_export_character, name='wa_export_character'),
    re_path('^ajax/pdf/character/(?P<id>\d+)/$', pdf_character, name='pdf_character'),
    re_path('^ajax/search/(?P<slug>[\w-]+)/(?P<id>\d+)/$', get_list, name='get_list'),
    re_path('^ajax/storyline/(?P<slug>[\w-]+)/$', get_storyline, name='get_storyline'),
    re_path('^ajax/conf_details/$', conf_details, name='conf_details'),
    re_path('^ajax/todo/$', show_todo, name='show_todo'),
    re_path('^ajax/build_pdf_rules/$', pdf_rules, name='pdf_rules'),

    re_path('^api/heartbeat/$', heartbeat, name='heartbeat'),
    re_path('^ajax/statistics/$', get_population_statistics, name='get_popstats'),
    re_path('^api/keywords/$', get_keywords, name='get_keywords'),
    re_path('^pdf/(?P<slug>[\w-]+)/$', pdf_show, name='pdf_show'),
    re_path('^toggle/(?P<id>\d+)/public$', toggle_public, name='toggle_public'),
    re_path('^toggle/(?P<id>\d+)/spotlight$', toggle_spotlight, name='toggle_spotlight'),
    re_path('^ajax/character/add/skill/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_skill, name='customize_skill'),
    re_path('^ajax/character/add/ba/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ba, name='customize_ba'),
    re_path('^ajax/character/add/bc/(?P<avatar>\d+)/(?P<item>\d+)/$', customize_bc, name='customize_bc'),
    re_path('^ajax/character/del/ba/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ba_del, name='customize_ba_del'),
    re_path('^ajax/character/del/bc/(?P<avatar>\d+)/(?P<item>\d+)/$', customize_bc_del, name='customize_bc_del'),
    re_path('^ajax/character/pick/skill/(?P<avatar>\d+)/(?P<item>\d+)/(?P<offset>\d+)/$', skill_pick,
            name='skill_pick'),
    re_path('^ajax/character/pick/attr/(?P<avatar>\d+)/(?P<item>\w+)/(?P<offset>\d+)/$', attr_pick, name='attr_pick'),
    re_path('^ajax/character/add/weapon/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_weapon, name='customize_weapon'),
    re_path('^ajax/character/add/armor/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_armor, name='customize_armor'),
    re_path('^ajax/character/add/shield/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_shield, name='customize_shield'),
    re_path('^ajax/character/add/ritual/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ritual, name='customize_ritual'),
    re_path('^ajax/character/del/weapon/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_weapon_del,
            name='customize_weapon_del'),
    re_path('^ajax/character/del/armor/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_armor_del,
            name='customize_armor_del'),
    re_path('^ajax/character/del/shield/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_shield_del,
            name='customize_shield_del'),
    re_path('^ajax/character/del/ritual/(?P<avatar>[\d]+)/(?P<item>\d+)/$', customize_ritual_del,
            name='customize_ritual_del'),
    re_path('^ajax/character/svg2pdf/(?P<slug>[\w-]+)/$', svg_to_pdf, name='svg_to_pdf'),
    re_path('^ajax/login/$', do_login, name="login"),
    re_path('^ajax/profile/$', do_profile, name="profile"),
    re_path('^ajax/logout/$', LogoutView.as_view(), name="logout"),
    re_path('^ghostmark/(?P<id>\d+)/$', ghostmark_test, name='ghostmark_test'),
    re_path('^ajax/friends/$', user_friends, name="user_friends"),
    re_path('^ajax/foes/$', user_foes, name="user_foes"),
    re_path('^ajax/others/$', user_others, name="user_others"),
    re_path('^ajax/persystem/$', user_persystem, name="user_persystem"),
    re_path('^ajax/blokes/$', bloke_selector, name="bloke_selector"),
    re_path('^ajax/audit/$', run_audit, name="run_audit"),
    re_path('^ajax/deck/$', epic_deck, name='epic_deck'),
    re_path('^ajax/epics/$', all_epics, name='all_epics'),
    re_path('^ajax/cards/$', handle_cards, name='handle_cards'),
    re_path('^ajax/spaceships/$', all_spaceships, name='all_spaceships'),
    re_path('^ajax/deck/save/$', save_sequence, name='save_sequence'),
    re_path('^ajax/deck/load/$', load_sequence, name='load_sequence'),
]
