#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from scenarist.models.epics import Epic

def view_epic(request, id=None):
  """ Ajax view of an event """
  if request.is_ajax():
    item = get_object_or_404(Event,pk=id)
    template = get_template('scenarist/epic.html')
    html = template.render({'c':item})
    return HttpResponse(html, content_type='text/html')
  else:
    raise Http404

def edit_epic(request,id):
  pass
