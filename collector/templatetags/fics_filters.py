from django import template

register = template.Library()
@register.filter(name='as_bullets')

def as_bullets(value):
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
  
