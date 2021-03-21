"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel


class Event(StoryModel):
    class Meta:
        ordering = ['chapter','title']
    from scenarist.models.acts import Act
    act = models.ForeignKey(Act, null=True, on_delete=models.CASCADE)
    resolution = models.TextField(default='', max_length=2560,blank=True)
    challenge = models.PositiveIntegerField(default=1)
    anchor = models.CharField(default='', max_length=256, blank=True)

    @property
    def full_chapter(self):
        return self.act.full_chapter+"."+self.chapter

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    @property
    def get_full_id(self):
        return f'{self.act.get_full_id}:{int(self.chapter):02}'

    def set_pdf(self, value=True):
        self.to_PDF = value


class EventAdmin(admin.ModelAdmin):
    ordering = ('act', 'chapter', 'title',)
    list_display = ('title','full_id','act', 'chapter', 'date', 'place', 'description')
    list_filter = ('act',)
    search_fields = ('description', 'title', 'resolution')
