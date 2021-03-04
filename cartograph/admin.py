from django.contrib import admin
from cartograph.models.system import System, SystemAdmin, OrbitalItem, OrbitalItemAdmin

admin.site.register(System, SystemAdmin)
admin.site.register(OrbitalItem, OrbitalItemAdmin)