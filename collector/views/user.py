import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from collector.forms.user import LoginForm
from django.contrib import messages
from collector.models.character import Character
from collector.models.bloke import Bloke
from django.template.loader import get_template


def do_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
        messages.info(request, f'This is the POST to authenticate from the form data.')
        return render(request, 'collector/login.html', {'form': form})
    else:
        form = LoginForm(request.GET)
        messages.info(request, f'This is the GET to display the login form.')
        return render(request, 'collector/login.html', {'form': form})


def do_profile(request):
    if request.method == "POST":
        main_characters = Character.objects.filter(player=request.user.username.capitalize())
        blokes = Bloke.objects.filter(character__in=main_characters)
        active_blokes = []
        for b in blokes:
            active_blokes.append(b.npc.rid)
        other_characters = Character.objects.filter(player='')
        for c in other_characters:
            if  c.rid in active_blokes:
                c.checked = True
            else:
                c.checked = False
        context = {'main_characters':main_characters,'blokes': other_characters, 'code':'test'}
        template = get_template('collector/profile.html')
        html = template.render(context, request)
        messages.info(request, f'Display {request.user.username.capitalize()} profile.')
        return HttpResponse(html, content_type='text/html')
    return HttpResponse(status=204)


def user_blokes(request, team_type='others'):
    if request.method == "GET":
        from collector.models.character import BLOKES, DRAMA_SEATS
        main_characters = Character.objects.filter(player=request.user.username.capitalize())
        blokes = Bloke.objects.filter(character__in=main_characters)
        blokes_characters = []
        for b in blokes:
            print(b.npc.team)
            if b.npc.team in BLOKES[team_type]:
                b.npc.intimacy = b.level
                blokes_characters.append(b.npc)
        full_lists = {}
        print(f'Blokes: {blokes_characters}')
        for team in BLOKES[team_type]:
            full_lists[team] = []
        print(f'Full List: {full_lists}')
        for b in blokes_characters:
            print(b.team)
            full_lists[b.team].append(b)
        print(f'Filled Full List: {full_lists}')
        for team in BLOKES[team_type]:
            if len(full_lists[team]) == 0:
                full_lists.pop(team)
        context = {'blokes': full_lists}
        template = get_template('collector/buddies.html')
        html = template.render(context, request)
        messages.info(request, f'Display {request.user.username.capitalize()} {team_type}.')
        return HttpResponse(html, content_type='text/html')
    return HttpResponse(status=204)


def user_friends(request):
    return user_blokes(request,'allies')

def user_foes(request):
    return user_blokes(request,'foes')

def user_others(request):
    return user_blokes(request,'others')

def user_persystem(request):
    pass