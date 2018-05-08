from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import SkillRef, Character, Skill
from .forms import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, WeaponFormSet, ArmorFormSet
from django.core.paginator import Paginator


def index(request):
	character_items = Character.objects.order_by('-player','-alliance','-challenge')
	paginator = Paginator(character_items,25)
	page = request.GET.get('page')
	character_items = paginator.get_page(page)
	context = {'character_items': character_items}
	return render(request, 'collector/index.html', context)

def recalc(request):
	character_items = Character.objects.all()
	for c in character_items:
		c.fix()
		c.save()
	skill_items = Skill.objects.all()
	for s in skill_items:
		s.fix()
		s.save()

	return redirect('/')

#def refs(request):
#	srs = SkillRef.objects.all()
#	answer = "References: "
#	for sr in srs:
#		answer = answer + " " + sr.reference
#	return HttpResponse("%s" % answer)


def personae(request):
	ps = Character.objects.all()
	answer = "Characters: "
	for p in ps:
		answer = answer + " (" + p.full_name + " :" + str(p.id) + ") "
	return HttpResponse("%s" % answer)


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
  skills = SkillFormSet(instance=character_item, queryset=character_item.skill_set.order_by("-value"))
  talents = TalentFormSet(instance=character_item, queryset=character_item.talent_set.order_by("-value"))
  blessingcurses = BlessingCurseFormSet(instance=character_item)
  armors = ArmorFormSet(instance=character_item)
  weapons = WeaponFormSet(instance=character_item)
  if skills.is_valid():
    if talents.is_valid():
      if blessingcurses.is_valid():
        if armors.is_valid():
          if weapons.save():
            if form.is_valid():
              skills.save()
              talents.save()
              blessingcurses.save()
              armors.save()
              weapons.save()         
              form.save()
              return redirect('/view/persona/'+str(character_item.id)+'/')
            else:
              print(form)
          else:
            print(weapons)
        else:
          print(armors)
      else:
        print (blessingcurses)
    else:
      print(talents)
  else:
    print("skills are invalid!")
    print(skills)
  return render(request, 'collector/persona_form.html', {'form': form, 'skills': skills, 'armors': armors, 'weapons': weapons, 'blessingcurses': blessingcurses, 'talents': talents})


