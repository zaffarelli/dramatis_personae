#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
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

