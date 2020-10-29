"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator
from collector.models.character import Character
from collector.models.fics_models import Specie
from collector.models.config import Config
from django.template.loader import get_template, render_to_string
import datetime
from collector.utils.basic import get_current_config
from collector.utils.fics_references import MAX_CHAR
from django.contrib import messages
from collector.views.characters import respawn_avatar_link

from django.contrib import messages

def index(request):
    """ The basic page for the application
    """
    return render(request, 'collector/index.html')


def get_list(request, id, slug='none'):
    """ Update the list of characters on the page
    """
    conf = get_current_config()
    if request.is_ajax:
        if slug == 'none':
            character_items = Character.objects.order_by('full_name')
        elif slug.startswith('c-'):
            ep_class = slug.split('-')[1].capitalize()
            ep_id = slug.split('-')[2]
            ep = get_object_or_404(eval(ep_class), pk=ep_id)
            cast = ep.get_full_cast()
            character_items = []
            for rid in cast:
                character_item = Character.objects.get(rid=rid)
                character_items.append(character_item)
            messages.info(request,f'New list filter applied: {slug}')
        else:
            character_items = Character.objects.filter(keyword=slug).order_by('full_name')
            messages.info(request,f'New list filter applied: {slug}')
        paginator = Paginator(character_items, MAX_CHAR)
        page = id
        character_items = paginator.get_page(page)
        context = {'character_items': character_items}
        template = get_template('collector/list.html')
        html = template.render(context,request)

        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def get_storyline(request, slug='none'):
    """ Change current config
    """
    if request.is_ajax:
        config_items = Config.objects.all()
        if slug != 'none':
            for c in config_items:
                c.is_active = (c.smart_code == slug)
                c.save()
        template = get_template('collector/conf_select.html')
        html = template.render({'configs': config_items}, request)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def recalc_character(request, id=None):
    """ Re-calculate one single character. To be use in the frontend
    """
    if request.is_ajax():
        messages.warning(request, 'Recalculating...')
        item = get_object_or_404(Character, pk=id)
        item.need_fix = True
        item.fix()
        item.save()
        crid = item.rid
        template = get_template('collector/character_detail.html')
        character = template.render({'c': item, 'no_skill_edit': False})
        template_link = get_template('collector/character_link.html')
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
    if request.is_ajax():
        item = get_object_or_404(Character, pk=id)
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
    if request.is_ajax():
        items = Character.objects.filter(full_name__contains=slug).order_by('full_name')
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
        raise Http404


def show_todo(request):
    """ variant of get_list. Might show the toto characters, actually showing the unbalanced ones
    """
    conf = get_current_config()
    if request.is_ajax:
        character_items = Character.objects.filter(balanced=False).order_by('full_name')
        paginator = Paginator(character_items, MAX_CHAR)
        page = id
        character_items = paginator.get_page(page)
        context = {'character_items': character_items}
        template = get_template('collector/list.html')
        html = template.render(context)
        return HttpResponse(html, content_type='text/html')
    else:
        return Http404


def add_character(request, slug=None):
    """ Add a new character to the universe
        The slug is supposed to be its real fullname.
    """
    conf = get_current_config()
    item = Character()
    if slug:
        item.full_name = " ".join(slug.split("-"))
    else:
        item.full_name = '_noname_ %s' % (datetime.datetime.now())
    item.epic = conf.epic
    item.use_history_creation = True
    item.save()
    item.specie = Specie.objects.filter(species='Urthish').first()
    item.get_rid(item.full_name)
    item.fix()
    item.save()
    character_item = get_object_or_404(Character, pk=item.id)
    template = get_template('collector/character_detail.html')
    character = template.render({'c': character_item, 'no_skill_edit': False})
    templatelink = get_template('collector/character_link.html')
    link = templatelink.render({'c': character_item}, request)
    context = {
        'rid': character_item.rid,
        'id': character_item.id,
        'character': character,
        'link': link,
    }
    messages.info(request, '...%s added' % (character_item.full_name))
    return JsonResponse(context)


def toggle_public(request, id=None):
    """ Toggle the character public/private flag
    """
    conf = get_current_config()
    context = {}
    character_item = Character.objects.get(pk=id)
    if (character_item != None):
        character_item.is_public = not character_item.is_public
        character_item.save()
    context = respawn_avatar_link(character_item, context, request)
    return JsonResponse(context)


def toggle_spotlight(request, id=None):
    """ Toggle the character spotlight flag
    """
    conf = get_current_config()
    context = {}
    character_item = Character.objects.get(pk=id)
    if character_item is not None:
        character_item.spotlight = not character_item.spotlight
        character_item.save()
    context = respawn_avatar_link(character_item, context, request)
    return JsonResponse(context)


def show_jumpweb(request):
    """ Display the full jumpweb.
        Todo: adapt this to the user actually logged.
    """
    if request.is_ajax:
        from collector.models.system import System
        conf = get_current_config()
        context = {}
        context['data'] = {}
        context['data']['mj'] = 1 if request.user.profile.is_gamemaster else 0
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


def conf_details(request):
    """ Current config info
        Todo: the list of the characters for a given Epic should not be retrieved by
                their epic info, but through the story casting functions.
    """
    if request.is_ajax:
        conf = get_current_config()
        context = {'epic': conf.parse_details()}
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
        name = f'avatar_{slug}.pdf'
        filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + name)
        return FileResponse(open(filename, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()