#    ___      _ _           _             
#   / __\___ | | | ___  ___| |_ ___  _ __ 
#  / /  / _ \| | |/ _ \/ __| __/ _ \| '__|
# / /__| (_) | | |  __/ (__| || (_) | |   
# \____/\___/|_|_|\___|\___|\__\___/|_|   
#                                        
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from collector.models.characters import Character
from collector.models.configs import Config
from collector.models.skills import Skill
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
      character_items = Character.objects.order_by('full_name').filter(keyword=slug)
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
  
  


def view_character(request, id=None):
  """ Ajax view of a character """
  if request.is_ajax():
    item = get_object_or_404(Character,pk=id)
    template = get_template('collector/character.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    raise Http404

def view_by_rid(request, slug=None):
  """ Ajax view of a character """
  if request.is_ajax():
    item = get_object_or_404(Character,rid=slug)
    template = get_template('collector/character.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    raise Http404

def extract_formset(rqp,s):
  """ Get only the fields matching to this formset """
  res = {}
  for k in rqp:
    if s in k:
      res[k] = rqp[k][0]
  return res

def edit_character(request,id=None):
  """
  Ajax edit of a character.
  WARNING: Beware that with this method, the last formset can grab an " at the end, so put
  the csrf token for the form after the last formset!!!
  """
  conf = get_current_config()
  crid = ''
  line = ''
  if request.is_ajax():
    if request.method == 'POST':
      #print("This is a POST request....")
      cid = request.POST.get('cid')
      character_item = Character.objects.get(pk=cid)
      crid = character_item.rid
      """ FIXME: There is a mistake here that puts " at start and end ...."""
      formdata = json.loads(json.dumps(parse_qs(json.dumps(request.POST['character'])),indent=2))
      forms = character_item.sanitize(formdata)
      fv = False
      if forms == None:
        print('No change for character...')
      else:
        fv = True
      #formdata = CharacterForm(request.POST['character'])
      #fv = formdata.is_valid()
      if fv:
        #print("Form is valid")
        skill_data = extract_formset(formdata,'skill_set')
        talent_data = extract_formset(formdata,'talent_set')
        blessingcurse_data = extract_formset(formdata,'blessingcurse_set')
        beneficeaffliction_data = extract_formset(formdata,'beneficeaffliction_set')
        armor_data = extract_formset(formdata,'armor_set')
        weapon_data = extract_formset(formdata,'weapon_set')
        shield_data = extract_formset(formdata,'shield_set')
        skills = SkillFormSet(skill_data, instance=character_item)
        talents = TalentFormSet(talent_data, instance=character_item)
        blessingcurses = BlessingCurseFormSet(blessingcurse_data, instance=character_item)
        beneficeafflictions = BeneficeAfflictionFormSet(beneficeaffliction_data, instance=character_item)
        armors = ArmorFormSet(armor_data, instance=character_item)
        weapons = WeaponFormSet(weapon_data, instance=character_item)
        shields = ShieldFormSet(shield_data, instance=character_item)
        skv = skills.is_valid()
        tav = talents.is_valid() 
        bcv = blessingcurses.is_valid()
        bav = beneficeafflictions.is_valid()
        arv = armors.is_valid()
        wpv = weapons.is_valid()
        shv = shields.is_valid()
        if skv and tav and bcv and bav and arv and wpv and fv and shv:        
          skills.save()
          talents.save()
          blessingcurses.save()
          beneficeafflictions.save()
          armors.save()
          weapons.save()
          shields.save()
          print('Saving character...')
          character_item.save()
          print('...character saved.')
          item = get_object_or_404(Character,pk=cid)
          template = get_template('collector/character.html')
          html = template.render({'c':item})
          templatelink = get_template('collector/character_link.html')
          line = templatelink.render({'c':character_item},request)
          #print("Form is valid")
        else:
          html = '<div class="classyview">'
          html += '<p>Unable to update this character !!!</p>'
          html += 'Skills: %s<br/>'%(skills.errors)
          html += 'Talents: %s<br/>'%(talents.errors)
          html += 'BlessingCurses: %s<br/>'%(blessingcurses.errors)
          html += 'BeneficeAfflictions: %s<br/>'%(beneficeafflictions.errors)
          html += 'Armors: %s<br/>'%(armors.errors)
          html += 'Weapons: %s<br/>'%(weapons.errors)
          html += 'Shields: %s<br/>'%(shields.errors)
          html += '</div>'
          templatelink = get_template('collector/character_link.html')
          line = templatelink.render({'c':character_item},request)
      else:
        html = '<div class="classyview">'
        html += 'Form is invalid...'
        html += '<PRE>%s</PRE>'%(formdata)
        html += '</div>'
    else:
      #print("This is a GET request....")
      character_item = get_object_or_404(Character, id=id)
      form = CharacterForm(request.POST or None, instance = character_item)
      skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by('skill_ref__reference'))
      talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by('-value'))
      blessingcurses = BlessingCurseFormSet(instance=character_item)
      beneficeafflictions = BeneficeAfflictionFormSet(instance=character_item)
      armors = ArmorFormSet(instance=character_item)
      weapons = WeaponFormSet(instance=character_item)
      shields = ShieldFormSet(instance=character_item)
      edit_context = {
         'form': form,
         'cid':character_item.id,
         'skills': skills,
         'armors': armors,
         'weapons': weapons,
         'blessingcurses': blessingcurses,
         'beneficeafflictions': beneficeafflictions,
         'talents': talents,
         'shields': shields,
      }
      template = get_template('collector/character_form.html')
      html = template.render(edit_context,request)
      templatelink = get_template('collector/character_link.html')
      line = templatelink.render({'c':character_item},request)
  else:
    html = '<div class="classyview">'
    html += 'This is no ajax !!!'
    html += '</div>'
  context = {
    'character': html,
    'rid': crid,
    'line': line,
  }
  return JsonResponse(context)


def add_character(request):
  """ Add a new character to the universe """
  conf = get_current_config()
  character_item = Character()
  character_item.full_name = '_noname_ %s'%(datetime.datetime.now())
  character_item.epic = conf.epic
  character_item.save()
  return redirect('/')


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
