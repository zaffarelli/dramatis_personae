'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django import template
from collector.models.character import Character
from collector.models.loot import Loot
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
    if isinstance(value,int):
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
                elif x>2:
                    res += one_medium
                else:
                    res += one_low
            else:
                res += blank
            if (x+1) % 10 == 0:
                res += '<br/>'
            x += 1
        return res
    else:
        return "ERROR!"

@register.filter(name='as_bullets_short_wildcard')

def as_bullets_short_wildcard(value):
    """ Change int value to list of bullet (Mark Rein*Hagen like)
    """
    if isinstance(value,int):
        one_low = '<i class="fas fa-circle fa-xs wildcard" title="%d"></i>'%(int(value))
        blank = '<i class="fas fa-circle fa-xs blank" title="%d"></i>'%(int(value))
        x = 0
        res = ''
        while x<10:
            if x<int(value):
                res += one_low
            else:
                res += blank
            if (x+1) % 10 == 0:
                res += '<br/>'
            x += 1
        return res
    else:
        return "ERROR!"


@register.filter(name='parse_avatars')

def parse_avatars(value):
  """ Replace avatars rids by html links in a text
  """
  value = "<br/>".join(value.split("\n"))
  """ Auto """
  seeker = re.compile('\¤(\w+)\¤')
  changes = []
  res = str(value)
  iter = seeker.finditer(res)
  for item in iter:
    rid = ''.join(item.group().split('¤'))
    ch = Character.objects.filter(rid=rid).first()
    if not ch is None:
      repstr = '<span id="%d" class="character_link embedded_link" title="%s">%s%s</span>'%(ch.id, ch.entrance, ch.full_name,"" if ch.balanced==True else "*")
    else:
      repstr = '<span class="embedded_link broken">[%s was not found]</span>'%(rid)
    changes.append({'src':item.group(),'dst':repstr})
  newres = res
  for change in changes:
    newres = newres.replace(change['src'],change['dst'])
  """ Replace µ by subsection"""
  sym = 'µ'
  #search =  "[A-Za-z\s\.\'\;]+"
  search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,]+"
  myregex = "\%s%s\%s"%(sym,search,sym)
  seeker = re.compile(myregex)
  changes = []
  txt = newres
  iter = seeker.finditer(txt)
  for item in iter:
    occ = ''.join(item.group().split(sym))
    repstr = '<br/><em>%s</em><br/>'%(occ)
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
    repstr = '<strong>%s</strong>'%(occ)
    changes.append({'src':item.group(),'dst':repstr})
  for change in changes:
    txt = txt.replace(change['src'],change['dst'])
  """ Replace ° by custom data"""
  sym = '°'
  search = "[A-Za-z0-9\é\è\ô\ö\à\s\.\'\;\-\(\)\&\:\,\_]+"
  myregex = "\%s%s\%s"%(sym,search,sym)
  seeker = re.compile(myregex)
  changes = []
  iter = seeker.finditer(txt)
  for item in iter:
    occ = ''.join(item.group().split(sym))
    loot = Loot.objects.filter(code=occ).first()
    repstr = "<div class='loot'>"
    repstr += "<strong>%s (%d)</strong><ul>"%(loot.name,loot.id)
    repstr += "<ul>"
    repstr += "<li>Response DV: <em>%d</em></li>"%(10+loot.sleeves_fame*loot.sleeves_gossip)
    repstr += "<li>Number of people participating to the auction: %d</li>"%(loot.sleeves_authenticity*loot.sleeves_fame)
    repstr += "<li>Highest auction: <em>£%d</em></li>"%(loot.sleeves_gossip*loot.sleeves_fame*loot.sleeves_minimum_increment+loot.price+loot.sleeves_auction*3)
    repstr += "<li>Group: %s</li>"%(loot.group)
    repstr += "<li>Estimated value: <em>£%d</em></li>"%(loot.price)
    repstr += "</ul><ul>"
    repstr += "<li>Fame: %d</li>"%(loot.sleeves_fame)
    repstr += "<li>Gossip: %d</li>"%(loot.sleeves_gossip)
    repstr += "<li>Authenticity: %d</li>"%(loot.sleeves_authenticity)
    repstr += "<li>Base auction: <em>£%d</em></li>"%(loot.sleeves_auction)
    repstr += "<li>Step: +£%d</li>"%(loot.sleeves_minimum_increment)
    repstr += "</ul>"
    repstr += "<p><strong>Procurrer:</strong> %s of %s</p>"%(loot.owner.full_name,loot.owner.alliance)
    if loot.description:
        repstr += "<strong>Description:</strong>"
        repstr += "<p>%s</p>"%(loot.description)
    if loot.secret:
        repstr += "<strong>Notes:</strong>"
        repstr += "<p>%s</p>"%(loot.secret)
    repstr += "</div>"
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

@register.filter(name='as_pa_short')
def as_pa_short(value):
    """ Display weight in kilograms """
    PA = {
          "PA_STR":"STR",
          "PA_CON":"CON",
          "PA_BOD":"BOD",
          "PA_MOV":"MOV",
          "PA_INT":"INT",
          "PA_WIL":"WIL",
          "PA_TEM":"TEM",
          "PA_PRE":"PRE",
          "PA_TEC":"TEC",
          "PA_REF":"REF",
          "PA_AGI":"AGI",
          "PA_AWA":"AWA",
          "OCC_LVL":"Occult",
          "OCC_DRK":"Darkside",
          "":"Error!",
        }
    return PA[value]


@register.filter(name='as_roman')
def as_roman(value):
    if isinstance(int(value),int):
        value = int(value)
        ROMAN = [
            (1000, "M"),
            ( 900, "CM"),
            ( 500, "D"),
            ( 400, "CD"),
            ( 100, "C"),
            (  90, "XC"),
            (  50, "L"),
            (  40, "XL"),
            (  10, "X"),
            (   9, "IX"),
            (   5, "V"),
            (   4, "IV"),
            (   1, "I"),
            ]
        result = ""
        for (arabic, roman) in ROMAN:
            (factor, value) = divmod(value, arabic)
            result += roman * factor
    else:
        result = value
    return result


@register.filter(name='wound')

def wound(value):
  if value=='':
    value=0
  res = int(value)
  if res>0:
      res = "<span class='wounded'>%d</span>"%(value)
  return res
