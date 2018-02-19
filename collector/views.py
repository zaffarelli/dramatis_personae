from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import SkillRef, Character, Skill


def index(request):
    latest_character_list = Character.objects.order_by('-pub_date')[:5]
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


def persona(request, character_id):
    character = get_object_or_404(Character,pk=character_id)
    return render(request, 'collector/persona.html', {'character': character})
