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
from scenarist.models.acts import Act
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin

class ActDetailView(DetailView):
  model = Act
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class ActUpdateView(AjaxFromResponseMixin,UpdateView):
  model = Act
  form_class = ActForm
  context_object_name = 'object'
  template_name_suffix = '_update_form'

class ActAddView(AjaxFromResponseMixin,CreateView):
  model = Act
  form_class = ActForm
  context_object_name = 'object'
  template_name_suffix = '_update_form'  

class ActDeleteView(DeleteView):
  model = Act
