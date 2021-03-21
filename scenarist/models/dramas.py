"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""

from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel


class Drama(StoryModel):
    class Meta:
        ordering = ['epic', 'chapter','date','title']
    from scenarist.models.epics import Epic
    epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
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
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_episodes(self):
        from scenarist.models.acts import Act
        episodes = Act.objects.filter(drama=self)
        return episodes

    @property
    def is_visible(self):
        return self.visible

    @property
    def get_full_id(self):
        return f'{self.epic.get_full_id}:{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value
        from scenarist.models.acts import Act
        all = Act.objects.filter(drama=self)
        for a in all:
            a.set_pdf(value)
            a.save()
        self.save()

class DramaAdmin(admin.ModelAdmin):
    ordering = ('epic', 'chapter', 'date', 'title',)
    list_display = ('title', 'full_id', 'epic', 'chapter', 'date', 'place', 'is_visible', 'description')
    list_filter = ('epic',)
    search_fields = ('title', 'description')
