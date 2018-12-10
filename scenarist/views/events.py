from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from scenarist.models.events import Event

def view_event(request, id=None):
  """ Ajax view of an event """
  if request.is_ajax():
    item = get_object_or_404(Event,pk=id)
    template = get_template('scenarist/event.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    raise Http404

def edit_event(request,id):
  pass
