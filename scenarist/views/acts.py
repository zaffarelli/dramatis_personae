'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from scenarist.forms.basic import *
from scenarist.models.acts import Act
from scenarist.models.dramas import Drama
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

def add_act(request):
  """ Add a new character to the universe """
  if request.is_ajax():
    if request.method == 'POST':
      id = request.POST.get('id')
      item = Event()
      item.drama = get_object(Drama,pk=id)
      item.save()
      c[item] = item
      return JsonResponse(c)
  return JsonNotFound

class ActDeleteView(DeleteView):
  model = Act
