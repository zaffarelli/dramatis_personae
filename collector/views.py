from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from collector.models import SkillRef, Character, Skill
from .forms import PersonaForm

def index(request):
	latest_character_list = Character.objects.order_by('full_name')
	context = {'latest_character_list': latest_character_list}
	return render(request, 'collector/index.html', context)


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
	return render(request, 'collector/persona.html', {'character': item})

def add_persona(request):
	if request.method == "POST":
		form = PersonaForm(request.POST)
		if form.is_valid():
			persona_item = form.save(commit=False)
			persona_item.save()
			return redirect('/')
	else:
		form = PersonaForm()
	return render(request, 'collector/persona_form.html', {'form': form})

def edit_persona(request,id=None):
	persona_item = get_object_or_404(Character, id=id)
	form = PersonaForm(request.POST or None, instance = persona_item)
	if form.is_valid():
		form.save()
		return redirect('/view/persona/'+str(persona_item.id)+'/')
	return render(request, 'collector/persona_form.html', {'form': form})
