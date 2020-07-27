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
import os
from urllib.parse import unquote
from urllib.parse import parse_qs
from collector.utils import fs_fics7
from django.views.decorators.csrf import csrf_exempt

import datetime
from collector.utils.xls_collector import export_to_xls, update_from_xls
from collector.utils.basic import get_current_config
from collector.templatetags.fics_filters import as_bullets
from django.http import FileResponse, Http404
from django.conf import settings
from django.contrib import messages


def pdf_show(request, slug):
    try:
        fname = 'avatar_%s.pdf' % (slug)
        filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + fname)
        return FileResponse(open(filename, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
