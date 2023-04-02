"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from collector.models.character import Character
# from collector.models.investigator import Investigator
from collector.models.specie import Specie
from collector.models.campaign import Campaign
from django.template.loader import get_template
import datetime
from collector.utils.basic import get_current_config, export_epic, slug_decode
from collector.utils.fics_references import FONTSET
# from django.conf import settings
from collector.views.characters import respawn_avatar_link
import os
from django.conf import settings
from django.http import FileResponse
from django.contrib import messages
from collector.utils.d4_changes import is_ajax
import json
import base64


# from collector.utils.log_wrapper import logwrap

def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login/')
    context = {'fontset': FONTSET}
    return render(request, 'collector/index.html', context=context)


def get_list(request, id, slug='none'):
    from collector.utils.basic import get_current_config
    campaign = get_current_config(request)
    if slug == 'none':
        slug = base64.b64encode(slug.encode("utf-8"))
    # print(f'[{slug}]')
    slug = slug.replace('_', '=')
    decs = str(base64.b64decode(slug), "utf-8")
    if decs == 'none':
        character_items = campaign.dramatis_personae \
            .order_by('balanced', '-team', 'keyword', 'historical_figure', 'nameless', 'full_name') \
            .filter(is_dead=False, keyword__startswith=campaign.epic.shortcut)
    elif decs.startswith('x-'):
        elements = decs.split('-')
        command = elements[1].lower()
        if command == 'all':
            character_items = Character.objects.filter(archived=False).order_by('historical_figure', 'nameless',
                                                                                'full_name')
        elif command == 'todo':
            character_items = Character.objects.filter(balanced=False).order_by('historical_figure', 'nameless',
                                                                                'full_name')
        elif command == 'orphans':
            character_items = Character.objects.filter(is_cast=False).order_by('historical_figure', 'nameless',
                                                                               'full_name')
        elif command == 'archived':
            character_items = Character.objects.filter(archived=True).order_by('historical_figure', 'nameless',
                                                                               'full_name')
        else:
            character_items = Character.objects.filter(rid__contains=command) | Character.objects.filter(
                full_name__icontains=command) | Character.objects.filter(alias__icontains=command)

        messages.info(request, f"Searching {command} characters, cross epics. Yeah, that's everybody.")
    elif decs.startswith('c-'):
        elements = decs.split('-')
        ep_class = elements[1].capitalize()
        # print(elements)
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
        elif ep_class == 'Card':
            # print(ep_id)
            from scenarist.models.cards import Card
            card = Card.objects.get(pk=ep_id)
            cast = card.get_full_cast()
        else:
            cast = []
        character_items = []
        if len(cast) > 0:
            for rid in cast:
                # print(rid)
                character_item = campaign.open_avatars.get(rid=rid)
                character_items.append(character_item)
        messages.info(request, f'New list filter applied specific character with rid {decs}')
    else:
        character_items = campaign.avatars.filter(keyword=decs).order_by('full_name')
        messages.info(request, f'New list filter applied fro keyword {decs}')
        if len(character_items) == 0:
            character_items = campaign.open_avatars.filter(rid__contains=decs.lower()).order_by('full_name')
            messages.info(request, f'Searching {decs} among rids')
    # for c in character_items:
    #     c.need_fix = True
    #     c.save()
    if request.user.is_authenticated:
        paginator = Paginator(character_items, request.user.profile.option_display_count)
    else:
        paginator = Paginator(character_items, settings.MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    messages.info(request, f'{paginator.count} characters found.')
    context = {'character_items': character_items, 'default_ghost_tgt': "list_ghostmark", "count": paginator.count}
    template = get_template('collector/list.html')
    html = template.render(context, request)
    response = {
        'mosaic': html,
    }
    return JsonResponse(response)


def show_todo(request):
    campaign = get_current_config(request)
    if is_ajax(request):
        character_items = campaign.avatars.filter(priority=True).order_by('full_name')
        if request.user.is_authenticated:
            paginator = Paginator(character_items, request.user.profile.option_display_count)
        else:
            paginator = Paginator(character_items, settings.MAX_CHAR)
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
    if is_ajax(request):
        character_item = Character.objects.get(pk=pk)
    context = {'c': character_item}
    template = get_template('collector/character_tile.html')
    html = template.render(context, request)
    return HttpResponse(html, content_type='text/html')


def deep_toggle(request, slug=None, id=None):
    response = {'status': 0}
    if is_ajax(request):
        matches = Character.objects.filter(id=id)
        if slug is not None:
            if len(matches) == 1:
                c = matches.first()
                x = getattr(c, slug)
                setattr(c, slug, not (x))
                c.save()
                response['status'] = 1
                response[slug] = getattr(c, slug)
                template = get_template('collector/character_link_row.html')
                html = template.render({'c': c})
                response['row'] = html
    return JsonResponse(response)


def get_storyline(request, slug='none'):
    if is_ajax(request):
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
    campaign = get_current_config(request)
    if is_ajax(request):
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
        # if campaign.is_coc7:
        #     template = get_template('collector/investigator_detail.html')
        #     template_link = get_template('collector/investigator_link.html')
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


def grab_avatar(request, id=None):
    campaign = get_current_config(request)
    if is_ajax(request):
        messages.info(request, 'Grabbing avatar...')
        campaign.grab(id)
    return HttpResponse(status=204)


def wa_export_character(request, id=None):
    campaign = get_current_config(request)
    if is_ajax(request):
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
    campaign = get_current_config(request)
    if campaign.is_coc7:
        item = Investigator()
    elif campaign.is_fics:
        item = Character()
    if slug:
        slug = slug_decode(slug)
        item.full_name = slug
    else:
        item.full_name = '_noname_ %s' % (datetime.datetime.now())
    item.epic = campaign.epic
    if campaign.is_fics:
        item.use_history_creation = True
        item.save()
        item.specie = Specie.objects.filter(species='Urthish').first()
        item.keyword = campaign.epic.full_id
    item.get_rid(item.full_name)
    item.save()
    character_item = campaign.avatars.get(pk=item.id)
    context = {'mosaic': {'rid': character_item.rid}}
    messages.info(request, f'...{character_item.full_name} added ({campaign.rpgsystem})')
    # return JsonResponse(context)
    return HttpResponse(status=204)


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
    if is_ajax(request):
        from collector.models.campaign import Campaign
        campaign = get_current_config(request)
        if campaign.new_narrative:
            epic_data = campaign.epic.to_json()
            context = {'data': epic_data}
            template = get_template('collector/conf_details2.html')
            html = template.render(context, request)
            response = {'mosaic': html}
        else:
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
    template = get_template('collector/ghostmark_test.html')
    html = template.render(context, request)
    return HttpResponse(html, content_type='text/html')


def display_sheet(request, pk=None):
    if is_ajax(request):
        from collector.models.campaign import Campaign
        campaign = get_current_config(request)
        if pk is None:
            pk = 22
        c = Character.objects.get(id=pk)
        scenario = campaign.epic.name.upper()
        pre_title = ""  # campaign.epic.place + ' - ' + campaign.epic.date
        post_title = "FuZion Interlock Custom System v8.0"
        spe = c.get_specialities()
        shc = c.get_shortcuts()
        j = c.to_jsonFICS()
        settings = {'version': 1.0, 'labels': {}, 'pre_title': pre_title, 'scenario': campaign.short_name.upper(),
                    'post_title': post_title, 'fontset': FONTSET, 'specialities': spe, 'shortcuts': shc}
        fics_sheet_context = {'settings': json.dumps(settings, sort_keys=True, indent=4), 'data': j}

        return JsonResponse(fics_sheet_context)


def switch_epic(request, id=None):
    campaign = get_current_config(request)
    # print(slug)
    if id is None:
        campaigns = Campaign.objects.all()
        list = []
        for c in campaigns:
            list.append(c.epic.shortcut)
        messages.error(request, f'No campaign code selected. Try one of those: {", ".join(list)}')
    else:
        # shortcut = slug_decode(slug)
        new_campaigns = Campaign.objects.filter(id=id)
        if len(new_campaigns) == 1:
            new_campaign = new_campaigns.first()
            new_campaign.is_active = True
            new_campaign.save()
            campaign.is_active = False
            campaign.save()
            messages.info(request, f'Current epic switched to {new_campaign.epic.name}.')
            # if not request.user.is_authenticated:
            #     return redirect('accounts/login/')
            # context = {'fontset': FONTSET}
            # return render(request, 'collector/index.html', context=context)
            return HttpResponseRedirect('/')
        messages.warning(request, f'Current campaign not changed.')
    return HttpResponse(status=204)


def display_sessionsheet(request, slug=None):
    if is_ajax(request):
        from collector.models.campaign import Campaign
        campaign = get_current_config(request)
        pks = []
        teams = campaign.team_set.filter(active=True)
        if len(teams) >= 1:
            team = teams.first()
            for tm in team.teammate_set.all():
                pks.append(tm.character_id)

        players = Character.objects.filter(id__in=pks)
        players_list = []
        i = 0
        for c in players:
            # spe = c.get_specialities()
            # shc = c.get_shortcuts()
            ch = c.to_jsonFICS()
            k = json.loads(ch)
            k['idx'] = i
            k['shortcuts'] = c.get_shortcuts()
            i += 1
            ch = json.dumps(k)
            players_list.append(ch)

        from scenarist.models.cards import Card
        adventure = Card.objects.filter(is_ongoing=True).first()
        scenario = adventure.name.upper()
        pre_title = adventure.place
        post_title = ""
        settings = {'version': 1.0, 'labels': {}, 'pre_title': pre_title, 'scenario': scenario,
                    'post_title': post_title, 'fontset': FONTSET,
                    'adventure': adventure.to_json}  # , 'specialities': spe, 'shortcuts': shc}
        response = {'settings': json.dumps(settings, sort_keys=True, indent=4),
                    'data': json.dumps(players_list, indent=4, sort_keys=True)}
        return JsonResponse(response)


def all_epics(request):
    if is_ajax(request):
        from collector.models.campaign import Campaign
        campaigns = Campaign.objects.filter(is_available=True).order_by('epic__era')
        epics = []
        for x in campaigns:
            e = json.loads(x.to_json())
            e['population'] = x.population
            e['epic_title'] = x.epic.name
            e['epic_era'] = x.epic.era
            e['epic'] = x.epic.to_json()
            e['full_cast'] = x.epic.dramatis_personae_simple()
            epics.append(e)
        context = {'epics': epics, 'title': "Epics", "comment": f"{len(epics)} epic(s)."}
        template = get_template('collector/epics.html')
        html = template.render(context, request)
        response = {'mosaic': html}
        return JsonResponse(response)
    else:
        return HttpResponse(status=204)


def all_spaceships(request):
    if is_ajax(request):
        from collector.models.spacecraft import Spaceship
        ships = Spaceship.objects.filter(is_available=True).order_by('ship_ref__ship_status')
        ships_data = []
        for ship in ships:
            e = ship.ship_data
            ships_data.append(e)
        context = {'ships': ships_data}
        template = get_template('collector/spaceships.html')
        html = template.render(context, request)
        response = {'mosaic': html}
        return JsonResponse(response)
    else:
        return HttpResponse(status=204)


def handle_cards(request):
    if is_ajax(request):
        from scenarist.models.cards import Card
        from collector.models.campaign import Campaign
        campaign = get_current_config(request)
        notes_items = Card.objects.filter(epic=campaign.epic, card_type__in=["EP", "DR", "AD", "UN"]).order_by(
            'full_id')
        cards = []
        for x in notes_items:
            n = x.to_json
            cards.append(n)
        context = {'cards': cards, 'title': "Adventure Cards", "comment": f"{len(cards)} item(s)."}
        template = get_template('collector/cards.html')
        html = template.render(context, request)
        response = {'mosaic': html}
        return JsonResponse(response)
    else:
        return HttpResponse(status=204)
