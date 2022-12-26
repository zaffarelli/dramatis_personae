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
from scenarist.models.adventures import Adventure
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse
from django.contrib import messages


class AdventureDetailView(DetailView):
    model = Adventure

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["adventure"]}')
        return context


class AdventureUpdateView(AjaxFromResponseMixin,UpdateView):
    model = Adventure
    form_class = AdventureForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


class AdventureDeleteView(DeleteView):
    model = Adventure


@csrf_exempt
def add_adventure(request):
    from django.utils import timezone
    if is_ajax(request):
      if request.method == 'POST':
        id_ = request.POST.get('id')
        id = id_.split('_')[1]
        item = Adventure()
        item.title = str(timezone.now())
        item.act = get_object_or_404(Adventure, pk=id)
        item.save()
    return HttpResponse(status=204)
