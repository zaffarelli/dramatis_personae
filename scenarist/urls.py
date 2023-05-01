"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.urls import re_path
from scenarist.views.cards import CardDeleteView, CardDetailView, CardUpdateView, add_card
from scenarist.views.pdfs import build_config_pdf


urlpatterns = [
    re_path('^cards/(?P<pk>\d+)/view/$', CardDetailView.as_view(), name='card-detail'),
    re_path('^cards/(?P<pk>\d+)/edit/$', CardUpdateView.as_view(), name='card-update'),
    re_path('^cards/(?P<pk>\d+)/delete/$', CardDeleteView.as_view(), name='card-delete'),
    re_path('^cards/add/$', add_card, name='card-add'),

    re_path('^ajax/build_config_pdf/$', build_config_pdf, name='build_config_pdf'),

]
