"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator
from collector.models.character import Character
from collector.models.investigator import Investigator
from collector.models.fics_models import Specie
from collector.models.campaign import Campaign
from django.template.loader import get_template, render_to_string
import datetime
from collector.utils.basic import get_current_config
from collector.utils.fics_references import MAX_CHAR
from django.contrib import messages
from collector.views.characters import respawn_avatar_link
import os
from django.conf import settings
from django.http import FileResponse
from django.contrib import messages
import json


def index(request):
    """ The basic page for the application
    """
    if not request.user.is_authenticated:
        return redirect('accounts/login/')
    return render(request, 'collector/index.html')


def get_list(request, id, slug='none'):
    """ Update the list of characters on the page
        They will be sorted by full name only !
    """
    from scenarist.models.epics import Epic
    from scenarist.models.dramas import Drama
    from scenarist.models.acts import Act
    from scenarist.models.events import Event
    from collector.utils.basic import get_current_config
    campaign = get_current_config()
    if slug == 'none':
        character_items = campaign.avatars.order_by('full_name')
    elif slug.startswith('c-'):
        ep_class = slug.split('-')[1].capitalize()
        ep_id = slug.split('-')[2]
        ep = get_object_or_404(eval(ep_class), pk=ep_id)
        cast = ep.get_full_cast()
        character_items = []
        for rid in cast:
            character_item = campaign.avatars.get(rid=rid)
            character_items.append(character_item)
        messages.info(request, f'New list filter applied: {slug}')
    else:
        character_items = campaign.avatars.filter(keyword=slug).order_by('full_name')
        messages.info(request, f'New list filter applied: {slug}')
    paginator = Paginator(character_items, MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    context = {'character_items': character_items}
    template = get_template('collector/list.html')
    html = template.render(context,request)
    messages.info(request, f'{paginator.count} characters found.')
    return HttpResponse(html, content_type='text/html')



def show_todo(request):
    """ variant of get_list. Might show the toto characters, actually showing the unbalanced ones
    """
    campaign = get_current_config()
    if request.is_ajax:
        character_items = campaign.avatars.filter(priority=True).order_by('full_name')
        paginator = Paginator(character_items, MAX_CHAR)
        page = id
        character_items = paginator.get_page(page)
        context = {'character_items': character_items}
        template = get_template('collector/list.html')
        html = template.render(context, request)
        messages.info(request, f'{paginator.count} characters found.')
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def get_storyline(request, slug='none'):
    """ Change current config
    """
    if request.is_ajax:
        config_items = Campaign.objects.filter(hidden=False)
        if slug != 'none':
            for c in config_items:
                c.is_active = (c.smart_code == slug)
                c.save()
        template = get_template('collector/conf_select.html')
        html = template.render({'configs': config_items}, request)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def recalc_avatar(request, id=None):
    """ Re-calculate one single character. To be use in the frontend
        This function must be compliant to all campaigns (actually fics and coc7)
    """
    campaign = get_current_config()
    if request.is_ajax():
        messages.warning(request, 'Recalculating...')
        item = campaign.avatars.get(pk=id)
        item.need_fix = True
        item.fix(campaign)
        item.save()
        item.need_pdf = True
        item.backup()
        crid = item.rid
        if campaign.is_fics:
            template = get_template('collector/character_detail.html')
            template_link = get_template('collector/character_link.html')
        if campaign.is_coc7:
            template = get_template('collector/investigator_detail.html')
            template_link = get_template('collector/investigator_link.html')
        character = template.render({'c': item, 'no_skill_edit': False})
        link = template_link.render({'c': item}, request)
        mobile_form = get_template('collector/mobile_form.html')
        mf = mobile_form.render({'c': item}, request)
        context = {
            'rid': crid,
            'id': id,
            'character': character,
            'link': link,
            'mobile_form': mf,
        }
        messages.info(request, '...%s recalculated' % item.full_name)
        return JsonResponse(context)
    else:
        raise Http404


def wa_export_character(request, id=None):
    """ Preparing statsblock export for World Anvil
    """
    campaign = get_current_config()
    if request.is_ajax():
        item = campaign.avatars.get(pk=id)
        template = get_template('collector/character_wa_statblock.html')
        character = template.render({'c': item}, request)
        context = {
            'character': character,
        }
        messages.info(request, '...%s exported for WorldAnvil' % item.full_name)
        return JsonResponse(context)
    else:
        raise Http404


def view_by_rid(request, slug=None):
    """ Ajax view of a character, with a part of the full name
        passed to the customizer input field.
    """
    campaign = get_current_config()
    if request.is_ajax():
        items = campaign.avatars.filter(rid__contains=slug.lower()).order_by('full_name')
        if items.count():
            item = items.first()
            context = {}
            template = get_template('collector/character_detail.html')
            character = template.render({'c': item, 'no_skill_edit': False})
            templatelink = get_template('collector/character_link.html')
            links = []
            for i in items:
                links.append({'rid': i.rid, 'data': templatelink.render({'c': i})})
            context = {
                'rid': item.rid,
                'id': item.id,
                'character': character,
                'links': links,
            }
            messages.info(request, 'Found: %s' % (item.rid))
            return JsonResponse(context)
        else:
            messages.error(request, f'The term "{slug}" was not found in characters RID.')
    return HttpResponse(status=204)


def add_avatar(request, slug=None):
    """ Add a new character to the universe
        The slug is supposed to be its real fullname.
        Campaign compliant
    """
    campaign = get_current_config()
    if campaign.is_coc7:
        item = Investigator()
    elif campaign.is_fics:
        item = Character()
    if slug:
        item.full_name = " ".join(slug.split("-"))
    else:
        item.full_name = '_noname_ %s' % (datetime.datetime.now())
    item.epic = campaign.epic
    if campaign.is_fics:
        item.use_history_creation = True
        item.save()
        item.specie = Specie.objects.filter(species='Urthish').first()
    item.get_rid(item.full_name)
    item.fix()
    item.save()
    character_item = campaign.avatars.get(pk=item.id)
    if campaign.is_fics:
        template = get_template('collector/character_detail.html')
        templatelink = get_template('collector/character_link.html')
    elif campaign.is_coc7:
        template = get_template('collector/investigator_detail.html')
        templatelink = get_template('collector/investigator_link.html')
    else:
        messages.warning(request, f'TODO for this campaign !!!')
    character = template.render({'c': character_item, 'no_skill_edit': False})
    link = templatelink.render({'c': character_item}, request)
    context = {
        'rid': character_item.rid,
        'id': character_item.id,
        'character': character,
        'link': link,
    }
    messages.info(request, f'...{character_item.full_name} added ({campaign.rpgsystem})')
    return JsonResponse(context)


def toggle_public(request, id=None):
    """ Toggle the character public/private flag
    """
    context = {}
    character_item = Character.objects.get(pk=id)
    if character_item is not None:
        character_item.is_public = not character_item.is_public
        character_item.save()
    context = respawn_avatar_link(character_item, context, request)
    return JsonResponse(context)


def toggle_spotlight(request, id=None):
    """ Toggle the character spotlight flag
    """
    context = {}
    character_item = Character.objects.get(pk=id)
    if character_item is not None:
        character_item.spotlight = not character_item.spotlight
        character_item.save()
    context = respawn_avatar_link(character_item, context, request)
    return JsonResponse(context)


def show_jumpweb(request):
    """ Display the full jumpweb.
    """
    if request.is_ajax:

        from collector.models.system import System
        from collector.utils.fics_references import NEW_ROUTES, NEW_SYSTEMS
        from collector.utils.basic import get_current_config
        campaign = get_current_config()
        context = {}
        context['data'] = {}
        context['campaign'] = campaign
        context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
        context['data']['new_routes'] = "|".join(NEW_ROUTES)
        context['data']['new_systems'] = "|".join(NEW_SYSTEMS)
        context['data']['nodes'] = []
        context['data']['links'] = []
        for s in System.objects.all():
            system = {}
            system['id'] = s.id
            system['name'] = s.name
            system['alliance'] = s.alliance
            system['sector'] = s.sector
            # system['jumproads'] = s.jumproads
            system['x'] = s.x
            system['y'] = s.y
            system['jump'] = s.jump
            system['group'] = s.group
            system['color'] = s.color
            system['orbital_map'] = 1 if s.orbital_map != '' else 0
            system['discovery'] = s.discovery
            system['dtj'] = s.dtj
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
        template = get_template('collector/jumpweb.html')
        html = template.render(context)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def show_orbital_map(request, id):
    """ Display the full jumpweb.
        Todo: adapt this to the user actually logged.
    """
    if request.is_ajax:
        from collector.models.system import System, OrbitalItem
        from collector.utils.basic import get_current_config
        campaign = get_current_config()
        system = get_object_or_404(System, pk=id)
        context = {'data': {}}
        context['campaign'] = campaign
        context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
        context['data']['title'] = f'{system.name}'
        context['data']['alliance'] = f'{system.alliance}'
        context['data']['symbol'] = f'{system.symbol}'
        context['data']['planets'] = []

        context['data']['zoom_val'] = system.zoom_val if system.zoom_val else 0
        context['data']['zoom_factor'] = system.zoom_factor if system.zoom_factor else 0
        for oi in system.orbitalitem_set.all():
            orbital_item = {'name': oi.name, 'AU': oi.distance, 'tilt': oi.tilt, 'speed': oi.speed, 'tone': oi.color,
                            'type': oi.get_category_display(), 'azimut': oi.azimut, 'size': oi.size, 'moon': oi.moon, 'description':oi.description, 'rings': oi.rings}
            context['data']['planets'].append(orbital_item)
        template = get_template('collector/orbital_map.html')
        html = template.render(context)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def conf_details(request):
    """ Current config info
        Todo: the list of the characters for a given Epic should not be retrieved by
                their epic info, but through the story casting functions.
    """
    if request.is_ajax:
        from collector.models.campaign import Campaign
        campaign = get_current_config()
        context = {'epic': campaign.parse_details()}
        template = get_template('collector/conf_details.html')
        html = template.render(context, request)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def heartbeat(request):
    """ Global heartbeat to raise messages in the messenger toaster.
        Todo: the actual system can certainly be enhanced
    """
    context = {}
    template = get_template('collector/messenger.html')
    html = template.render(context, request)
    return HttpResponse(html, content_type='text/html')


def pdf_show(request, slug):
    try:
        name = f'{slug}.pdf'
        filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/avatars/' + name)
        return FileResponse(open(filename, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def show_ghostmark(request,rid=None):
    if request.is_ajax:
        from collector.models.character import Character
        from collector.models.alliance_ref import AllianceRef
        from django.core import serializers
        context = {'data':{'character':{}, 'alliance':{}}}
        c = Character.objects.filter(rid=rid)
        if len(c)>0:
            context['data']['character'] = c.first().toJSON()
            if c.first().alliance_ref:
                a = AllianceRef.objects.filter(id=c.first().alliance_ref.id)
                context['data']['alliance'] = a.first().toJSON()
        template = get_template('collector/ghostmark.html')
        html = template.render(context)
        return HttpResponse(html, content_type='image/svg+xml')
    else:
        return Http404
