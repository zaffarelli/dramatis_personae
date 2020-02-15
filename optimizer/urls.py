from django.conf.urls import url
from django.urls import path, re_path
from optimizer.views import run_duel


urlpatterns = [
    re_path('^duel/(?P<pka>\d+)/(?P<pkb>\d+)/run', run_duel, name='run-duel'),
]
