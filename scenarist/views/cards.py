"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_exempt
from scenarist.forms.basic import *
from scenarist.models.cards import Card
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone


class CardDetailView(DetailView):
    model = Card

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["card"]}')
        return context


class CardUpdateView(AjaxFromResponseMixin, UpdateView):
    model = Card
    form_class = CardForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


class CardDeleteView(DeleteView):
    model = Card


@csrf_exempt
def add_card(request):
    if request.is_ajax():
        if request.method == 'POST':
            id_ = request.POST.get('id')
            id = id_.split('_')[1]
            item = Card()
            item.name = str(timezone.now())
            item.save()
    return HttpResponse(status=204)
