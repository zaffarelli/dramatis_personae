# _________        .__  .__                 __                
# \_   ___ \  ____ |  | |  |   ____   _____/  |_  ___________ 
# /    \  \/ /  _ \|  | |  | _/ __ \_/ ___\   __\/  _ \_  __ \
# \     \___(  <_> )  |_|  |_\  ___/\  \___|  | (  <_> )  | \/
#  \______  /\____/|____/____/\___  >\___  >__|  \____/|__|   
#         \/                      \/     \/                   
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
from urllib.parse import unquote
from urllib.parse import parse_qs
from collector.utils import fs_fics7
from django.views.decorators.csrf import csrf_exempt
import datetime
from collector.utils.xls_collector import export_to_xls, update_from_xls
from collector.utils.basic import get_current_config


def pdf_character(request,id=None):
  """ Create and show a character as PDF """
  item = get_object_or_404(Character,pk=id)
  if item.backup() == True:
    answer = '<a class="pdflink" target="_blank" href="pdf/%s.pdf">%s</a>'%(item.rid,item.rid)
  else:
    answer = '<span class="pdflink">no character found</span>'
  return HttpResponse(answer, content_type='text/html')



def recalc(request):
  """ Recalc and export to PDF all avatars """  
  conf = get_current_config()
  character_items = Character.objects.filter(epic=conf.epic).order_by('-player','-ready_for_export','full_name')
  x = 1
  for c in character_items:
    c.pagenum = x     
    c.save()
    x += 1
  return redirect('/')

def export(request):
  """ XLS export of the characters """
  export_to_xls()
  return redirect('/')

def xls_update(request):
  """ XLS import of data """
  update_from_xls()
  return redirect('/')
