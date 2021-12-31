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
from scenarist.models.events import Event
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse
from django.contrib import messages


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["event"]}')
        return context


class EventUpdateView(AjaxFromResponseMixin,UpdateView):
    model = Event
    form_class = EventForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


class EventDeleteView(DeleteView):
    model = Event


@csrf_exempt
def add_event(request):
    if request.is_ajax():
      if request.method == 'POST':
        id_ = request.POST.get('id')
        id = id_.split('_')[1]
        item = Event()
        from django.utils import timezone
        item.title = str(timezone.now())
        item.act = get_object_or_404(Act, pk=id)
        item.save()
        return JsonResponse(item.to_json())
    return HttpResponse(status=204)
