from django import template
from collector.models.characters import Character
import re
import string

register = template.Library()
@register.filter(name='as_bullets')

def as_bullets(value):
  """ Change int value to list of bullet (Mark Rein*Hagen like)
  """
  one = '<i class="fas fa-circle fa-xs" title="%d"></i>'%(value)
  blank = '<i class="fas fa-circle fa-xs blank" title="%d"></i>'%(value)
  x = 0
  res = ''
  while x<10:
    if x<int(value):
      res += one
    else:
      res += blank
    if (x+1) % 5 == 0:
      res += '<br/>'
    x += 1
  return res


@register.filter(name='parse_avatars')

def parse_avatars(value):
  """ Replace avatars rids by html links in a text
  """
  seeker = re.compile('\¤(\w+)\¤')
  changes = []
  res = str(value)
  iter = seeker.finditer(res)
  for item in iter:
    rid = ''.join(item.group().split('¤'))
    ch = Character.objects.filter(rid=rid).first()    
    if not ch is None:
      repstr = '<span id="%s" class="embedded_link" title="%s">%s</span>'%(ch.rid, ch.entrance, ch.full_name)
    else:
      repstr = '[%s was not found]'%(rid)
    changes.append({'src':item.group(),'dst':repstr})
  newres = res
  for change in changes:
    newres = newres.replace(change['src'],change['dst'])
  return newres
