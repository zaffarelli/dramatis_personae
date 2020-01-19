'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from collector.models.character import Character
from collector.models.fics_models import Specie, Role, Profile
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
      character_items = Character.objects.filter(epic=conf.epic).order_by('balanced','full_name')
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
      character_items = Character.objects.order_by('full_name').filter(keyword=slug).order_by('balanced')
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

# def recalc_pa_character(request, id=None):
#   if request.is_ajax():
#     item = get_object_or_404(Character,pk=id)
#     item.onsave_reroll_attributes = True
#     item.save()
#     crid = item.rid
#     template = get_template('collector/character_detail.html')
#     character = template.render({'c':item, 'no_skill_edit':True})
#     templatelink = get_template('collector/character_link.html')
#     link = templatelink.render({'c':item},request)
#     context = {
#       'rid': crid,
#       'character': character,
#       'link': link,
#     }
#     messages.info(request, 'Recalculating attributes for %s'%(item.full_name))
#     return JsonResponse(context)
#   else:
#     raise Http404
#
# def recalc_skills_character(request, id=None):
#   if request.is_ajax():
#     item = get_object_or_404(Character,pk=id)
#     item.onsave_reroll_skills = True
#     item.save()
#     crid = item.rid
#     template = get_template('collector/character_detail.html')
#     character = template.render({'c':item, 'no_skill_edit':True})
#     templatelink = get_template('collector/character_link.html')
#     link = templatelink.render({'c':item},request)
#     context = {
#       'rid': crid,
#       'character': character,
#       'link': link,
#     }
#     messages.info(request, 'Recalculating skills for %s'%(item.full_name))
#     return JsonResponse(context)
#   else:
#     raise Http404

def view_by_rid(request, slug=None):
  """ Ajax view of a character """
  if request.is_ajax():
    item = get_object_or_404(Character,rid=slug)
    template = get_template('collector/character_detail.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
    messages.info(self.request, 'Display by RID: %s'%(context['c'].rid))
  else:
    raise Http404

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
    character_item = Character()
    if slug:
        character_item.full_name = " ".join(slug.split("-"))
    else:
        character_item.full_name = '_noname_ %s'%(datetime.datetime.now())
    character_item.epic = conf.epic
    character_item.use_history_creation = True
    character_item.specie = Specie.objects.first()
    character_item.role = Role.objects.first()
    character_item.profile = Profile.objects.first()
    character_item.save()
    return HttpResponse(status=204)


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
