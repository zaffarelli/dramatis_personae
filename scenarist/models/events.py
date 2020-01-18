'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
'''
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

    @property
    def minis(self):
        from collector.models.character import Character
        casting = self.get_casting()
        flat_cast = [c for subcast in casting for c in subcast]
        #print(flat_cast)
        list = []
        for c in flat_cast:
            ch = Character.objects.filter(rid=c).first()
            if ch.player == "":
                list.append(ch)
        return list

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

class EventAdmin(admin.ModelAdmin):
  ordering = ('chapter','title',)
