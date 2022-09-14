"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import datetime
from scenarist.forms.basic import *
from scenarist.models.scenes import Scene
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse
from django.contrib import messages


class SceneDetailView(DetailView):
    model = Scene

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["scene"]}')
        return context


class SceneUpdateView(AjaxFromResponseMixin,UpdateView):
    model = Scene
    form_class = SceneForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


class SceneDeleteView(DeleteView):
    model = Scene


@csrf_exempt
def add_scene(request):
    from django.utils import timezone
    if request.is_ajax():
      if request.method == 'POST':
        from scenarist.models.adventures import Adventure
        id_ = request.POST.get('id')
        id = id_.split('_')[1]
        item = Scene()
        item.title = str(timezone.now())
        item.adventure = Adventure.objects.get(pk=id)
        item.save()
    return HttpResponse(status=204)
