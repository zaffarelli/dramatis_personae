from django.contrib import admin
from optimizer.models.team import Team, TeamAdmin
from optimizer.models.policy import Policy, PolicyAdmin

# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(Policy, PolicyAdmin)
