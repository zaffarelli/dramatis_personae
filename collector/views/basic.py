#    ___      _ _           _             
#   / __\___ | | | ___  ___| |_ ___  _ __ 
#  / /  / _ \| | |/ _ \/ __| __/ _ \| '__|
# / /__| (_) | | |  __/ (__| || (_) | |   
# \____/\___/|_|_|\___|\___|\__\___/|_|   
#                                        
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator

from collector.models.characters import Character
from collector.models.skills import Skill
from collector.forms.basic import CharacterForm, SkillFormSet, TalentFormSet, BlessingCurseFormSet, BeneficeAfflictionFormSet, WeaponFormSet, ArmorFormSet, ShieldFormSet
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

@csrf_exempt
def skill_touch(request):
  """ Touching skills to edit them in the view """
  if request.is_ajax():
    answer = 'error'
    if request.method == 'POST':
      #print(request.POST)
      skill_id = request.POST.get('skill')
      sid = int(skill_id)
      fingerval = request.POST.get('finger')
      finger = int(fingerval)
      #print('%s %s'%(sid,finger))
      skill_item = get_object_or_404(Skill,id=sid)
      skill_item.value += int(finger)
      skill_item.save()
      answer = as_bullets(skill_item.value)
    return HttpResponse(answer, content_type='text/html')
  return Http404

def pdf_show(request,slug):
  try:
    fname = 'avatar_%s.pdf'%(slug)
    filename = os.path.join(settings.MEDIA_ROOT, 'pdf/' + fname)
    #print(filename)    
    return FileResponse(open(filename, 'rb'), content_type='application/pdf')
  except FileNotFoundError:
    raise Http404()

