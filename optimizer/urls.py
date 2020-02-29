'''
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
'''
from django.conf.urls import url
from django.urls import path, re_path
from optimizer.views import run_duel, run_100_duels, run_fencing_tournament


urlpatterns = [
    re_path('^duel/(?P<pka>\d+)/(?P<pkb>\d+)/run', run_duel, name='run-duel'),
    re_path('^duels/(?P<pka>\d+)/(?P<pkb>\d+)/run', run_100_duels, name='run-100-duels'),
    re_path('^tournament/run', run_fencing_tournament, name='run-fencing-tournament'),
]
