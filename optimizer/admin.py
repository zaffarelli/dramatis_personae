from django.contrib import admin
from optimizer.models.team import Team, TeamAdmin

# Register your models here.
admin.site.register(Team, TeamAdmin)
