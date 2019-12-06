'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
# utils.py
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from PyPDF2 import PdfFileMerger
import datetime
import os
import logging
from collector.models.tourofduty_ref import TourOfDutyRef


logger = logging.getLogger(__name__)

def render_to_pdf(template_src, context_dict={}):
  """ Render PDF document """
  template = get_template(template_src)
  html = template.render(context_dict)
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')),result) # ISO-8859-1
  if not pdf.err:
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = 'avatar_%s.pdf' % context_dict['filename']
    content = "inline; filename='%s'"% filename
    response['content-disposition'] = content
    return response
  return HttpResponse(pdf.err, content_type='text/plain')

def write_pdf(template_src, context_dict={}):
  template = get_template(template_src)
  html = template.render(context_dict)
  fname = 'avatar_%s.pdf'%(context_dict['filename'])
  filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + fname)
  result = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
  result.close()
 
def get_current_config():
  from collector.models.config import Config
  item = Config.objects.get(is_active=True)
  return item


def make_avatar_appendix(conf):
  """ Creating appendix with the list of avatars from the epic """
  d = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  res = []
  mypath = os.path.join(settings.MEDIA_ROOT, 'pdf/')
  media_resources = os.path.join(settings.MEDIA_ROOT, 'pdf/resources/')
  media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
  mystaticpath = os.path.join(settings.STATIC_ROOT, 'pdf/')
  onlyfiles = [f for f in os.listdir(media_results) if os.path.isfile(os.path.join(media_results, f))]
  pdfs = onlyfiles
  merger = PdfFileMerger()
  merger.append(open('%s__aa_header.pdf'%(media_resources), 'rb'))
  pdfs.sort()
  ep = conf.epic
  cast = ep.get_full_cast()
  i = 0
  for pdf in pdfs:
    if 'avatar_' in pdf:
      arid = pdf.split('avatar_')
      if arid[1].split('.')[0] in cast:
        i += 1
        merger.append(open(media_results+pdf, 'rb'))
  if i>0:
    des = '%sappendix_%s.pdf'%(media_results,conf.epic.shortcut)
    with open(des, 'wb') as fout:
      merger.write(fout)
  return res

def make_epic_corpus(conf):
  res = []
  mypath = os.path.join(settings.MEDIA_ROOT, 'pdf/')
  media_resources = os.path.join(settings.MEDIA_ROOT, 'pdf/resources/')
  media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
  mystaticpath = os.path.join(settings.STATIC_ROOT, 'pdf/')
  merger = PdfFileMerger()
  merger.append(open('%sresources/__es_header.pdf'%(mystaticpath), 'rb'))
  template = get_template('collector/conf_pdf.html')
  context = {'epic':conf.parse_details()}
  html = template.render(context)
  fname = 'c_%s.pdf'%(conf.epic.shortcut)
  filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + fname)
  es_pdf = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), es_pdf)
  es_pdf.close()
  merger.append(open(filename, 'rb'))  
  des = '%scorpus_%s.pdf'%(media_results,conf.epic.shortcut)
  with open(des, 'wb') as fout:
    merger.write(fout)
  return res
  
def export_epic(conf):
  res = {'epic':conf.epic.title}
  comments = []
  comments += make_avatar_appendix(conf)
  comments += make_epic_corpus(conf)
  com = '<br/>'.join(comments)  
  res['comment'] = '<div class="classyview"><p>'+com+'</p></div>'
  media_results = os.path.join(settings.MEDIA_ROOT, 'pdf/results/')
  merger = PdfFileMerger()
  merger.append(open('%scorpus_%s.pdf'%(media_results,conf.epic.shortcut), 'rb'))
  merger.append(open('%sappendix_%s.pdf'%(media_results,conf.epic.shortcut), 'rb'))
  des = '%s%s.pdf'%(media_results,conf.epic.shortcut)
  with open(des, 'wb') as fout:
    merger.write(fout)
  print('> Epic [%s] exported to PDF: [%s]'%(conf.epic.title,des))
  return res


def extract_rules():
  from collector.models.weapon import WeaponRef
  from collector.models.skill_ref import SkillRef
  context = {}

  import datetime
  context['date'] = datetime.datetime.now()

  skills = SkillRef.objects.all().order_by('reference','is_root','is_speciality')
  context['skills'] = skills

  melee_weapons = WeaponRef.objects.filter(category='MELEE')
  context['melee_weapons'] = melee_weapons 
  ranged_weapons = WeaponRef.objects.exclude(category='MELEE')
  context['ranged_weapons'] = ranged_weapons 


  racial = TourOfDutyRef.objects.filter(category='0').order_by('-source')
  context['racial'] = racial 
  castes = ['Nobility', 'Church', 'Guild', 'Alien']
  castes_context = []
  for caste in castes:
    caste_context = {}
    caste_context['name'] = caste
    upbringing = TourOfDutyRef.objects.filter(category='1',caste=caste).order_by('-source')
    caste_context['upbringing'] = upbringing 
    apprenticeship = TourOfDutyRef.objects.filter(category='2',caste=caste).order_by('-source')
    caste_context['apprenticeship'] = apprenticeship
    early_career = TourOfDutyRef.objects.filter(category='3',caste=caste).order_by('-source')
    caste_context['early_career'] = early_career
    castes_context.append(caste_context)
  context['castes'] = castes_context
  tour_of_duty = TourOfDutyRef.objects.filter(category='4').order_by('-source')
  context['tour_of_duty'] = tour_of_duty
  worldly_benefits = TourOfDutyRef.objects.filter(category='5').order_by('-source')
  context['worldly_benefits'] = worldly_benefits
  
  #print(context)
  template = get_template('collector/references.html')
  html = template.render(context)
  fname = 'rules.pdf'
  filename = os.path.join(settings.MEDIA_ROOT, 'pdf/results/' + fname)
  es_pdf = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), es_pdf)
  es_pdf.close()
  
  
