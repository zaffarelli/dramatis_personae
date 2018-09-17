from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from collector.models.characters import Character
from collector.models.skills import Skill
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, WeaponFormSet, ArmorFormSet, ShieldFormSet
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

MAX_CHAR = 10 # How many avatars per page

def index(request):
  """ The basic page for the application """
  return render(request,'collector/index.html')

def get_list(request,id,slug='none'):
  """ Update the list of characters on the page """
  if request.is_ajax:
    if slug=='none':
      character_items = Character.objects.order_by('ready_for_export','full_name')
    else:
      character_items = Character.objects.order_by('ready_for_export','full_name').filter(keyword=slug)
    paginator = Paginator(character_items,MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    context = {'character_items': character_items}
    template = get_template('collector/list.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
  else:
    Http404

# def by_keyword_personae(request,keyword):
  # character_items = Character.objects.filter(keyword=keyword)
  # paginator = Paginator(character_items,MAX_CHAR)
  # page = request.GET.get('page')
  # character_items = paginator.get_page(page)
  # context = {'character_items': character_items}
  # return render(request, 'collector/index.html', context)

# def by_alliance_personae(request,alliancehash):
  # character_items = Character.objects.filter(alliancehash=alliancehash)
  # paginator = Paginator(character_items,MAX_CHAR)
  # page = request.GET.get('page')
  # character_items = paginator.get_page(page)
  # context = {'character_items': character_items}
  # return render(request, 'collector/index.html', context)

# def by_species_personae(request,species):
  # character_items = Character.objects.filter(category=species)
  # paginator = Paginator(character_items,MAX_CHAR)
  # page = request.GET.get('page')
  # character_items = paginator.get_page(page)
  # context = {'character_items': character_items}
  # return render(request, 'collector/index.html', context)

def pdf_character(request,id=None):
  """ Create and show a character as PDF """
  item = get_object_or_404(Character,pk=id)
  if item.backup() == True:
    answer = '<a class="pdflink" target="_blank" href="pdf/%s.pdf">%s</a>'%(item.rid,item.rid)
  else:
    answer = '<span class="pdflink">no character found</span>'
  return HttpResponse(answer, content_type='text/html')


def recalc(request):
  """ Recalc and export to PDF all avatars """
  character_items = Character.objects.order_by('-player','-ready_for_export','full_name')
  x = 1
  for c in character_items:
    c.pagenum = x
    #c.rid = 'none'
    #if c.role == 'player':
    #  c.role = '04'
    #if c.role == '08' or c.role == 'standard' or c.role == 'brute' or c.role == 'boss' or c.role == 'villain' or c.role == 'grunt' or c.role == 'support' or c.role == 'thug' or c.role == 'nameless':
    #  c.role = '02'
      
    c.save()
    x += 1
  return redirect('/')

def export(request):
  """ XLS export of the characters """
  export_to_xls()
  return redirect('/')

def xls_update(request):
  """ XLS import of data """
  update_from_xls()
  return redirect('/')

#def view_persona(request, id=None):
#  item = get_object_or_404(Character,pk=id)
#  return render(request, 'collector/persona.html', {'c': item})

def view_character(request, id=None):
  """ Ajax view of a character """
  if request.is_ajax():
    print("This is Ajax")
    item = get_object_or_404(Character,pk=id)
    template = get_template('collector/character.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    print("This is NOT Ajax")
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
  crid = ''
  line = ''
  if request.is_ajax():
    if request.method == 'POST':
      cid = request.POST.get('cid')
      character_item = Character.objects.get(pk=cid)
      crid = character_item.rid
      """ FIXME: There is a mistake here that puts " at start and end ...."""
      formdata = json.loads(json.dumps(parse_qs(json.dumps(request.POST['character'])),indent=2))
      #formdata = ast.literal_eval(request.POST['character'])
      #print(type(formdata))
      #print(formdata)
      forms = fs_fics7.sanitize(character_item,formdata)
      fv = False
      if forms == None:
        print('No change for character...')
      else:
        fv = True
      skill_data = extract_formset(formdata,'skill_set')
      talent_data = extract_formset(formdata,'talent_set')
      blessingcurse_data = extract_formset(formdata,'blessingcurse_set')
      armor_data = extract_formset(formdata,'armor_set')
      weapon_data = extract_formset(formdata,'weapon_set')
      shield_data = extract_formset(formdata,'shield_set')
      skills = SkillFormSet(skill_data, instance=character_item)
      talents = TalentFormSet(talent_data, instance=character_item)
      blessingcurses = BlessingCurseFormSet(blessingcurse_data, instance=character_item)
      armors = ArmorFormSet(armor_data, instance=character_item)
      weapons = WeaponFormSet(weapon_data, instance=character_item)
      shields = ShieldFormSet(shield_data, instance=character_item)
      skv = skills.is_valid()
      tav = talents.is_valid() 
      bcv = blessingcurses.is_valid()
      arv = armors.is_valid()
      wpv = weapons.is_valid()
      shv = shields.is_valid()
      if skv and tav and bcv and arv and wpv and fv and shv:        
        skills.save()
        talents.save()
        blessingcurses.save()
        armors.save()
        weapons.save()
        shields.save()
        character_item.save()
        item = get_object_or_404(Character,pk=cid)
        template = get_template('collector/character.html')
        html = template.render({'c':item})
        templatelink = get_template('collector/character_link.html')
        line = templatelink.render({'c':character_item},request)
      else:
        html = '<div class="classyview">'
        html += '<p>Unable to update this character !!!</p>'
        html += 'Skills: %s<br/>'%(skills.errors)
        html += 'Talents: %s<br/>'%(talents.errors)
        html += 'BlessingCurses: %s<br/>'%(blessingcurses.errors)
        html += 'Armors: %s<br/>'%(armors.errors)
        html += 'Weapons: %s<br/>'%(weapons.errors)
        html += 'Shields: %s<br/>'%(shields.errors)
        html += '</div>'
        templatelink = get_template('collector/character_link.html')
        line = templatelink.render({'c':character_item},request)        
    else:
      print("This is a get request....")
      print(request)
      character_item = get_object_or_404(Character, id=id)
      form = CharacterForm(request.POST or None, instance = character_item)
      skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by('skill_ref__reference'))
      talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by('-value'))
      blessingcurses = BlessingCurseFormSet(instance=character_item)
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

# def add_persona(request):
  # if request.method == 'POST':
    # form = CharacterForm(request.POST)
    # if form.is_valid():
      # character_item = form.save(commit=False)
      # character_item.save()
      # return redirect('/')
  # else:
    # form = CharacterForm()
  # return render(request, 'collector/persona_form.html', {'form': form})

def add_character(request):
  character_item = Character()
  character_item.full_name = 'Nameless at %s'%(datetime.datetime.now())
  character_item.save()
  return redirect('/')



# def edit_persona(request,id=None):
  # """ Old static system for edit"""
  # character_item = get_object_or_404(Character, id=id)
  # form = CharacterForm(request.POST or None, instance = character_item)
  # if request.method == 'POST':
    # skills = SkillFormSet(request.POST, request.FILES, instance=character_item)
    # talents = TalentFormSet(request.POST, request.FILES, instance=character_item)
    # blessingcurses = BlessingCurseFormSet(request.POST, request.FILES, instance=character_item)
    # armors = ArmorFormSet(request.POST, request.FILES, instance=character_item)
    # weapons = WeaponFormSet(request.POST, request.FILES, instance=character_item)
    # shields = ShieldFormSet(request.POST, request.FILES, instance=character_item)
    # skv = skills.is_valid()
    # tav = talents.is_valid() 
    # bcv = blessingcurses.is_valid()
    # arv = armors.is_valid()
    # wpv = weapons.is_valid()
    # shv = shields.is_valid()
    # if skv and tav and bcv and arv and wpv and shv and form.is_valid():
      # skills.save()
      # talents.save()
      # blessingcurses.save()
      # armors.save()
      # weapons.save()
      # shields.save()
      # form.save()
      # return redirect('/view/persona/'+str(character_item.id)+'/')
  # else:
    # skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by('skill_ref__reference'))
    # talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by('-value'))
    # blessingcurses = BlessingCurseFormSet(instance=character_item)
    # armors = ArmorFormSet(instance=character_item)
    # weapons = WeaponFormSet(instance=character_item)
    # shields = ShieldFormSet(instance=character_item)
  # return render(request, 'collector/persona_form.html', {'form': form, 'cid':character_item.id, 'skills': skills, 'armors': armors, 'weapons': weapons, 'blessingcurses': blessingcurses, 'talents': talents, 'shields': shields})

@csrf_exempt
def skill_touch(request):
  """ Touching skills to edit them in the view """
  if request.is_ajax():
    answer = 'error'
    if request.method == 'POST':
      #print(request.POST)
      skill_id = request.POST.get('skill')
      sid = int(skill_id)
      fingerval = request.POST.get('finger')
      finger = int(fingerval)
      #print('%s %s'%(sid,finger))
      skill_item = get_object_or_404(Skill,id=sid)
      skill_item.value += int(finger)
      skill_item.save()
      answer = skill_item.value
    return HttpResponse(answer, content_type='text/html')
  return Http404


