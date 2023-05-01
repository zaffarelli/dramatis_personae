'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
from django.contrib import admin

from scenarist.models.cards import Card, CardAdmin, CardLink, CardLinkAdmin

admin.site.register(CardLink, CardLinkAdmin)
admin.site.register(Card, CardAdmin)
