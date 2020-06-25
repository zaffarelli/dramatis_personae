'''
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character

class Team(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=256, unique=True)


    def __str__(self):
        return "%s (%d)"%(self.name,self.population)

    @property
    def population(self):
        return len(self.teammate_set.all())
    @property
    def members(self):
        lst = []
        for x in self.teammate_set.all():
            str = "%s"%(x.character.full_name)
            if x.character.player:
                str += " [%s]"%(x.character.player)
            lst.append(str)
        return ", ".join(lst)

class TeamMate(models.Model):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    character = models.ForeignKey(Character,on_delete=models.CASCADE)

class TeamMateInline(admin.TabularInline):
    model = TeamMate

class TeamAdmin(admin.ModelAdmin):
    model = Team
    inlines = [
        TeamMateInline,
    ]
    list_display = ('name','population','members')
