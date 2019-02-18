
# utils.py
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
from PyPDF2 import PdfFileMerger
#from os import listdir
#from os.path import isfile, join
import datetime
import os
import logging

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
  filename = os.path.join(settings.MEDIA_ROOT, 'pdf/' + fname)
  #filename = './static/pdf/%s.pdf' % context_dict['filename']
  result = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
  result.close()

def get_current_config():
  from collector.models.configs import Config
  item = Config.objects.get(is_active=True)
  return item

def debug_print(s,level='log'):
  from collector.utils.fics_references import DEBUG_ALL
  if DEBUG_ALL:
    print(s)
  else:
    if level=='debug':
      logger.debug(s)
    elif level=='error':
      logger.error(s)
    elif level=='info':
      logger.info(s)
    elif level=='warning':
      logger.warning(s)
    elif level=='critical':
      logger.critical(s)
    else:
      logger.debug(s)

def make_avatar_appendix(conf):
  """ Creating appendix with the list of avatars from the epic """
  d = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  res = []
  mypath = os.path.join(settings.MEDIA_ROOT, 'pdf/')
  res.append('Working in path %s.'%(mypath))
  onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
  pdfs = onlyfiles
  merger = PdfFileMerger()
  res.append('Opening... header')
  merger.append(open('%s___header.pdf'%(mypath), 'rb'))
  pdfs.sort()

  # getting relevant list
  ep = conf.epic
  cast = ep.get_full_cast()
  
  i = 0
  for pdf in pdfs:
    if 'avatar_' in pdf:
      x = pdf.split('avatar_')
      res.append('%s'%(x))
      if x[1].split('.')[0] in cast:
        i += 1
        merger.append(open(mypath+pdf, 'rb'))
        res.append('Adding %s'%(mypath+pdf))
  if i>0:
    des = '%saa_%s.pdf'%(mypath,conf.epic.shortcut)
    with open(des, 'wb') as fout:
      merger.write(fout)
    res.append('Writing... %d characters in %s'%(i,des))
  return res

def make_epic_corpus(conf):
  res = []
  res.append('Building Epic Corpus...')
  template = get_template('collector/conf_pdf.html')
  context = {'epic':conf.parse_details()}
  html = template.render(context)
  fname = 'corpus_%s.pdf'%(conf.epic.shortcut)
  filename = os.path.join(settings.MEDIA_ROOT, 'pdf/' + fname)
  result = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
  result.close()
  return res
  
def export_epic(conf):
  res = {'epic':conf.epic.title}
  comments = []
  comments += make_avatar_appendix(conf)
  comments += make_epic_corpus(conf)
  com = '<br/>'.join(comments)
  res['comment'] = '<div class="classyview"><p>'+com+'</p></div>'
  return res
