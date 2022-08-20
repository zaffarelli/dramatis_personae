"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel


class Adventure(StoryModel):
    """
    An adventure is part of a campaign, like a big chapter. It is primarily a collection of scenes and schemes.
    """

    class Meta:
        ordering = ['chapter', 'title']

    from scenarist.models.epics import Epic
    epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
    total_rewards = models.TextField(default='', max_length=2560, blank=True)
    total_challenge = models.PositiveIntegerField(default=0)
    from scenarist.models.backlogs import Backlog
    backlogs = models.ManyToManyField(Backlog)

    @property
    def full_chapter(self):
        return self.epic.full_chapter + "." + self.chapter

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('adventure-detail', kwargs={'pk': self.pk})

    @property
    def get_full_id(self):
        return f'{self.epic.get_full_id}:{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value


class AdventureAdmin(admin.ModelAdmin):
    ordering = ['epic', 'chapter', 'title']
    list_display = ['title', 'full_id', 'epic', 'chapter', 'date', 'place', 'description']
    list_filter = ['epic']
    search_fields = ['description', 'title', 'resolution']
