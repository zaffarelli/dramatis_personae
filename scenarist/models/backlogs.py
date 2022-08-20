"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel

BACKLOG_CATEGORIES = (
    ('NC','Non Categorized'),
    ('FA','Factions'),
    ('OC','Occult'),
    ('TK','Technology'),
    ('SP','Spaceships'),
    ('CO','Combat'),
)


class Backlog(StoryModel):
    """
    A backlog is a piece of information concerning a special rule, a special place, a special situation,
    a piece of setting. It can be included in multiple adventures as it is a pure reference
    """
    class Meta:
        ordering = ['chapter', 'title']
    category = models.CharField(max_length=2, default='NC', choices=BACKLOG_CATEGORIES)
    reference = models.CharField(max_length=128, default='', blank=True)

    @property
    def full_chapter(self):
        return self.chapter

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('backlog-detail', kwargs={'pk': self.pk})

    @property
    def get_full_id(self):
        return f'{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value


class BacklogAdmin(admin.ModelAdmin):
    ordering = ['chapter', 'title']
    list_display = ['title', 'full_id', 'chapter', 'date', 'place', 'description']
    list_filter = ['category']
    search_fields = ['description', 'title']
