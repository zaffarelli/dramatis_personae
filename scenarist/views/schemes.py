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
from scenarist.models.schemes import Scheme
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse
from django.contrib import messages


class SchemeDetailView(DetailView):
    model = Scheme

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["scheme"]}')
        return context


class SchemeUpdateView(AjaxFromResponseMixin, UpdateView):
    model = Scheme
    form_class = SchemeForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


class SchemeDeleteView(DeleteView):
    model = Scheme


@csrf_exempt
def add_scheme(request):
    from django.utils import timezone
    if is_ajax(request):
        if request.method == 'POST':
            id_ = request.POST.get('id')
            id = id_.split('_')[1]
            item = Scheme()
            item.title = str(timezone.now())
            item.save()
    return HttpResponse(status=204)
