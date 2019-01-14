#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
#
from django.conf.urls import url
from django.urls import path, re_path
from scenarist.views.epics import EpicDetailView, EpicUpdateView
from scenarist.views.dramas import DramaDetailView, DramaUpdateView, add_drama, DramaDeleteView
from scenarist.views.acts import ActDetailView, ActUpdateView,  add_act, ActDeleteView
from scenarist.views.events import EventDetailView, EventUpdateView,  add_event, EventDeleteView
from scenarist.views.pdfs import build_config_pdf

urlpatterns = [
  re_path('^epics/(?P<pk>\d+)/view', EpicDetailView.as_view(), name='epic-detail'),
  re_path('^epics/(?P<pk>\d+)/edit', EpicUpdateView.as_view(), name='epic-update'),

  re_path('^dramas/(?P<pk>\d+)/view', DramaDetailView.as_view(), name='drama-detail'),
  re_path('^dramas/(?P<pk>\d+)/edit', DramaUpdateView.as_view(), name='drama-update'),
  re_path('^dramas/add', add_drama, name='drama-add'),
  re_path('^dramas/(?P<pk>\d+)/delete', DramaDeleteView.as_view(), name='drama-delete'),

  re_path('^acts/(?P<pk>\d+)/view', ActDetailView.as_view(), name='act-detail'),
  re_path('^acts/(?P<pk>\d+)/edit', ActUpdateView.as_view(), name='act-update'),
  re_path('^acts/add', add_act, name='act-add'),
  re_path('^acts/(?P<pk>\d+)/delete', ActDeleteView.as_view(), name='act-delete'),
  
  re_path('^events/(?P<pk>\d+)/view', EventDetailView.as_view(), name='event-detail'),
  re_path('^events/(?P<pk>\d+)/edit', EventUpdateView.as_view(), name='event-update'),
  re_path('^events/add', add_event, name='event-add'),
  re_path('^events/(?P<pk>\d+)/delete', DramaDeleteView.as_view(), name='event-delete'),

  re_path('^ajax/build_config_pdf/', build_config_pdf, name='build_config_pdf'),
]

