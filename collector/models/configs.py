'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
import random

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

  def get_popstats_races(self):
    from collector.models.characters import Character
    all = Character.objects.filter(epic=self.epic)
    inside_labels = []
    inside_datasets = []
    dat = []
    back = []
    border = []
    idx = 255
    arrfetch = {}
    for c in all:
      if arrfetch.get(c.castspecies.species) is None:
        arrfetch[c.castspecies.species] = 1
      else:
        arrfetch[c.castspecies.species] += 1
        
    for x in arrfetch:
      inside_labels.append(x)
      dat.append(arrfetch[x])
      col = '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])+'C0'
      back.append('%s'%(col))
      border.append('#C0C0C0C0')
      idx -= 32
  
    inside_datasets = [{
      'label': 'Species',
      'data': dat,
      'backgroundColor': back,
      'borderColor': border,
      'borderWidth': 1,
      'fill': False
    }]
    
    data = {
      'labels': inside_labels,
      'datasets': inside_datasets
    }
    return data

  def get_popstats_alliances(self):
    from collector.models.characters import Character
    all = Character.objects.filter(epic=self.epic,alliance__icontains='House')
    inside_labels = []
    inside_datasets = []
    dat = []
    back = []
    border = []
    idx = 255
    arrfetch = {}
    for c in all:
      if arrfetch.get(c.alliance) is None:
        arrfetch[c.alliance] = 1
      else:
        arrfetch[c.alliance] += 1
        
    for x in arrfetch:
      inside_labels.append(x)
      dat.append(arrfetch[x])
      col = '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])+'C0'
      back.append('%s'%(col))
      border.append('#C0C0C0C0')
      idx -= 32
  
    inside_datasets = [{
      'label': 'Species',
      'data': dat,
      'backgroundColor': back,
      'borderColor': border,
      'borderWidth': 1,
      'fill': False
    }]
    
    data = {
      'labels': inside_labels,
      'datasets': inside_datasets
    }
    return data

class ConfigAdmin(admin.ModelAdmin):
  ordering = ['title']


