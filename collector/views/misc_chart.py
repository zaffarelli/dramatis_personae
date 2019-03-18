'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''

from django.http import JsonResponse
from django.template.loader import get_template
from collector.models.characters import Character
from collector.utils.basic import get_current_config
import json


def get_chardar(request, pk):
  pass


def get_population_statistics(request, *args, **kwargs):
  conf = get_current_config()
  data = conf.get_popstats_races()
  data2 = conf.get_popstats_alliances()
  da = json.dumps(data)
  da2 = json.dumps(data2)
  template = get_template('collector/popstats.html')
  chart1 = template.render({'chart_data':da, 'chart_data2':da2})
  context = {
    'chart1': chart1,
  }
  return JsonResponse(context)
