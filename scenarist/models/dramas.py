'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
'''
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel
import json
import time

class Drama(StoryModel):
    class Meta:
        ordering = ['epic','chapter','date','title']

    from scenarist.models.epics import Epic
    epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
    #players = models.TextField(max_length=640,default='',blank=True)
    resolution = models.TextField(default='', max_length=2560,blank=True)

    @property
    def full_chapter(self):
        return self.chapter

    @property
    def challenge(self):
        from scenarist.models.acts import Act
        episodes = Act.objects.filter(drama=self)
        total = 0
        for e in episodes:
            total += e.challenge
        return total

    @property
    def dramatis_personae(self):
        list = self.get_full_cast()
        nok = []
        ok = []
        from collector.models.character import Character
        for x in list:
            ch = Character.objects.filter(rid=x).first()
            it = ch.full_name
            if ch.is_dead:
                it += "(&dagger;)"
            if ch.balanced:
                ok.append(it)
            else:
                nok.append(it)

        return ", ".join(ok)+"<hr/>"+", ".join(nok)

    def get_absolute_url(self):
        return reverse('drama-detail', kwargs={'pk': self.pk})

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        #casting.append(self.fetch_avatars(self.players))
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_episodes(self):
        from scenarist.models.acts import Act
        episodes = Act.objects.filter(drama=self)
        return episodes



class DramaAdmin(admin.ModelAdmin):
  ordering = ('epic','chapter','date','title',)
  list_display = ('title','epic')
