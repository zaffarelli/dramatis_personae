from cartograph.models.system import System
from cartograph.utils.fics_references import NEW_ROUTES, NEW_SYSTEMS
from collector.utils.basic import get_current_config, slug_decode
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import get_template
import json
from django.contrib import messages


def show_jumpweb(request):
    if request.is_ajax:
        campaign = get_current_config(request)
        context = {}
        context['data'] = {}
        # context['campaign'] = campaign.to_json()
        context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
        context['data']['new_routes'] = ""#"|".join(NEW_ROUTES)
        context['data']['new_systems'] = ""#"|".join(NEW_SYSTEMS)
        context['data']['epic_systems'] = campaign.known_systems
        context['data']['era'] = campaign.epic.era
        context['data']['nodes'] = []
        context['data']['links'] = []
        known_worlds = context['data']['epic_systems'].split('|')
        for s in System.objects.all():
            system = {}
            system['focus'] = False
            if s.name in known_worlds:
                system['focus'] = True
            system['discovery'] = s.discovery
            system['id'] = s.id
            system['name'] = s.name
            system['alliance'] = s.alliance
            system['sector'] = s.sector
            system['x'] = s.x
            system['y'] = s.y
            system['jump'] = s.jump
            system['group'] = s.group
            system['color'] = s.color
            system['color2'] = s.color
            if s.allianceref:
                # print(s.allianceref)
                system['color'] = s.allianceref.color_front
                system['color2'] = s.allianceref.color_back
                system['alliance'] = s.allianceref.reference
            system['orbital_map'] = 1 if s.orbital_map != '' else 0

            system['dtj'] = f'{s.dtj:.2f}'
            system['garrison'] = s.garrison
            system['tech'] = s.tech
            system['symbol'] = s.symbol
            system['population'] = s.population
            context['data']['nodes'].append(system)
            for j in s.jumproads.all():
                lnk = {}
                if j.id > s.id:
                    lnk['source'] = s.id
                    lnk['target'] = j.id
                else:
                    lnk['source'] = j.id
                    lnk['target'] = s.id
                context['data']['links'].append(lnk)
        # c = json.dumps(context, sort_keys=True, indent=4)
        # print(c)
        return JsonResponse(context)
    else:
        return Http404


def show_orbital_map(request, slug=None):
    if request.is_ajax:

        campaign = get_current_config(request)
        slug = slug_decode(slug)
        if slug is None:
            slug = 'Delphi'
        context = {'data': {}}
        try:
            system = System.objects.get(name=slug)
            context['campaign'] = campaign.to_json()
            context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
            context['data']['title'] = f'{system.name}'
            context['data']['alliance'] = f'{system.alliance}'
            context['data']['symbol'] = f'{system.symbol}'
            context['data']['planets'] = []
            context['data']['belts'] = []

            context['data']['zoom_val'] = system.zoom_val if system.zoom_val else 0
            context['data']['zoom_factor'] = system.zoom_factor if system.zoom_factor else 0
            for oi in system.orbitalitem_set.all():
                orbital_item = {'name': oi.name, 'AU': oi.distance, 'tilt': oi.tilt, 'tone': oi.color,
                                'type': oi.get_category_display(), 'azimut': oi.azimut, 'size': oi.size, 'moon': oi.moon,
                                'description': oi.description, 'rings': oi.rings}
                if oi.category == "3":
                    orbital_item['roids'] = []
                    context['data']['belts'].append(orbital_item)
                else:
                    context['data']['planets'].append(orbital_item)
        except System.DoesNotExist:
            messages.error(request, f'System not found!')
            return HttpResponse(status=204)
        # c = json.dumps(context, sort_keys=True, indent=4)
        # print(c)
        return JsonResponse(context)
    else:
        return HttpResponse(status=204)
