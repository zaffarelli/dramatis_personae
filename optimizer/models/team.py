"""
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
"""
from django.db import models
from django.contrib import admin
from collector.models.character import Character
from collector.models.campaign import Campaign


class Team(models.Model):
    """ I don't know exactly what I wanted to do with that team model...
    """
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=256, unique=True)
    active = models.BooleanField(default=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s (%d)"%(self.name,self.population)

    @property
    def population(self):
        return len(self.teammate_set.all())

    @property
    def members(self):
        lst = []
        for x in self.teammate_set.all():
            str = f'{x.character.full_name}'
            if x.character.player:
                str += f' [{x.character.player}]'
            if x.seat:
                str += f' [{x.seat.upper()}]'
            lst.append(str)
        return ", ".join(lst)


class TeamMate(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    seat = models.CharField(default='', blank=True, null=True, max_length=256)


class TeamMateInline(admin.TabularInline):
    model = TeamMate


class TeamAdmin(admin.ModelAdmin):
    model = Team
    inlines = [ TeamMateInline ]
    list_display = ['name', 'active', 'population', 'members', 'campaign']
    list_filter = ['active']
