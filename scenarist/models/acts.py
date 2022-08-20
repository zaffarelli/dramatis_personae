'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
'''
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel


class Act(StoryModel):
    class Meta:
        ordering = ['chapter','title']
    from scenarist.models.dramas import Drama
    drama = models.ForeignKey(Drama, null=True, on_delete=models.CASCADE)
    # resolution = models.TextField(default='', max_length=2560,blank=True)

    @property
    def challenge(self):
        from scenarist.models.events import Event
        episodes = Event.objects.filter(act=self)
        total = 0
        for e in episodes:
            total += e.challenge
        return total

    @property
    def full_chapter(self):
        return self.drama.full_chapter+"."+self.chapter

    def get_casting(self):
        """ Bring all avatars rids from all relevant text fields"""
        casting = super().get_casting()
        casting.append(self.fetch_avatars(self.resolution))
        return casting

    def get_absolute_url(self):
        return reverse('act-detail', kwargs={'pk': self.pk})

    def get_episodes(self):
        from scenarist.models.events import Event
        episodes = Event.objects.filter(act=self)
        return episodes

    @property
    def get_full_id(self):
        return f'{self.drama.get_full_id}:{int(self.chapter):02}'


    def set_pdf(self, value=True):
        self.to_PDF = value
        from scenarist.models.events import Event
        all = Event.objects.filter(act=self)
        for e in all:
            e.set_pdf(value)
            e.save()
        self.save()


class ActAdmin(admin.ModelAdmin):
    ordering = ['drama', 'chapter', 'title']
    list_display = ('title', 'full_id', 'drama', 'chapter', 'visible', 'to_PDF', 'date', 'place', 'description')
    list_filter = ['drama', 'visible', 'to_PDF']
    search_fields = ('title', 'description')
