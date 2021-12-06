"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from scenarist.forms.basic import *
from scenarist.models.acts import Act
from django.shortcuts import get_object_or_404
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import datetime


class ActDetailView(DetailView):
    model = Act

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["act"]}')
        return context


class ActUpdateView(AjaxFromResponseMixin,UpdateView):
    model = Act
    form_class = ActForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


def add_act(request):
    if request.is_ajax():
        if request.method == 'POST':
            full_id = request.POST.get('id')
            id = full_id.split('_')[1]
            item = Act()
            item.drama = Drama.objects.get(pk=id)
            item.epic = item.drama.epic
            item.title = datetime.datetime.now()
            item.save()
            c = {}
            return JsonResponse(c)
    return HttpResponse(status=204)


class ActDeleteView(DeleteView):
    model = Act
