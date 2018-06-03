from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from .models import Character, Skill#, Shield, ShieldRef, Talent, SkillRef, 
from .forms import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, WeaponFormSet, ArmorFormSet, ShieldFormSet
from .utils import render_to_pdf
from django.template.loader import get_template, render_to_string
from django.template import RequestContext
import json
from urllib.parse import parse_qs
from collector import fs_fics7
from django.views.decorators.csrf import csrf_exempt

MAX_CHAR = 10 # How many avatars per page

def index(request):
  """ Index page """
  character_items = Character.objects.order_by('-player','-ready_for_export','full_name')
  paginator = Paginator(character_items,MAX_CHAR)
  page = request.GET.get('page')
  character_items = paginator.get_page(page)
  context = {'character_items': character_items}
  return render(request,'collector/index.html', context)

def get_list(request,id):
  """ List update page """
  if request.is_ajax:
    character_items = Character.objects.order_by('-player','-ready_for_export','full_name')
    paginator = Paginator(character_items,MAX_CHAR)
    page = id
    character_items = paginator.get_page(page)
    context = {'character_items': character_items}

    template = get_template('collector/list.html')
    html = template.render(context)
    return HttpResponse(html, content_type='text/html')
    
    #return render(request,'collector/list.html', context)
  else:
    Http404

def by_keyword_personae(request,keyword):
  character_items = Character.objects.filter(keyword=keyword)
  paginator = Paginator(character_items,MAX_CHAR)
  page = request.GET.get('page')
  character_items = paginator.get_page(page)
  context = {'character_items': character_items}
  return render(request, 'collector/index.html', context)

def by_alliance_personae(request,alliancehash):
  character_items = Character.objects.filter(alliancehash=alliancehash)
  paginator = Paginator(character_items,MAX_CHAR)
  page = request.GET.get('page')
  character_items = paginator.get_page(page)
  context = {'character_items': character_items}
  return render(request, 'collector/index.html', context)

def by_species_personae(request,species):
  character_items = Character.objects.filter(category=species)
  paginator = Paginator(character_items,MAX_CHAR)
  page = request.GET.get('page')
  character_items = paginator.get_page(page)
  context = {'character_items': character_items}
  return render(request, 'collector/index.html', context)

def pdf_character(request,id=None):
  item = get_object_or_404(Character,pk=id)
  if item.backup() == True:
    answer = "<a class='pdflink' target='_blank' href='pdf/%s.pdf'>%s</a>"%(item.rid,item.rid)
  else:
    answer = "<span class='pdflink'>no character found</span>"
  return HttpResponse(answer, content_type='text/html')


def recalc(request):
  character_items = Character.objects.order_by('-player','-ready_for_export','full_name')
  x = 1
  for c in character_items:
    c.pagenum = x
    c.save()
    x += 1
  return redirect('/')

def export(request):
  items = Character.objects.order_by('full_name').filter(ready_for_export=True)
  return render(request, 'collector/export.html', {'characters': items}, content_type='text/plain;charset=utf-8' )

def view_persona(request, id=None):
  item = get_object_or_404(Character,pk=id)
  return render(request, 'collector/persona.html', {'c': item})

