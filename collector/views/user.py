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
        from collector.models.character import DRAMA_SEATS
        main_characters = Character.objects.filter(player=request.user.username.capitalize())
        blokes = Bloke.objects.filter(character__in=main_characters)
        blokes_characters = []
        for b in blokes:
            b.npc.intimacy = b.level
            blokes_characters.append(b.npc)
        full_lists = {}
        for team in reversed(DRAMA_SEATS):
            full_lists[team[1]] = []
        for b in blokes_characters:
            try:
                x = b.get_team_display()
                full_lists[x].append(b)
            except:
                pass
        for team in reversed(DRAMA_SEATS):
            if len(full_lists[team[1]]) == 0:
                full_lists.pop(team[1])
        context = {'main_characters':main_characters,'blokes': full_lists}
        template = get_template('collector/profile.html')
        html = template.render(context, request)
        messages.info(request, f'Display {request.user.username.capitalize()} profile.')
        return HttpResponse(html, content_type='text/html')
    return HttpResponse(status=204)

