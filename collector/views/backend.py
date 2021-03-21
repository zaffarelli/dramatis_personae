'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from collector.models.character import Character
from collector.models.skill import Skill
from collector.forms.basic import CharacterForm, SkillFormSet, BlessingCurseFormSet, \
    BeneficeAfflictionFormSet, WeaponFormSet, ArmorFormSet, ShieldFormSet
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
from django.contrib import messages
from collector.utils.xls_collector import export_to_xls, update_from_xls
from collector.utils.basic import get_current_config, extract_rules
from collector.utils.gs_export import update_gss


def pdf_character(request, id=None):
    """ Create and show a character as PDF """
    item = get_object_or_404(Character, pk=id)
    if item.backup() == True:
        answer = '<a class="pdflink" target="_blank" href="pdf/results/avatars/%s.pdf">%s</a>' % (item.rid, item.rid)
    else:
        answer = '<span class="pdflink">no character found</span>'
    messages.info(request, 'PDF created.')
    return HttpResponse(status=204)


def recalc(request):
    """ Recalc and export to PDF all avatars """

    campaign = get_current_config()
    cast = campaign.get_full_cast()
    character_items = []
    for rid in cast:
        character_item = campaign.avatars.get(rid=rid)
        character_items.append(character_item)
    #character_items = Character.objects.order_by('-player', 'full_name')
    x = 1
    for c in character_items:
        c.need_fix = True
        c.need_pdf = True
        x += 1
        messages.info(request, f'Recalculating {c.full_name}')
        c.save()
    return HttpResponse(status=204)


def export(request):
    """ XLS export of the characters """
    export_to_xls()
    messages.info(request, 'Exported to XLS spreadsheet...')
    return HttpResponse(status=204)


def xls_update(request):
    """ XLS import of data """
    update_from_xls()
    return HttpResponse(status=204)


def gss_update(request):
    update_gss()
    messages.info(request, 'Exported to Google spreadsheet...')
    return HttpResponse(status=204)


def pdf_rules(request):
    """ Create and show a character as PDF """
    extract_rules()
    messages.info(request, 'Rebuilding Rules reference...')
    return HttpResponse(status=204)


def roll_dice(request, slug):
    context = {}
    contstant = 0
    formula = slug.replace("i", "!").replace("_", " ").replace("x", "+")
    print(formula)
    actions = formula.split("+")
    dice = formula[0].split("d")
    if len(actions) > 1:
        constant = int(actions[1])
    print(dice[0])
    total = 0
    for x in range(1, int(dice[0])):
        r, d = fs_fics7.d12x()
        total += r
    print(r)
    print(d)
    context = {
        'rolls': d,
        'mods': constant,
        'total': total,
    }
    return JsonResponse(context)


def bloke_selector(request):
    if request.method == "POST":
        return HttpResponse(status=204)
    else:
        from collector.models.bloke import Bloke, BLOKE_LEVELS
        levels = []
        for x in BLOKE_LEVELS:
            levels.append({'value':x[0],'text':x[1]})
        other_characters = []
        players = ['Delphine','Chninkel','Marie','Lustus','Taz']
        for player in players:
            main_characters = Character.objects.filter(player=player)
            blokes = Bloke.objects.filter(character__in=main_characters)
            active_blokes = []
            for b in blokes:
                active_blokes.append({'character':b.npc,'intimacy':b.level})
            npc = Character.objects.filter(player='')
            for c in npc:
                c.intimacy = 'none'
                for a in active_blokes:
                    if c.rid == a['character'].rid:
                        c.intimacy = a['intimacy']
            other_characters.append({'player':player,'blokes':npc})
        context = {'blokes': other_characters, 'choices':levels}
        template = get_template('collector/blokes.html')
        html = template.render(context, request)
        messages.info(request, f'Blokes selector loaded.')
        response = { 'mosaic': html}
        return JsonResponse(response)