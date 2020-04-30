'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''

from django.http import JsonResponse
from django.template.loader import get_template
from django.contrib import messages
from collector.models.character import Character
from collector.utils.basic import get_current_config
import json

def get_chardar(request, pk):
  pass

def get_population_statistics(request, *args, **kwargs):
    conf = get_current_config()
    da = []

    # List of balanced / unbalanced characters
    ch = conf.get_chart('balanced',filter='balanced',type='doughnut')
    da.append(json.dumps(ch['data']))


    ch = conf.get_chart('alliance',filter='is_public',pattern=True,type='doughnut')
    da.append(json.dumps(ch['data']))

    ch = conf.get_chart('is_public',filter='balanced',pattern=True,type='doughnut')
    da.append(json.dumps(ch['data']))
    ch = conf.get_chart('full_name',filter='fencing_league',pattern=True,type='horizontalBar',bar_property='victory_rating')
    da.append(json.dumps(ch['data']))
    ch = conf.get_chart('caste',type='doughnut')
    da.append(json.dumps(ch['data']))
    ch = conf.get_chart('alliance',type='doughnut')
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
  ch = conf.get_chart('keyword',filter='keyword',type='horizontalBar')
  da = json.dumps(ch['data'])
  template = get_template('collector/keywords.html')
  chart = template.render({'cname':'chart_keywords','cdata':da})
  context = {
    'chart': chart,
  }
  return JsonResponse(context)
