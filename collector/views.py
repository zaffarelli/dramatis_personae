from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import SkillRef, Character, Skill
from .forms import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, WeaponFormSet, ArmorFormSet
from django.core.paginator import Paginator
from django.views.generic.list import ListView


def index(request):
  character_items = Character.objects.order_by('-player','-alliance','-challenge')
  paginator = Paginator(character_items,10)
  page = request.GET.get('page')
  character_items = paginator.get_page(page)
  context = {'character_items': character_items}
  return render(request, 'collector/index.html', context)

def recalc(request):
  character_items = Character.objects.all()
  for c in character_items:
    c.save()
  return redirect('/')

def export(request):
  items = Character.objects.order_by("full_name").filter(ready_for_export=True)
  return render(request, 'collector/export.html', {'characters': items}, content_type='text/plain;charset=utf-8' )

def view_persona(request, id=None):
  item = get_object_or_404(Character,pk=id)
  print(item)
  return render(request, 'collector/persona.html', {'c': item})

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
    skv = skills.is_valid()
    tav = talents.is_valid() 
    bcv = blessingcurses.is_valid()
    arv = armors.is_valid()
    wpv = weapons.is_valid()
    if skv and tav and bcv and arv and wpv and form.is_valid():
      skills.save()
      talents.save()
      blessingcurses.save()
      armors.save()
      weapons.save()
      form.save()
      return redirect('/view/persona/'+str(character_item.id)+'/')
  else:
    skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by("-value"))
    talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by("-value"))
    blessingcurses = BlessingCurseFormSet(instance=character_item)
    armors = ArmorFormSet(instance=character_item)
    weapons = WeaponFormSet(instance=character_item)
  return render(request, 'collector/persona_form.html', {'form': form, 'skills': skills, 'armors': armors, 'weapons': weapons, 'blessingcurses': blessingcurses, 'talents': talents})


