from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import SkillRef, Character, Skill
from .forms import CharacterForm
from django.core.paginator import Paginator

def index(request):
	character_items = Character.objects.order_by('player','-alliance','full_name')
	paginator = Paginator(character_items,15)
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

def refs(request):
	srs = SkillRef.objects.all()
	answer = "References: "
	for sr in srs:
		answer = answer + " " + sr.reference
	return HttpResponse("%s" % answer)


def personae(request):
	ps = Character.objects.all()
	answer = "Characters: "
	for p in ps:
		answer = answer + " (" + p.full_name + " :" + str(p.id) + ") "
	return HttpResponse("%s" % answer)


def view_persona(request, id=None):
	item = get_object_or_404(Character,pk=id)
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
	return render(request, 'collector/character_form.html', {'form': form})

def edit_persona(request,id=None):
	character_item = get_object_or_404(Character, id=id)
	form = CharacterForm(request.POST or None, instance = character_item)
	if form.is_valid():
		form.save()
		return redirect('/view/persona/'+str(character_item.id)+'/')
	return render(request, 'collector/persona_form.html', {'form': form})
