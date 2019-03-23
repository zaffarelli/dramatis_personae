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

  def prepare_color_set(size=16):
    colorset = []
    idx = 0
    vmin, vmax = 0X33, 0xCC           
    start = [vmax,vmin,vmax]
    while x < size:
      angle = 2*Math.pi / size
      col = '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])+'C0'
      colorset.append(col)
    return colorset

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
    all_nobles = Character.objects.filter(epic=self.epic,caste__icontains='Nobility')
    all_church = Character.objects.filter(epic=self.epic,caste__icontains='Church')
    all_freefolk = Character.objects.filter(epic=self.epic,caste__icontains='Freefolk')
    inside_labels = []
    inside_datasets = []
    dat,dat1,dat2 = [], [], []
    back, back1, back2 = [], [], []
    border, border1, border2 = [], [], []
    nobility = {}
    church = {}
    freefolk = {}
    for c in all_nobles:
      if nobility.get(c.alliance) is None:
        nobility[c.alliance] = 1
      else:
        nobility[c.alliance] += 1

    for c in all_church:
      if church.get(c.alliance) is None:
        church[c.alliance] = 1
      else:
        church[c.alliance] += 1

    for c in all_freefolk:
      if freefolk.get(c.alliance) is None:
        freefolk[c.alliance] = 1
      else:
        freefolk[c.alliance] += 1
        
    for x in nobility:
      inside_labels.append(x)
      dat.append(nobility[x])
      col = '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])+'C0'
      back.append('%s'%(col))
      border.append('#C0C0C0C0')

    for x in church:
      inside_labels.append(x)
      dat1.append(church[x])
      col = '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])+'C0'
      back1.append('%s'%(col))
      border1.append('#C0C0C0C0')

    for x in freefolk:
      inside_labels.append(x)
      dat2.append(freefolk[x])
      col = '#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])+'C0'
      back2.append('%s'%(col))
      border2.append('#C0C0C0C0')

  
    inside_datasets.append({
      'data': dat,
      'backgroundColor': back,
      'borderColor': border,
      'borderWidth': 1,
      'fill': False
    })
    inside_datasets.append({
      'data': dat1,
      'backgroundColor': back1,
      'borderColor': border1,
      'borderWidth': 1,
      'fill': False
    })
    inside_datasets.append({
      'data': dat2,
      'backgroundColor': back2,
      'borderColor': border2,
      'borderWidth': 1,
      'fill': False
    })
    
    data = {
      'labels': inside_labels,
      'datasets': inside_datasets
    }
    return data

class ConfigAdmin(admin.ModelAdmin):
  ordering = ['title']


