'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
from django.db import models
import re
import string
import json

class StoryModel(models.Model):
  class Meta:
    abstract = True

  title = models.CharField(default='', max_length=256, blank=True, unique=True)
  chapter = models.CharField(default='', blank=True, max_length=64)
  date = models.CharField(max_length=128, default='', blank=True)
  place = models.CharField(max_length=128, default='', blank=True)
  description = models.TextField(max_length=2560,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  to_PDF = models.BooleanField(default=True)
  
  def __str__(self):
    """ Standard display """
    return '%s. %s' % (self.chapter, self.title)
    
  def toJSON(self):
    """ Returns JSON of object """
    return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

  def fetch_avatars(self, value):
    """ Bring all avatars rids from some text"""
    from collector.models.characters import Character
    avar = []
    seeker = re.compile('\¤(\w+)\¤')
    changes = []
    res = str(value)
    iter = seeker.finditer(res)
    for item in iter:
      rid = ''.join(item.group().split('¤'))
      ch = Character.objects.filter(rid=rid).first()    
      if not ch is None:
        avar.append(ch.rid)
    return avar

  def get_casting(self):
    """ Bring all avatars rids from all relevant text fields"""
    casting = []
    if (self.to_PDF):
      casting.append(self.fetch_avatars(self.description))
    return casting

  def get_episodes(self):
    """ Return subchapters """
    return []

  def get_full_cast(self):
    """ Return the depth cast for this episode """
    casting = self.get_casting()
    for episode in self.get_episodes():
      casting.append(episode.get_full_cast())
    flat_cast = [c for subcast in casting for c in subcast]
    return sorted(list(set(flat_cast)))

