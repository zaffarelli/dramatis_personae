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
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, \
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
    from collector.tasks import recalc_avatar
    conf = get_current_config()
    character_items = Character.objects.filter(epic=conf.epic).order_by('-player', 'full_name')
    x = 1
    messages.info(request, 'Starting recalculation tasks...')
    for c in character_items:
        recalc_avatar.delay(c.rid, x)
        x += 1
        messages.info(request, f'Recalculating {c.full_name}')
    messages.info(request, 'Recalculation tasks started.')
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
