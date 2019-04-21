'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''

from django.http import JsonResponse
from django.template.loader import get_template
from django.contrib import messages
from collector.models.characters import Character
from collector.utils.basic import get_current_config
import json


def get_chardar(request, pk):
  pass


def get_population_statistics(request, *args, **kwargs):
  conf = get_current_config()
  da = []
  ch = conf.get_chart('profile__reference','Profiles','profile.reference')
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('role__reference','Roles','role.reference')  
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('specie__species','Specie','specie.species')  
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('caste','Caste','caste','doughnut')  
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('gender','Gender','gender','doughnut')  
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('native_fief','Native Fief','native_fief','doughnut')  
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('OP','Option Points','OP')  
  da.append(json.dumps(ch['data']))
  ch = conf.get_chart('is_locked','Locked Avatars','is_locked')  
  da.append(json.dumps(ch['data']))
  charts = []
  template = get_template('collector/popstats.html')
  idx = 0
  for x in da:    
    charts.append(template.render({'cname':'chart_%d'%(idx),'cdata':x}))
    idx += 1
  context = {
    'charts': charts,
  }
  messages.add_message(request, messages.INFO, 'Population Statistics updated...')
  return JsonResponse(context)

def get_keywords(request, *args, **kwargs):
  """ Get all the keywords into a chart"""
  conf = get_current_config()
  ch = conf.get_chart('keyword','Keywords','keyword','horizontalBar')  
  da = json.dumps(ch['data'])
  template = get_template('collector/keywords.html')
  chart = template.render({'cname':'chart_keywords','cdata':da})
  context = {
    'chart': chart,
  }
  messages.add_message(request, messages.INFO, 'Loading keywords...')
  return JsonResponse(context)
