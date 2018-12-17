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
from scenarist.models.dramas import Drama
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin

class DramaDetailView(DetailView):
  model = Drama
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context

class DramaUpdateView(AjaxFromResponseMixin,UpdateView):
  model = Drama
  form_class = DramaForm
  context_object_name = 'object'
  template_name_suffix = '_update_form'

class DramaAddView(AjaxFromResponseMixin,CreateView):
  model = Drama
  form_class = DramaForm
  context_object_name = 'object'
  template_name_suffix = '_update_form'  

class DramaDeleteView(DeleteView):
  model = Drama
