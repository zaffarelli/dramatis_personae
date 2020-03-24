'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
import random
import math

class Config(models.Model):
  class Meta:
    ordering = ['title', 'epic']
  from scenarist.models.epics import Epic
  from scenarist.models.dramas import Drama
  title = models.CharField(default='aaa', max_length=128, blank=True, unique=True)
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
    return context

  def prepare_colorset(self, size = 16):
    colorset = []
    hcolorset = []
    colval = '456789AB'
    idx = 0
    while idx < size:
      com = '%s%s%s%s%s%s'%(random.sample(colval,1)[0],random.sample(colval,1)[0],random.sample(colval,1)[0],random.sample(colval,1)[0],random.sample(colval,1)[0],random.sample(colval,1)[0])
      col = '#'+com+'88'
      hcol = '#'+com+'FF'
      colorset.append(col)
      hcolorset.append(hcol)
      idx += 1
    return colorset, hcolorset

  def get_chart(self,o,filter='',pattern='',type='bar',bar_property=''):
    from collector.models.character import Character
    if pattern:
        all = Character.objects.filter(epic=self.epic,is_visible=True).filter(**{filter:pattern}).order_by(o)
    else:
        all = Character.objects.filter(epic=self.epic,is_visible=True).order_by(o)
    inside_labels = []
    inside_datasets = []
    dat = []
    back = []
    border = []
    arrfetch = {}
    for c in all:
        value = c.__dict__[o]
        if bar_property=='':
           if arrfetch.get(value) is None:
               arrfetch[value] = 1
           else:
               arrfetch[value] += 1
        else:
           if arrfetch.get(value) is None:
               arrfetch[value] = c.__dict__[bar_property]
    for x in arrfetch:
      inside_labels.append(x)
      dat.append(arrfetch[x])
      border.append('#C0C0C0C0')
    colors, hoverColors = self.prepare_colorset(len(border))
    inside_datasets = [{
      'data': dat,
      'backgroundColor': colors ,
      'hoverBackgroundColor': hoverColors,
      'borderColor': border,
      'hoverBorderColor': colors,
      'borderWidth': 1
    }]
    data = {
      'labels': inside_labels,
      'datasets': inside_datasets
    }
    full_data = {
      'name':o,'data': {
        'type': type,
        'data': data,
        'options': {
          'title': {
            'display': True,
            'text': o.upper(),
            'fontColor':'#fff',
          },
          'legend': {
            'display': False,
            'position':'right',
            'labels':{
              'fontColor':'#fff',
            }
          },
          'circumference': 2*math.pi,
          'rotation': -math.pi,
          'cutoutPercentage': 40,
        }
      }
    }
    return full_data



class ConfigAdmin(admin.ModelAdmin):
  ordering = ['title']
