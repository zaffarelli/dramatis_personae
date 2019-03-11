'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
from django.contrib import admin

from scenarist.models.epics import Epic, EpicAdmin
from scenarist.models.dramas import Drama, DramaAdmin
from scenarist.models.acts import Act, ActAdmin
from scenarist.models.events import Event, EventAdmin

admin.site.register(Epic, EpicAdmin)
admin.site.register(Drama, DramaAdmin)
admin.site.register(Act, ActAdmin)
admin.site.register(Event, EventAdmin)
