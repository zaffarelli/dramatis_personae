"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.http import JsonResponse
from django.template.loader import get_template
from django.contrib import messages
from collector.models.character import Character
from collector.utils.basic import get_current_config
from django.contrib import messages
import json


def get_population_statistics(request, *args, **kwargs):
    campaign = get_current_config()
    da = []
    ch = campaign.get_specific_chart(name='population_per_ranking')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_current_system')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_native_system')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_alliance')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_team')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_occult')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_chart(field='balanced', bar_property='balanced', type='doughnut', legend_display=False)
    da.append(json.dumps(ch['data']))
    charts = []
    template = get_template('collector/popstats.html')
    idx = 0
    for x in da:
        charts.append(template.render({'cname': 'chart_%d' % (idx), 'cdata': x}))
        idx += 1
    context = {
        'mosaic':charts,
    }
    messages.add_message(request, messages.INFO, 'Statistics updated...')
    return JsonResponse(context)


def get_keywords(request, *args, **kwargs):
    campaign = get_current_config()
    all = campaign.avatars.order_by('keyword')
    data = {'keywords':[]}
    edata = {'dramas': []}
    keyword = ''
    count = 0
    for x in all:
        if x.keyword != keyword:
            if keyword != '':
                data['keywords'].append({'name':keyword,'count':count})
            count = 0
            keyword = x.keyword
        count += 1
    for d in campaign.epic.drama_set.all():
        edata['dramas'].append({'drama':d.title,'code':f'c-drama-{d.id}','chapter':d.get_full_id})
    # ch = campaign.get_chart(field='keyword', bar_property='keyword', type='horizontalBar', legend_display=False, ticks=False)
    # da = json.dumps(ch['data'])
    template = get_template('collector/keywords.html')
    chart = template.render({'cdata': data, 'edata':edata})
    context = {
        'chart': chart,
    }
    return JsonResponse(context)
