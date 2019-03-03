from django.db import models
from django.contrib import admin


class Config(models.Model):
  class Meta:
    ordering = ['title', 'epic']  
  from scenarist.models.epics import Epic
  from scenarist.models.dramas import Drama
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
  description = models.TextField(max_length=128,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_active = models.BooleanField(default=False)
  smart_code = models.CharField(default='xxxxxx', max_length=6, blank=True)
  current_drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
  
  def __str__(self):
    return '%s' % (self.title)

  def parse_details(self):
    """ Return details from the config epic, dramas and acts    
    """
    from scenarist.models.epics import Epic
    from scenarist.models.dramas import Drama
    from scenarist.models.acts import Act
    from scenarist.models.events import Event
    from collector.utils.fs_fics7 import get_keywords
    
    epic = Epic.objects.get(title = self.epic.title)
    dramas = Drama.objects.filter(epic = epic).order_by('chapter','date')
    context_dramas =[]
    for drama in dramas:
      context_acts = []
      acts = Act.objects.filter(drama = drama).order_by('chapter','date')
      for act in acts:        
        context_events = []
        events = Event.objects.filter(act = act).order_by('chapter','date')
        for event in events:
          context_event = {'title':event.title, 'data': event}
          context_events.append(context_event)
        context_act = {'title':act.title, 'data': act, 'events': context_events}
        context_acts.append(context_act)
      context_drama = {'title':drama.title, 'data': drama, 'acts': context_acts}
      context_dramas.append(context_drama)
    context = {'title':epic.title, 'data': epic, 'dramas': context_dramas}
    context['keywords'] = get_keywords()
    #print(context)
    return context

class ConfigAdmin(admin.ModelAdmin):
  ordering = ['title']


