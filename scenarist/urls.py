#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        


from django.conf.urls import url
from django.urls import path, re_path
from scenarist.views.events import *
from scenarist.views.dramas import *

urlpatterns = [
  re_path('^events/(?P<id>\d+)/edit$', edit_event, name='edit_event'),
  re_path('^events/(?P<id>\d+)/view$', view_event, name='view_event'),
  re_path('^dramas/(?P<pk>\d+)/view', DramaDetailView.as_view(), name='drama-detail'),
  re_path('^dramas/(?P<pk>\d+)/edit', DramaUpdate.as_view(), name='drama-update'),
]

