"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel
import json


class Adventure(StoryModel):
    """
    An adventure is part of a campaign, like a big chapter. It is primarily a collection of scenes and schemes.
    """
    class Meta:
        ordering = ['chapter', 'name']
    from scenarist.models.epics import Epic
    epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
    total_rewards = models.TextField(default='', max_length=2560, blank=True)
    total_challenge = models.PositiveIntegerField(default=0)
    from scenarist.models.backlogs import Backlog
    backlogs = models.ManyToManyField(Backlog, blank=True)

    @property
    def full_chapter(self):
        return self.epic.chapter + "." + self.chapter

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    @property
    def linked_backlogs(self):
        list = []
        for item in self.backlogs.all():
            list.append(item.name)
        return list

    @property
    def linked_backlogs_str(self):
        str = "<ul><li>"+"</li><li>".join(self.linked_backlogs)+"</li></ul>"
        return str

    def get_absolute_url(self):
        return reverse('adventure-detail', kwargs={'pk': self.pk})

    @property
    def get_full_id(self):
        return f'{self.epic.get_full_id}:{self.chapter:02}'

    def set_pdf(self, value=True):
        self.to_PDF = value

    def to_json(self):
        """ Returns JSON of object """
        from scenarist.utils.tools import json_default
        jst = super().to_json()
        job = json.loads(jst)
        job['fullchapter'] = self.full_chapter
        scenes = []
        for scene in self.scene_set.all().order_by('chapter','place','-dt'):
            scenes.append(scene.to_json())
        job['scenes'] = scenes
        schemes = []
        for scheme in self.scheme_set.all().order_by('chapter','place','-dt'):
            schemes.append(scheme.to_json())
        job['schemes'] = schemes
        return job

    def get_episodes(self):
        from scenarist.models.scenes import Scene
        episodes = Scene.objects.filter(adventure=self)
        return episodes


class AdventureAdmin(admin.ModelAdmin):
    ordering = ['epic', 'chapter', 'name']
    list_display = ['name', 'full_id', 'epic', 'chapter', 'date_offset', 'place', 'description']
    list_filter = ['epic']
    search_fields = ['description', 'name', 'resolution']
