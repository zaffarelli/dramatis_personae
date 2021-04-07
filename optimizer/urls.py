'''
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
'''
from django.conf.urls import url
from django.urls import path, re_path
from optimizer.views import run_duel, run_100_duels, run_fencing_tournament, run_imperial_tournament


urlpatterns = [
    re_path('^ajax/run_duel/(?P<slug>\w+)/$', run_duel, name='run-duel'),
    re_path('^ajax/run_100_duels/(?P<slug>\w+)/$', run_100_duels, name='run-100-duels'),
    re_path('^ajax/fencing_tournament/$', run_fencing_tournament, name='run-fencing-tournament'),
    re_path('^ajax/imperial_tournament/$', run_imperial_tournament, name='run-imperial-tournament'),
]
