"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from collector.models.character import Character
from collector.models.investigator import Investigator
from collector.models.specie import Specie
from collector.models.campaign import Campaign
from django.template.loader import get_template
import datetime
from collector.utils.basic import get_current_config, export_epic
from collector.utils.fics_references import MAX_CHAR, FONTSET
from collector.views.characters import respawn_avatar_link
import os
from django.conf import settings
from django.http import FileResponse
from django.contrib import messages
import json


def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login/')
    context = {'fontset': FONTSET}
    return render(request, 'collector/index.html', context=context)


def get_list(request, id, slug='none'):
    from collector.utils.basic import get_current_config
    campaign = get_current_config()
    if slug == 'none':
        character_items = campaign.avatars.order_by('-ranking', 'full_name').filter(balanced=False, is_dead=False,
                                                                                    nameless=False, player='').order_by(
            '-OCC_LVL', '-tod_count')
    elif slug.startswith('c-'):
        elements = slug.split('-')
        ep_class = elements[1].capitalize()
        ep_id = 1
        if len(elements) > 2:
            ep_id = elements[2]
        if ep_class == 'Epic':
            from scenarist.models.epics import Epic
            epic = Epic.objects.get(pk=ep_id)
            cast = epic.get_full_cast()
        elif ep_class == 'Drama':
            from scenarist.models.dramas import Drama
            drama = Drama.objects.get(pk=ep_id)
            cast = drama.get_full_cast()
        elif ep_class == 'Act':
            from scenarist.models.acts import Act
            act = Act.objects.get(pk=ep_id)
            cast = act.get_full_cast()
        elif ep_class == 'Event':
            from scenarist.models.events import Event
            event = Event.objects.get(pk=ep_id)
            cast = event.get_full_cast()
        else:
            cast = []
        character_items = []
        if len(cast) > 0:
            for rid in cast:
                print(rid)
                character_item = campaign.open_avatars.get(rid=rid)
                character_items.append(character_item)
        messages.info(request, f'New list filter applied: {slug}')
    else:
        character_items = campaign.avatars.filter(keyword=slug).order_by('team', '-ranking', 'full_name')
        messages.info(request, f'New list filter applied: {slug}')
        if len(character_items) == 0:
            character_items = campaign.open_avatars.filter(rid__contains=slug.lower()).order_by('full_name')
            messages.info(request, f'Searching {slug} among rids')
    # for c in character_items:
    #     c.need_fix = True
    #     c.save()
    paginator = Paginator(character_items, MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    messages.info(request, f'{paginator.count} characters found.')
    context = {'character_items': character_items, 'default_ghost_tgt': "list_ghostmark"}
    template = get_template('collector/list.html')
    html = template.render(context, request)
    response = {
        'mosaic': html,
    }
    return JsonResponse(response)


def show_todo(request):
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


def tile_avatar(request, pk=None):
    if request.is_ajax:
        character_item = Character.objects.get(pk=pk)
    context = {'c': character_item}
    template = get_template('collector/character_tile.html')
    html = template.render(context, request)
    return HttpResponse(html, content_type='text/html')


def get_storyline(request, slug='none'):
    if request.is_ajax:
        config_items = Campaign.objects.filter(hidden=False)
        if slug != 'none':
            for c in config_items:
                c.is_active = (c.smart_code == slug)
                c.save()
        template = get_template('collector/conf_select.html')
        html = template.render({'configs': config_items}, request)
        response = {'mosaic': html}
        return JsonResponse(response)
    else:
        return Http404


def recalc_avatar(request, id=None):
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


def add_avatar(request, slug=None):
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
    item.save()
    character_item = campaign.avatars.get(pk=item.id)
    context = {'mosaic': {'rid': character_item.rid}}
    messages.info(request, f'...{character_item.full_name} added ({campaign.rpgsystem})')
    return JsonResponse(context)


def toggle_public(request, id=None):
    context = {}
    character_item = Character.objects.get(pk=id)
    if character_item is not None:
        character_item.is_public = not character_item.is_public
        character_item.save()
    context = respawn_avatar_link(character_item, context, request)
    return JsonResponse(context)


def toggle_spotlight(request, id=None):
    context = {}
    character_item = Character.objects.get(pk=id)
    if character_item is not None:
        character_item.spotlight = not character_item.spotlight
        character_item.save()
    context = respawn_avatar_link(character_item, context, request)
    return JsonResponse(context)


def conf_details(request):
    if request.is_ajax:
        from collector.models.campaign import Campaign
        campaign = get_current_config()
        _ = export_epic(request, campaign)
        context = {'epic': campaign.parse_details()}
        template = get_template('collector/conf_details.html')
        html = template.render(context, request)
        response = {'mosaic': html}
        return JsonResponse(response)
    else:
        return Http404


def heartbeat(request):
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


def ghostmark_test(request, id=None):
    from collector.models.character import Character
    character_item = Character.objects.get(id=id)
    context = {'c': character_item}
    template = get_template('collector/dp_logo_test.html')
    html = template.render(context, request)
    return HttpResponse(html, content_type='text/html')


def display_sheet(request, pk=None):
    if request.is_ajax:
        if pk is None:
            pk = 22
        c = Character.objects.get(id=pk)
        scenario = "PANCREATOR VOBISCUM SIT"
        pre_title = 'Outer Belt Sector'
        post_title = "Lux Splendor, 5021 A.D"
        spe = c.get_specialities()
        shc = c.get_shortcuts()
        j = c.toJSONFICS()
        settings = {'version': 1.0, 'labels':{}, 'pre_title': pre_title, 'scenario': scenario,
                    'post_title': post_title, 'fontset': FONTSET, 'specialities': spe, 'shortcuts': shc}
        fics_sheet_context = {'settings': json.dumps(settings, sort_keys=True, indent=4), 'data': j}

        return JsonResponse(fics_sheet_context)