def view_character(request, id=None):
  """ Ajax view of a character """
  if request.is_ajax():
    item = get_object_or_404(Character,pk=id)
    template = get_template('collector/character.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    raise Http404

"""
def pdf_character(request, id=None):

  if request.is_ajax():
    item = get_object_or_404(Character,pk=id)
    context = {
      'c':item,
      'filename':item.rid,
    }
    pdf = render_to_pdf('collector/persona_pdf.html',context)
    return pdf
  else:
    raise Http404
"""


def old_extract_formset(rqp,s):
  res = {'management':{},'data':{}}
  for k in rqp:
    if s in k:
      key = k.split('-')
      if 'INITIAL_FORMS' in k or 'TOTAL_FORMS' in k or 'MIN_NUM_FORMS' in k or 'MAX_NUM_FORMS' in k:
        res['management'][key[1]] = rqp[k]        
      else:
        num = key[1]
        att = key[2]
        val = rqp[k]
        if not num in res['data']:
          res['data'][num] = {}
        res['data'][num][att] = val
  print(res)
  return res

def extract_formset(rqp,s):
  res = {}
  for k in rqp:
    if s in k:
      res[k] = rqp[k]
  print(s)    
  print(res)
  return res

def edit_character(request,id=None):
  """ Ajax edit of a character """
  if request.is_ajax():
    if request.method == "POST":
      
      cid = request.POST.get("cid")
      #print("cid is %s"%cid)
      #character_item = get_object_or_404(Character, id=cid)
      character_item = Character.objects.get(pk=cid)
      #print("%s request is post "%character_item)
      formdata = json.loads(json.dumps(parse_qs(json.dumps(request.POST['character'])),indent=2))      
      forms = fs_fics7.sanitize(character_item,formdata)
      
      #print(formdata)
      
      #fv = character_item.update_from_json(forms)
      
      #fv = True
      #fv = character_item.save()
      form = CharacterForm(forms, instance = character_item)      
      fv = form.is_valid()
      skill_data = extract_formset(formdata,'skill_set')
      talent_data = extract_formset(formdata,'talent_set')
      blessingcurse_data = extract_formset(formdata,'blessingcurse_set')
      armor_data = extract_formset(formdata,'armor_set')
      weapon_data = extract_formset(formdata,'weapon_set')
      shield_data = extract_formset(formdata,'shield_set')
#      character_item.save()
#      print(fv)
      skills = SkillFormSet(skill_data, request.FILES, instance=character_item)
      for x in skills:
        print(x.as_p)
        print("------------------------------------------------------------------------------")
      skv = skills.is_valid()
      print(skills.errors)
      talents = TalentFormSet(talent_data, request.FILES, instance=character_item)
      tav = talents.is_valid() 
      blessingcurses = BlessingCurseFormSet(blessingcurse_data, request.FILES, instance=character_item)
      bcv = blessingcurses.is_valid()
      armors = ArmorFormSet(armor_data, request.FILES, instance=character_item)
      arv = armors.is_valid()
      weapons = WeaponFormSet(weapon_data, request.FILES, instance=character_item)
      wpv = weapons.is_valid()
      shields = ShieldFormSet(shield_data, request.FILES, instance=character_item)
      shv = shields.is_valid()
      #print("Forms created")
      
      
      
      
      
      
      
      
      if skv and tav and bcv and arv and wpv and shv and fv:
      #if fv:
        print("Forms are valid")      
        print("%s forms are valid"%character_item)
        skills.save()
        talents.save()
        blessingcurses.save()
        armors.save()
        weapons.save()
        shields.save()
        form.save()
        print("%s form saved"%character_item)
        item = get_object_or_404(Character,pk=cid)
        template = get_template('collector/character.html')
        html = template.render({'c':item})
        return HttpResponse(html, content_type='text/html')
        #return redirect('ajax/view/character/'+str(character_item.id)+'/')
    else:
      character_item = get_object_or_404(Character, id=id)
      form = CharacterForm(request.POST or None, instance = character_item)
      skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by("skill_ref__reference"))
      talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by("-value"))
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
      return HttpResponse(html, content_type='text/html')
  else:
    raise Http404

def add_persona(request):
  if request.method == "POST":
    form = CharacterForm(request.POST)
    if form.is_valid():
      character_item = form.save(commit=False)
      character_item.save()
      return redirect('/')
  else:
    form = CharacterForm()
  return render(request, 'collector/persona_form.html', {'form': form})

def edit_persona(request,id=None):
  """ Old static system for edit"""
  character_item = get_object_or_404(Character, id=id)
  form = CharacterForm(request.POST or None, instance = character_item)
  if request.method == "POST":
    skills = SkillFormSet(request.POST, request.FILES, instance=character_item)
    talents = TalentFormSet(request.POST, request.FILES, instance=character_item)
    blessingcurses = BlessingCurseFormSet(request.POST, request.FILES, instance=character_item)
    armors = ArmorFormSet(request.POST, request.FILES, instance=character_item)
    weapons = WeaponFormSet(request.POST, request.FILES, instance=character_item)
    shields = ShieldFormSet(request.POST, request.FILES, instance=character_item)
    skv = skills.is_valid()
    tav = talents.is_valid() 
    bcv = blessingcurses.is_valid()
    arv = armors.is_valid()
    wpv = weapons.is_valid()
    shv = shields.is_valid()
    if skv and tav and bcv and arv and wpv and shv and form.is_valid():
      skills.save()
      talents.save()
      blessingcurses.save()
      armors.save()
      weapons.save()
      shields.save()
      form.save()
      return redirect('/view/persona/'+str(character_item.id)+'/')
  else:
    skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by('skill_ref__reference'))
    talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by('-value'))
    blessingcurses = BlessingCurseFormSet(instance=character_item)
    armors = ArmorFormSet(instance=character_item)
    weapons = WeaponFormSet(instance=character_item)
    shields = ShieldFormSet(instance=character_item)
  return render(request, 'collector/persona_form.html', {'form': form, 'cid':character_item.id, 'skills': skills, 'armors': armors, 'weapons': weapons, 'blessingcurses': blessingcurses, 'talents': talents, 'shields': shields})

@csrf_exempt
def skill_touch(request):
  """ Touching skills to edit them in the view """
  if request.is_ajax():
    answer = 'error'
    if request.method == 'POST':
      print(request.POST)
      skill_id = request.POST.get('skill')
      sid = int(skill_id)
      fingerval = request.POST.get('finger')
      finger = int(fingerval)
      print("%s %s"%(sid,finger))
      skill_item = get_object_or_404(Skill,id=sid)
      skill_item.value += int(finger)
      skill_item.save()
      answer = skill_item.value
    return HttpResponse(answer, content_type='text/html')
  return Http404


