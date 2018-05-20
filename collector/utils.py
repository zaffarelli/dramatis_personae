
# utils.py
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
  template = get_template(template_src)
  html = template.render(context_dict)
  result = BytesIO()
  pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")),result) # ISO-8859-1
  if not pdf.err:
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = "%s.pdf" % context_dict['filename']
    content = "inline; filename='%s'"% filename
    response['content-disposition'] = content
    return response
  return HttpResponse(pdf.err, content_type='text/plain')

def write_pdf(template_src, context_dict={}):
  template = get_template(template_src)
  html = template.render(context_dict)
  filename = "./collector/pdf/%s.pdf" % context_dict['filename']
  result = open(filename, 'wb')
  pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
  result.close()
