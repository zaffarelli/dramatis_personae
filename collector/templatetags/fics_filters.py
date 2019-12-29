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


@register.filter(name='modulo')
def modulo(num, val):
  return num % val


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


@register.filter(name='as_bullets_short')

def as_bullets_short(value):
    """ Change int value to list of bullet (Mark Rein*Hagen like)
    """
    one_veryhigh = '<i class="fas fa-circle fa-xs veryhigh" title="%d"></i>'%(int(value))
    one_high = '<i class="fas fa-circle fa-xs high" title="%d"></i>'%(int(value))
    one_medium = '<i class="fas fa-circle fa-xs medium" title="%d"></i>'%(int(value))
    one_low = '<i class="fas fa-circle fa-xs low" title="%d"></i>'%(int(value))
    blank = '<i class="fas fa-circle fa-xs blank" title="%d"></i>'%(int(value))
    x = 0
    res = ''
    while x<10:
        if x<int(value):
            if x>6:
                res += one_veryhigh
            elif x>4:
                res += one_high
            elif x>1:
                res += one_medium
            else:
                res += one_low
        else:
            res += blank
        if (x+1) % 10 == 0:
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
      repstr = '<span id="%s" class="embedded_link" title="%s">%s%s</span>'%(ch.rid, ch.entrance, ch.full_name, ' (€)' if ch.is_exportable else '')
    else:
      repstr = '[%s was not found]'%(rid)
    changes.append({'src':item.group(),'dst':repstr})
  newres = res
  for change in changes:
    newres = newres.replace(change['src'],change['dst'])

  sym = 'µ'
  search =  "[A-Za-z\s\.\'\;]+"
  myregex = "\%s%s\%s"%(sym,search,sym)
  seeker = re.compile(myregex)
  changes = []
  txt = newres
  iter = seeker.finditer(txt)
  for item in iter:
    occ = ''.join(item.group().split(sym))
    repstr = '<div class="subsection">%s</div>'%(occ)
    changes.append({'src':item.group(),'dst':repstr})
  for change in changes:
    txt = txt.replace(change['src'],change['dst'])

  """ Replace § by em"""
  sym = '§'
  search =  "[A-Za-z\s\.\'\;]+"
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
      repstr = '<span id="%s" class="embedded_link" title="%s">%s</span>'%(ch.rid, ch.entrance, ch.full_name)
    else:
      repstr = '<span class="embedded_link">[%s was not found]</span>'%(rid)
    changes.append({'src':item.group(),'dst':repstr})
  for change in changes:
    txt = txt.replace(change['src'],change['dst'])
  """ Replace µ by subsection titles """
  sym = 'µ'
  search =  "[A-Za-z\s\.\'\;]+"
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
  search =  "[A-Za-z\s\.\'\;]+"
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

@register.filter(name='dictsort_3cols')
def dictsort_3cols(value,ref):
  mylist = dictsort(value,ref)
  count = len(mylist)
  rowcount = int(count/3)
  if count%3!=0:
    rowcount+=1
  idx = 0
  cols = [[],[],[]]
  for x in dictsort(value,ref):
    c = int(idx/rowcount)
    cols[c].append(x)
    idx += 1
  flat_cols = []
  for idx in range(rowcount):
    if len(cols[0])>idx:
      flat_cols.append(cols[0][idx])
    if len(cols[1])>idx:
      flat_cols.append(cols[1][idx])
    if len(cols[2])>idx:
      flat_cols.append(cols[2][idx])
  return flat_cols

@register.filter(name='signed')
def signed(value):
  return "%+d"%(int(value))


@register.filter(name='as_root')
def as_root(value):
  return "<b>%s</b>"%(value)

@register.filter(name='as_specialty')
def as_specialty(value):
  x = value.split('(')[1]
  val = x.split(')')[0]
  return "&gt;&nbsp;<i>%s</i>"%(val)


@register.filter(name='as_lifepath')
def as_lifepath(value):
  lp = ['Race','Upbringing','Apprenticeship','Early Career','Tour of Duty','Worldly Benefits']
  return "%s"%(lp[int(value)])


@register.filter(name='prettybool')

def prettybool(value):
    """ Display a boolean mark"""
    if value == True:
        res = '<i class="fas fa-check fa-xs"></i>'
    else:
        res = '<i class="fas fa-times fa-xs"></i>'
    return res

@register.filter(name='as_height')
def as_height(value):
    """ Display height in meters """
    res = "%2.2f m"%(value/100)
    return res

@register.filter(name='as_weight')
def as_weight(value):
    """ Display weight in kilograms """
    res = "%3d kg"%(value)
    return res
