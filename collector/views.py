from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Character #, Skill, Shield, ShieldRef, Talent, SkillRef, 
from .forms import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, WeaponFormSet, ArmorFormSet, ShieldFormSet
from .utils import render_to_pdf
from django.template.loader import get_template

import json


#from django.views.generic.list import ListView
#from django.views.generic.edit import DeleteView
#from django.urls import reverse_lazy

MAX_CHAR = 10

def index(request):
  character_items = Character.objects.order_by('keyword')
  paginator = Paginator(character_items,MAX_CHAR)
  page = request.GET.get('page')
  character_items = paginator.get_page(page)
  context = {'character_items': character_items}
  return render(request, 'collector/index.html', context)

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

def persona_as_pdf(request,id=None):
  item = get_object_or_404(Character,pk=id)
  context = {
    'c':item,
    'filename':item.rid,
  }
  pdf = render_to_pdf('collector/persona_pdf.html',context)
  return pdf


def recalc(request):
  character_items = Character.objects.all()
  for c in character_items:
    c.save()
  return redirect('/')

def export(request):
  items = Character.objects.order_by('full_name').filter(ready_for_export=True)
  return render(request, 'collector/export.html', {'characters': items}, content_type='text/plain;charset=utf-8' )

def view_persona(request, id=None):
  item = get_object_or_404(Character,pk=id)
  return render(request, 'collector/persona.html', {'c': item})

def view_character(request, id=None):
  if request.is_ajax():
    item = get_object_or_404(Character,pk=id)
    template = get_template('collector/character.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    raise Http404
 
  
  #return render(request, 'collector/character.html', {'c': item})

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
    skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by("skill_ref__reference"))
    talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by("-value"))
    blessingcurses = BlessingCurseFormSet(instance=character_item)
    armors = ArmorFormSet(instance=character_item)
    weapons = WeaponFormSet(instance=character_item)
    shields = ShieldFormSet(instance=character_item)
  return render(request, 'collector/persona_form.html', {'form': form, 'cid':character_item.id, 'skills': skills, 'armors': armors, 'weapons': weapons, 'blessingcurses': blessingcurses, 'talents': talents, 'shields': shields})


#class CharacterDelete(DeleteView):
#  model = Character
#  success_url = reverse_lazy('index')

