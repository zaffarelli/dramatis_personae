#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.conf.urls import url
from django.urls import path, re_path
from scenarist.views.epics import EpicDetailView, EpicUpdate
from scenarist.views.dramas import DramaDetailView, DramaUpdate
from scenarist.views.acts import ActDetailView, ActUpdate
from scenarist.views.events import EventDetailView, EventUpdate

urlpatterns = [
  re_path('^epics/(?P<pk>\d+)/view', EpicDetailView.as_view(), name='epic-detail'),
  re_path('^epics/(?P<pk>\d+)/edit', EpicUpdate.as_view(), name='epic-update'),
  re_path('^dramas/(?P<pk>\d+)/view', DramaDetailView.as_view(), name='drama-detail'),
  re_path('^dramas/(?P<pk>\d+)/edit', DramaUpdate.as_view(), name='drama-update'),
  re_path('^acts/(?P<pk>\d+)/view', ActDetailView.as_view(), name='act-detail'),
  re_path('^acts/(?P<pk>\d+)/edit', ActUpdate.as_view(), name='act-update'),
  re_path('^events/(?P<pk>\d+)/view', EventDetailView.as_view(), name='event-detail'),
  re_path('^events/(?P<pk>\d+)/edit', EventUpdate.as_view(), name='event-update'),
]

