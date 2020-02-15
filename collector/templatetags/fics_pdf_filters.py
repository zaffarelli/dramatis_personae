'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django import template
from collector.models.character import Character
import re
import string
from django.template.defaultfilters import dictsort

register = template.Library()

@register.filter(name='parse_avatars_pdf')
def parse_avatars_pdf(value):
  """ Replace avatars rids by html links in a text """
  sym = '¤'
  search =  '(\w+)'
  seeker = re.compile('\%s%s\%s'%(sym,search,sym))
  changes = []
  txt = str(value)
  iter = seeker.finditer(txt)
  for item in iter:
    rid = ''.join(item.group().split(sym))
    ch = Character.objects.filter(rid=rid).first()
    if ch:
      repstr = '<span class="embedded_link">%s%s</span>'%(ch.full_name,"" if ch.balanced==True else "*")
    else:
      repstr = '<span class="embedded_link broken">[%s was not found]</span>'%(rid)
    changes.append({'src':item.group(),'dst':repstr})
  for change in changes:
    txt = txt.replace(change['src'],change['dst'])
  """ Replace µ by subsection titles """
  sym = 'µ'
  search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,]+"
  myregex = "\%s%s\%s"%(sym,search,sym)
  seeker = re.compile(myregex)
  changes = []
  iter = seeker.finditer(txt)
  for item in iter:
    occ = ''.join(item.group().split(sym))
    repstr = '</p><h6 class="subsection">%s</h6><p>'%(occ)
    changes.append({'src':item.group(),'dst':repstr})
  for change in changes:
    txt = txt.replace(change['src'],change['dst'])
  """ Replace § by em"""
  sym = '§'
  search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,]+"
  myregex = "\%s%s\%s"%(sym,search,sym)
  seeker = re.compile(myregex)
  changes = []
  iter = seeker.finditer(txt)
  for item in iter:
    occ = ''.join(item.group().split(sym))
    repstr = '<em>%s</em>'%(occ)
    changes.append({'src':item.group(),'dst':repstr})
  for change in changes:
    txt = txt.replace(change['src'],change['dst'])
  return txt

@register.filter(name='high_skill_check_pdf')
def high_skill_check_pdf(value):
    res = value
    if value >= 5:
        res = "<em>%d</em>"%(value)
    return value
