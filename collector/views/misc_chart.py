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

  ch = conf.get_chart('castprofile__reference','Profiles','castprofile.reference')
  da.append(json.dumps(ch['data']))

  ch = conf.get_chart('castrole__reference','Roles','castrole.reference')  
  da.append(json.dumps(ch['data']))

  ch = conf.get_chart('castspecies__species','Species','castspecies.species')  
  da.append(json.dumps(ch['data']))

  ch = conf.get_chart('keyword','Keywords','keyword','handleKeywordClick')  
  da.append(json.dumps(ch['data']))

  ch = conf.get_chart('caste','Caste','caste','','doughnut')  
  da.append(json.dumps(ch['data']))

  ch = conf.get_chart('gender','Gender','gender','','doughnut')  
  da.append(json.dumps(ch['data']))

  ch = conf.get_chart('native_fief','Native Fief','native_fief','','doughnut')  
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
