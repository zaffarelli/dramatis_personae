"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel


class Scheme(StoryModel):
    """
    A scheme is part of an adventure. It's something that happens at some time.
    """

    class Meta:
        ordering = ['chapter', 'title']

    from scenarist.models.adventures import Adventure
    adventure = models.ForeignKey(Adventure, null=True, on_delete=models.CASCADE)

    @property
    def full_chapter(self):
        return self.adventure.full_chapter + "." + self.chapter

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('scheme-detail', kwargs={'pk': self.pk})

    @property
    def get_full_id(self):
        return f'{self.adventure.get_full_id}:{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value


class SchemeAdmin(admin.ModelAdmin):
    ordering = ('adventure', 'chapter', 'title',)
    list_display = ('title', 'full_id', 'adventure', 'chapter', 'date', 'place', 'description')
    list_filter = ('adventure',)
    search_fields = ('description', 'title', 'resolution')
