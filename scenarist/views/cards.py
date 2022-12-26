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

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        cardlinks_formset = context['cardlinks']
        if cardlinks_formset.is_valid():
            response = super().form_valid(form)
            cardlinks_formset.instance = self.object
            cardlinks_formset.save()
            return response
        else:
            messages.error(self.request, 'Card %s has errors. Unable to save.' % (context['c'].name))
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CardUpdateView, self).get_context_data(**kwargs)
        context["object"] = self.object
        if self.request.POST:
            context['form'] = CardForm(self.request.POST, instance=self.object)
            context['cardlinks'] = CardLinkFormSet(self.request.POST, instance=self.object)
            context['cardlinks'].full_clean()
            messages.success(self.request, 'Card updated: %s' % (context['form']['name'].value()))
        else:
            context['form'] = CardForm(instance=self.object)
            context['cardlinks'] = CardLinkFormSet(instance=self.object)
            messages.info(self.request, 'Card displayed: %s' % (context['form']['name'].value()))
        return context


class CardDeleteView(DeleteView):
    model = Card


@csrf_exempt
def add_card(request):
    if is_ajax(request):
        if request.method == 'POST':
            id_ = request.POST.get('id')
            id = id_.split('_')[1]
            item = Card()
            item.name = str(timezone.now())
            item.save()
    return HttpResponse(status=204)
