"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.urls import re_path
from scenarist.views.epics import EpicDetailView, EpicUpdateView
from scenarist.views.dramas import DramaDetailView, DramaUpdateView, add_drama, DramaDeleteView
from scenarist.views.acts import ActDetailView, ActUpdateView, add_act, ActDeleteView
from scenarist.views.events import EventDetailView, EventUpdateView, add_event, EventDeleteView
from scenarist.views.adventures import AdventureDetailView, AdventureUpdateView, AdventureDeleteView, add_adventure
from scenarist.views.scenes import SceneDetailView, SceneUpdateView, SceneDeleteView, add_scene
from scenarist.views.schemes import SchemeDeleteView, SchemeDetailView, SchemeUpdateView, add_scheme
from scenarist.views.cards import CardDeleteView, CardDetailView, CardUpdateView, add_card
from scenarist.views.backlogs import BacklogDeleteView, BacklogDetailView, add_backlog, BacklogUpdateView
from scenarist.views.pdfs import build_config_pdf
from scenarist.views.quizz import quizz_reroll

urlpatterns = [
    re_path('^epics/(?P<pk>\d+)/view/$', EpicDetailView.as_view(), name='epic-detail'),
    re_path('^epics/(?P<pk>\d+)/edit/$', EpicUpdateView.as_view(), name='epic-update'),

    re_path('^dramas/(?P<pk>\d+)/view/$', DramaDetailView.as_view(), name='drama-detail'),
    re_path('^dramas/(?P<pk>\d+)/edit/$', DramaUpdateView.as_view(), name='drama-update'),
    re_path('^dramas/add/$', add_drama, name='drama-add'),
    re_path('^dramas/(?P<pk>\d+)/delete/$', DramaDeleteView.as_view(), name='drama-delete'),

    re_path('^acts/(?P<pk>\d+)/view/$', ActDetailView.as_view(), name='act-detail'),
    re_path('^acts/(?P<pk>\d+)/edit/$', ActUpdateView.as_view(), name='act-update'),
    re_path('^acts/add/$', add_act, name='act-add'),
    re_path('^acts/(?P<pk>\d+)/delete/$', ActDeleteView.as_view(), name='act-delete'),

    re_path('^events/(?P<pk>\d+)/view/$', EventDetailView.as_view(), name='event-detail'),
    re_path('^events/(?P<pk>\d+)/edit/$', EventUpdateView.as_view(), name='event-update'),
    re_path('^events/add/$', add_event, name='event-add'),
    re_path('^events/(?P<pk>\d+)/delete/$', EventDeleteView.as_view(), name='event-delete'),

    re_path('^adventures/(?P<pk>\d+)/view/$', AdventureDetailView.as_view(), name='adventure-detail'),
    re_path('^adventures/(?P<pk>\d+)/edit/$', AdventureUpdateView.as_view(), name='adventure-update'),
    re_path('^adventures/(?P<pk>\d+)/delete/$', AdventureDeleteView.as_view(), name='adventure-delete'),
    re_path('^adventures/add/$', add_adventure, name='adventure-add'),

    re_path('^backlogs/(?P<pk>\d+)/view/$', BacklogDetailView.as_view(), name='backlog-detail'),
    re_path('^backlogs/(?P<pk>\d+)/edit/$', BacklogUpdateView.as_view(), name='backlog-update'),
    re_path('^backlogs/(?P<pk>\d+)/delete/$', BacklogDeleteView.as_view(), name='backlog-delete'),
    re_path('^backlogs/add/$', add_backlog, name='backlog-add'),

    re_path('^scenes/(?P<pk>\d+)/view/$', SceneDetailView.as_view(), name='scene-detail'),
    re_path('^scenes/(?P<pk>\d+)/edit/$', SceneUpdateView.as_view(), name='scene-update'),
    re_path('^scenes/(?P<pk>\d+)/delete/$', SceneDeleteView.as_view(), name='scene-delete'),
    re_path('^scenes/add/$', add_scene, name='scene-add'),

    re_path('^schemes/(?P<pk>\d+)/view/$', SchemeDetailView.as_view(), name='scheme-detail'),
    re_path('^schemes/(?P<pk>\d+)/edit/$', SchemeUpdateView.as_view(), name='scheme-update'),
    re_path('^schemes/(?P<pk>\d+)/delete/$', SchemeDeleteView.as_view(), name='scheme-delete'),
    re_path('^schemes/add/$', add_scheme, name='scheme-add'),

    re_path('^cards/(?P<pk>\d+)/view/$', CardDetailView.as_view(), name='card-detail'),
    re_path('^cards/(?P<pk>\d+)/edit/$', CardUpdateView.as_view(), name='card-update'),
    re_path('^cards/(?P<pk>\d+)/delete/$', CardDeleteView.as_view(), name='card-delete'),
    re_path('^cards/add/$', add_card, name='card-add'),

    re_path('^ajax/build_config_pdf/$', build_config_pdf, name='build_config_pdf'),

    # re_path('^ajax/quizz/(?P<quizz_id>\d+)/question/(?P<question_num>\d+)/tag/(?P<tag>\w+)/reroll/$', quizz_reroll,
    #         name='quizz_reroll'),

]
