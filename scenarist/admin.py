#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.contrib import admin

from scenarist.models.epics import Epic, EpicAdmin
from scenarist.models.dramas import Drama, DramaAdmin
from scenarist.models.acts import Act, ActAdmin
from scenarist.models.events import Event, EventAdmin

admin.site.register(Epic, EpicAdmin)
admin.site.register(Drama, DramaAdmin)
admin.site.register(Act, ActAdmin)
admin.site.register(Event, EventAdmin)
