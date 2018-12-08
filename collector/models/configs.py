from django.db import models
from django.contrib import admin


class Config(models.Model):
  class Meta:
    ordering = ['title', 'epic']  
  from collector.models.epics import Epic
  from collector.models.dramas import Drama
  from collector.models.acts import Act
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
  drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
  act = models.ForeignKey(Act, null=True, blank=True, on_delete=models.SET_NULL)
  description = models.TextField(max_length=128,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_active = models.BooleanField(default=False)
  smart_code = models.CharField(default='xxxxxx', max_length=6, blank=True)

  def __str__(self):
    return '%s (%s / %s)' % (self.title, self.epic, self.gamemaster)

  def parse_details(self):
    """ Return details from the config epic, dramas and acts    
    """
    from collector.models.epics import Epic
    from collector.models.dramas import Drama
    from collector.models.acts import Act
    epic = Epic.objects.get(title = self.epic.title)
    dramas = Drama.objects.filter(epic = epic).order_by('date')
    context_dramas =[]
    for drama in dramas:
      context_acts = []
      acts = Act.objects.filter(drama = drama).order_by('date')
      for act in acts:
        context_act = {'title':act.title, 'data': act}
        context_acts.append(context_act)
      context_drama = {'title':drama.title, 'data': drama, 'acts': context_acts}
      context_dramas.append(context_drama)
    context = {'title':epic.title, 'data': epic, 'dramas': context_dramas}
    #print(context)
    return context

class ConfigAdmin(admin.ModelAdmin):
  ordering = ('title','epic')


