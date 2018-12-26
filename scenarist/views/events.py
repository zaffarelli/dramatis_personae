#  __                           _     _   
# / _\ ___ ___ _ __   __ _ _ __(_)___| |_ 
# \ \ / __/ _ \ '_ \ / _` | '__| / __| __|
# _\ \ (_|  __/ | | | (_| | |  | \__ \ |_ 
# \__/\___\___|_| |_|\__,_|_|  |_|___/\__|
#  
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
