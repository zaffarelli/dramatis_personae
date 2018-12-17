#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from scenarist.forms.basic import *
from scenarist.models.events import Event
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin

class EventDetailView(DetailView):
  model = Event
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class EventUpdateView(AjaxFromResponseMixin,UpdateView):
  model = Event
  form_class = EventForm
  context_object_name = 'object'
  template_name_suffix = '_update_form'

class EventAddView(AjaxFromResponseMixin,CreateView):
  model = Event
  form_class = EventForm
  context_object_name = 'object'
  template_name_suffix = '_update_form'  

class EventDeleteView(DeleteView):
  model = Event
