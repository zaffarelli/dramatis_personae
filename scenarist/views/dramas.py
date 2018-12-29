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

def add_drama(request):
  """ Add a new character to the universe """
  if request.is_ajax():
    if request.method == 'POST':
      id = request.POST.get('id')
      item = Drama()
      item.act = get_object(Epic,pk=id)
      item.save()
      c[item] = item
      return JsonResponse(c)
  return JsonNotFound

class DramaDeleteView(DeleteView):
  model = Drama
