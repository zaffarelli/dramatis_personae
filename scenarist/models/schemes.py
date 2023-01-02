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


class Scheme(StoryModel):
    """
    A scheme is part of an adventure. It's something that happens at some time.
    """

    class Meta:
        ordering = ['chapter', 'name']

    from scenarist.models.adventures import Adventure
    adventure = models.ForeignKey(Adventure, null=True, on_delete=models.CASCADE)
    from scenarist.models.backlogs import Backlog
    backlogs = models.ManyToManyField(Backlog, blank=True)

    @property
    def full_chapter(self):
        return f"{self.full_id}.{self.name}"

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('scheme-detail', kwargs={'pk': self.pk})

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

    @property
    def get_full_id(self):
        return f':{self.chapter:02}'

    def set_pdf(self, value=True):
        self.to_PDF = value

    def to_json(self):
        """ Returns JSON of object """
        from scenarist.utils.tools import json_default
        jst = super().to_json()
        job = json.loads(jst)
        # job['fullchapter'] = self.full_chapter
        return job


class SchemeAdmin(admin.ModelAdmin):
    ordering = ['chapter', 'name']
    list_display = ['name', 'full_id',  'chapter', 'date_offset', 'dt', 'place', 'linked_backlogs', 'description']
    list_filter = []
    search_fields = ['description', 'name', 'resolution']
