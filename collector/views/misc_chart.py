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


def get_chardar(request, pk):
    pass


def get_population_statistics(request, *args, **kwargs):
    campaign = get_current_config()
    da = []
    # List of balanced / unbalanced characters
    # ch = conf.get_chart(field='full_name', filter='entrance__isnull', pattern=True, bar_property='full_name', type='doughnut', legend_display=False)
    # da.append(json.dumps(ch['data']))


    # ch = campaign.get_chart(field='native_fief', bar_property='native_fief', filter='', type='doughnut', legend_display=False)
    # da.append(json.dumps(ch['data']))
    #
    #
    # ch = campaign.get_chart(field='current_fief', bar_property='current_fief', filter='', type='doughnut', legend_display=False)
    # da.append(json.dumps(ch['data']))
    #

    #
    # ch = campaign.get_chart(field='full_name',
    #                     filter='stories_count__gt',
    #                     pattern=0,
    #                     type='horizontalBar',
    #                     bar_property='stories_count',
    #                     order_by='-')
    # da.append(json.dumps(ch['data']))
    #
    # ch = campaign.get_chart(field='full_name', filter='life_path_total__gt', pattern=0, bar_property="life_path_total", type='horizontalBar', order_by='-')
    # da.append(json.dumps(ch['data']))

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
    #
    # ch = campaign.get_chart(field='alliance', bar_property='alliance', type='horizontalBar', legend_display=False)
    # da.append(json.dumps(ch['data']))



    # ch = campaign.get_chart(field='full_name', filter='fencing_league', pattern=True, type='horizontalBar',
    #                      bar_property='victory_rating', legend_display=True)
    # da.append(json.dumps(ch['data']))
    # ch = campaign.get_chart(bar_property='caste', field='caste', type='bar', legend_display=True)
    # da.append(json.dumps(ch['data']))
    #


    charts = []
    template = get_template('collector/popstats.html')
    idx = 0
    for x in da:
        charts.append(template.render({'cname': 'chart_%d' % (idx), 'cdata': x}))
        idx += 1
    context = {
        'charts': charts,
    }
    messages.add_message(request, messages.INFO, 'Population Statistics updated...')
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
