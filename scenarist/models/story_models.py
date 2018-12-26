#  __                           _     _   
# / _\ ___ ___ _ __   __ _ _ __(_)___| |_ 
# \ \ / __/ _ \ '_ \ / _` | '__| / __| __|
# _\ \ (_|  __/ | | | (_| | |  | \__ \ |_ 
# \__/\___\___|_| |_|\__,_|_|  |_|___/\__|
#                                        
from django.db import models

class StoryModel(models.Model):
  class Meta:
    abstract = True

  title = models.CharField(default='', max_length=256, blank=True, unique=True)
  chapter = models.CharField(default='', blank=True, max_length=64)
  date = models.CharField(max_length=128, default='', blank=True)
  place = models.CharField(max_length=128, default='', blank=True)
  description = models.TextField(max_length=1280,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)

  def __str__(self):
    return '%s. %s' % (self.chapter, self.title)
    
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

  def fetch_avatars(self, str):
    """ Bring all avatars rids from some text"""
    avar = []
    return avar

  def get_casting(self):
    """ Bring all avatars rids from all relevant text fields"""
    casting = []
    casting.append(self.fetch_avatars(self.description))
    return casting
    
