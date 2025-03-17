from django.contrib import admin
from optimizer.models.team import Team, TeamAdmin
from optimizer.models.policy import Policy, PolicyAdmin
from optimizer.models.celestial_ship_cards import CelestialShipCard, CelestialShipCardAdmin

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(CelestialShipCard,CelestialShipCardAdmin)
