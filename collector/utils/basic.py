
# utils.py
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



def render_to_pdf(template_src, context_dict={}):
  """ Render PDF document """
  template = get_template(template_src)
  html = template.render(context_dict)
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')),result) # ISO-8859-1
  if not pdf.err:
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = '%s.pdf' % context_dict['filename']
    content = "inline; filename='%s'"% filename
    response['content-disposition'] = content
    return response
  return HttpResponse(pdf.err, content_type='text/plain')

def write_pdf(template_src, context_dict={}):
  template = get_template(template_src)
  html = template.render(context_dict)
  filename = './collector/pdf/%s.pdf' % context_dict['filename']
  result = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
  result.close()

def get_current_config():
  from collector.models.configs import Config
  item = Config.objects.get(is_active=True)
  return item

def debug_print(str):
  from collector.utils.fics_references import DEBUG_ALL
  if DEBUG_ALL:
    print(str)
