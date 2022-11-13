"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
import datetime as dt
from scenarist.models.story_models import StoryModel
import json


class Epic(StoryModel):
    class Meta:
        ordering = ['era', 'name']
    era = models.IntegerField(default=5017, blank=True)
    shortcut = models.CharField(default='xx', max_length=32, blank=True)
    image = models.CharField(default='', max_length=64, blank=True)
    system = models.CharField(default='', max_length=128, blank=True, null=True)

    @property
    def printtime(self):
        x = dt.datetime.now().strftime("%Y-%m-%d-%H:%M")
        return x

    @property
    def campaign(self):
        from collector.models.campaign import Campaign
        campaign = Campaign.objects.filter(epic=self)
        return campaign

    @property
    def challenge(self):
        from scenarist.models.dramas import Drama
        episodes = Drama.objects.filter(epic=self)
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
        for rid in list:
            ch = Character.objects.filter(rid=rid).first()
            it = ch.full_name
            if ch.is_dead:
                it += "(&dagger;)"
            if ch.balanced:
                ok.append(it)
            else:
                nok.append(it)
        return ", ".join(ok)+"<hr/>"+", ".join(nok)


    def dramatis_personae_simple(self):
        list = self.get_full_cast()
        nok = []
        ok = []
        from collector.models.character import Character
        for rid in list:
            ch = Character.objects.filter(rid=rid).first()
            if ch.is_dead:
                option = "(&dagger;)"
            else:
                option = ''
            it = f"<span class='officetag chlink' id='chlink__{ch.rid}'>{ch.full_name} {option}</span>"

            if ch.balanced:
                ok.append(it)
            else:
                nok.append(it)
        return " ".join(ok)+"<br/>"+" ".join(nok)+"<br/>"

    def get_absolute_url(self):
        return reverse('epic-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s (%s)' % (self.name, self.era)

    def get_episodes(self):
        from scenarist.models.dramas import Drama
        episodes = Drama.objects.filter(epic=self)
        if len(episodes) == 0:
            from scenarist.models.adventures import Adventure
            episodes = Adventure.objects.filter(epic=self)
        return episodes

    def get_adventures(self):
        list = []
        adventures = self.adventure_set.all().order_by('chapter')
        for adventure in adventures:
            list.append(adventure.to_json())
        return list

    @property
    def get_full_id(self):
        """ Return subchapters """
        return self.shortcut

    def set_pdf(self, value=True):
        self.to_PDF = value
        from scenarist.models.dramas import Drama
        all = Drama.objects.filter(epic=self)
        for d in all:
            d.set_pdf(value)
            d.save()
        self.save()

    def to_json(self):
        """ Returns JSON of object """
        from scenarist.utils.tools import json_default
        jstr = super().to_json()
        k = json.loads(jstr)
        k['adventures'] = self.get_adventures()
        return k


class EpicAdmin(admin.ModelAdmin):
    ordering = ['era', 'name']
    list_display = ['shortcut', 'era', 'full_id', 'chapter', 'name']
