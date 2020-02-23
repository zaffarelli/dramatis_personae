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
    idx = 0
    circ = 360.0
    vmin, vmax = 0X33, 0xcc
    colval = [vmin,vmin,vmin]
    try:
      angle_inc = (circ*math.pi * 2) / (size)
      #print('ok')
    except:
      #print('paf')
      return [],[]
    #print('Full circle=%0.4f'%(math.pi * 2))
    angle_step = (circ*math.pi * 2) / 8
    #compo_range = (vmax-vmin)/angle_step
    target_component = [
      [2,+1],    # 0 0 0   0
      [1,+1],    # 0 0 1   1
      [2,-1],    # 0 1 1   3
      [0,+1],    # 0 1 0   2
      [2,+1],    # 1 1 0   6
      [1,-1],    # 1 1 1   7
      [2,-1],    # 1 0 1   5
      [0,-1]     # 1 0 0   4
    ]
    comp = 0
    while idx < size:
      angle = angle_inc * (idx % size)
      angle_steps_covered = int(angle / angle_step)
      inc = (vmax-vmin)*6/size #(angle - int(angle_steps_covered)*angle_step)/angle_step * (vmax-vmin)

      cv = target_component[comp][0]
      if target_component[comp][1] > 0:
        colval[cv] +=  int(inc)
        if colval[cv]+inc>vmax:
          comp += 1
      else:
        colval[cv] -=  int(inc)
        if colval[cv]-inc<vmin:
          comp += 1
      comp %= 8
      col = '#%02X%02X%02X80'%(colval[0]%0xff,colval[1]%0xff,colval[2]%0xff)
      hcol = '#%02X%02X%02XF0'%(colval[0]%0xff,colval[1]%0xff,colval[2]%0xff)
      #col = '#%02X80%02X80'%(int((idx/size)*256),int((idx/size)*256))
      colorset.append(col)
      hcolorset.append(hcol)
      #print('%16s (comp:%0.4f inc:%0.4f ASC:%0.4f )'%(col,comp,inc, angle_steps_covered ))
      #print('%16s'%(col))
      idx += 1
    #print('done')
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
    print(arrfetch)
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
            'text': o,
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
