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
from django.shortcuts import get_object_or_404
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
      item.act = get_object_or_404(Act,pk=id)
      item.epic = item.act.epic
      item.name = "new event"
      item.save()
      #c[item] = item
      #print("toto")
      return JsonResponse(c)
  return JsonNotFound

class ActDeleteView(DeleteView):
  model = Act
