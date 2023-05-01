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
    campaign = get_current_config(request)
    da = []
    ch = campaign.get_specific_chart(name='population_per_keyword')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_species')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_ranking')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_OP')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_native_system')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_alliance')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_specific_chart(name='population_per_team')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_chart(field='balanced', bar_property='balanced', type='doughnut', legend_display=False)
    da.append(json.dumps(ch['data']))
    ch = campaign.get_occult_chart(occult='Psi')
    da.append(json.dumps(ch['data']))
    ch = campaign.get_occult_chart(occult='Theurgy')
    da.append(json.dumps(ch['data']))
    charts = []
    template = get_template('collector/popstats.html')
    idx = 0
    for x in da:
        charts.append(template.render({'cname': 'chart_%d' % (idx), 'cdata': x}))
        idx += 1
    context = {
        'mosaic': "".join(charts)
    }
    messages.add_message(request, messages.INFO, 'Statistics updated...')
    return JsonResponse(context)


def get_keywords(request, *args, **kwargs):
    user_profile = request.user.profile
    # print(user_profile)
    # campaign = get_current_config(request)
    all = Character.objects.order_by('keyword')
    data = {'keywords': []}
    edata = {'dramas': []}
    keyword = ''
    count = 0
    for x in all:
        if x.keyword != keyword:
            if keyword != '':
                data['keywords'].append({'name': keyword, 'count': count})
            count = 0
            # print(keyword)
            keyword = x.keyword
        count += 1
    # for item in campaign.epic.card_set.all():
    #     if item.card_type in ['AD', 'DR']:
    #         edata['dramas'].append({'name': item.name, 'code': f'c-card-{item.id}', 'chapter': item.full_id})

    template = get_template('collector/keywords.html')
    chart = template.render({'cdata': data, 'edata': edata})
    context = {
        'chart': chart,
    }
    return JsonResponse(context)
