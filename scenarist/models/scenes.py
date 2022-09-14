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


class Scene(StoryModel):
    """
    A scene is part of an adventure, and is intimately linked to the what the PC will experience.
    """

    class Meta:
        ordering = ['chapter', 'name']

    from scenarist.models.adventures import Adventure
    adventure = models.ForeignKey(Adventure, null=True, on_delete=models.CASCADE)

    challenge = models.PositiveIntegerField(default=1)
    anchor = models.CharField(default='', max_length=256, blank=True)
    duration = models.PositiveIntegerField(default=60)
    from scenarist.models.backlogs import Backlog
    backlogs = models.ManyToManyField(Backlog, blank=True)

    @property
    def full_chapter(self):
        return "SCE." + self.adventure.full_chapter + "." + self.chapter

    @property
    def linked_backlogs(self):
        list = []
        for item in self.backlogs.all():
            list.append(item.name)
        return list

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    @property
    def get_full_id(self):
        return f'{self.adventure.get_full_id}:{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value

    def to_json(self):
        """ Returns JSON of object """
        from scenarist.utils.tools import json_default
        jst = super().to_json()
        job = json.loads(jst)
        job['fullchapter'] = self.full_chapter
        return job

    @property
    def linked_backlogs_str(self):
        str = "<ul><li>" + "</li><li>".join(self.linked_backlogs) + "</li></ul>"
        return str


class SceneAdmin(admin.ModelAdmin):
    ordering = ['adventure', 'chapter', 'name']
    list_display = ['name', 'full_id', 'adventure', 'chapter', 'date', 'place', 'description']
    list_filter = ['adventure']
    search_fields = ['description', 'name', 'resolution']
