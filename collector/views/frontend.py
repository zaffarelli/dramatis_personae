'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from collector.models.character import Character
from collector.models.fics_models import Specie
from collector.models.config import Config
from collector.models.skill import Skill
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, BeneficeAfflictionFormSet, WeaponFormSet, ArmorFormSet, ShieldFormSet
from collector.utils.basic import render_to_pdf
from django.template.loader import get_template, render_to_string
from django.template import RequestContext
import json
import ast
from urllib.parse import unquote
from urllib.parse import parse_qs
from collector.utils import fs_fics7
from django.views.decorators.csrf import csrf_exempt
import datetime
from collector.utils.xls_collector import export_to_xls, update_from_xls
from collector.utils.basic import get_current_config
from collector.utils.fics_references import MAX_CHAR
from django.contrib import messages
from collector.views.characters import respawnAvatarLink
from collector.views.characters import CharacterUpdateView


def index(request):
  """ The basic page for the application """
  return render(request,'collector/index.html')

def get_list(request,id,slug='none'):
  """ Update the list of characters on the page """
  from scenarist.models.epics import Epic
  from scenarist.models.dramas import Drama
  from scenarist.models.acts import Act
  from scenarist.models.events import Event
  conf = get_current_config()
  if request.is_ajax:
    if slug=='none':
      character_items = Character.objects.filter(epic=conf.epic).order_by('full_name')
    elif slug.startswith('c-'):
      ep_class = slug.split('-')[1].capitalize()
      ep_id = slug.split('-')[2]
      ep = get_object_or_404(eval(ep_class),pk=ep_id)
      cast = ep.get_full_cast()
      character_items = []
      for rid in cast:
        character_item = Character.objects.get(rid=rid)
        character_items.append(character_item)
    else:
      character_items = Character.objects.filter(keyword=slug).order_by('full_name')
    paginator = Paginator(character_items,MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    context = {'character_items': character_items}
    template = get_template('collector/list.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
  else:
    Http404

def get_storyline(request,slug='none'):
  """ Change current config """
  if request.is_ajax:
    config_items = Config.objects.all()
    if slug != 'none':
      for c in config_items:
        c.is_active = (c.smart_code == slug)
        c.save()
    template = get_template('collector/conf_select.html')
    html = template.render({ 'configs': config_items },request)
    return HttpResponse(html, content_type='text/html')
  else:
    http404


def recalc_character(request, id=None):
  if request.is_ajax():
    messages.warning(request, 'Recalculating...')
    item = get_object_or_404(Character,pk=id)
    item.save()
    crid = item.rid
    template = get_template('collector/character_detail.html')
    character = template.render({'c':item, 'no_skill_edit':False})
    templatelink = get_template('collector/character_link.html')
    link = templatelink.render({'c':item},request)
    context = {
      'rid': crid,
      'id': id,
      'character': character,
      'link': link,
    }
    messages.info(request, '...%s recalculated'%(item.full_name))
    return JsonResponse(context)
  else:
    raise Http404

def view_by_rid(request, slug=None):
  """ Ajax view of a character """
  if request.is_ajax():
    items = Character.objects.filter(full_name__contains=slug).order_by('full_name')
    if items.count():
        item = items.first()
        context = {}
        template = get_template('collector/character_detail.html')
        character = template.render({'c':item, 'no_skill_edit':False})
        templatelink = get_template('collector/character_link.html')
        links = []
        for i in items:
            links.append({'rid':i.rid,'data':templatelink.render({'c':i})})
        context = {
            'rid': item.rid,
            'id': item.id,
            'character': character,
            'links': links,
        }
        messages.info(request, 'Found: %s'%(item.rid))
        return JsonResponse(context)
  else:
    raise Http404

def show_todo(request):
  """ variant of get_list """
  from scenarist.models.epics import Epic
  from scenarist.models.dramas import Drama
  from scenarist.models.acts import Act
  from scenarist.models.events import Event
  conf = get_current_config()
  if request.is_ajax:
    character_items = Character.objects.filter(epic=conf.epic, balanced=False).order_by('full_name')
    paginator = Paginator(character_items,MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    context = {'character_items': character_items}
    template = get_template('collector/list.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
  else:
    Http404



def extract_formset(rqp,s):
  """ Get only the fields matching to this formset """
  res = {}
  for k in rqp:
    if s in k:
      res[k] = rqp[k][0]
  return res

def add_character(request, slug=None):
    """ Add a new character to the universe """
    conf = get_current_config()
    item = Character()
    if slug:
        item.full_name = " ".join(slug.split("-"))
    else:
        item.full_name = '_noname_ %s'%(datetime.datetime.now())
    item.epic = conf.epic
    item.use_history_creation = True
    item.specie = Specie.objects.filter(species='Urthish').first()
    # item.role = Role.objects.first()
    # item.profile = Profile.objects.first()
    item.save()
    character_item = get_object_or_404(Character,pk=item.id)
    template = get_template('collector/character_detail.html')
    character = template.render({'c':character_item, 'no_skill_edit':False})
    templatelink = get_template('collector/character_link.html')
    link = templatelink.render({'c':character_item},request)
    context = {
      'rid': character_item.rid,
      'id': character_item.id,
      'character': character,
      'link': link,
    }
    messages.info(request, '...%s added'%(character_item.full_name))
    return JsonResponse(context)

def toggle_public(request, id=None):
    conf = get_current_config()
    context = {}
    character_item = Character.objects.get(pk=id)
    if (character_item != None):
        character_item.is_public = not character_item.is_public
        character_item.save()
    context = respawnAvatarLink(character_item,context)
    return JsonResponse(context)

def toggle_spotlight(request, id=None):
    conf = get_current_config()
    context = {}
    character_item = Character.objects.get(pk=id)
    if (character_item != None):
        character_item.spotlight = not character_item.spotlight
        character_item.save()
    context = respawnAvatarLink(character_item,context)
    return JsonResponse(context)

def show_jumpweb(request):
  """ Current config info """
  if request.is_ajax:
    from collector.models.system import System
    conf = get_current_config()
    context = {}
    context['data'] = {}
    context['data']['nodes'] = []
    context['data']['links'] = []
    for s in System.objects.all():
        system = {}
        system['id'] = s.id
        system['name'] = s.name
        system['alliance'] = s.alliance
        system['sector'] = s.sector
        #system['jumproads'] = s.jumproads
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
    http404


def conf_details(request):
  """ Current config info """
  if request.is_ajax:
    conf = get_current_config()
    context = {'epic':conf.parse_details()}
    template = get_template('collector/conf_details.html')
    html = template.render(context,request)
    return HttpResponse(html, content_type='text/html')
  else:
    http404

def update_messenger(request):
  context = {}
  template = get_template('collector/messenger.html')
  html = template.render(context,request)
  return HttpResponse(html, content_type='text/html')
