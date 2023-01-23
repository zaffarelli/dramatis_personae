"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_exempt
from extra_views import UpdateWithInlinesView, InlineFormSetFactory

from collector.utils.d4_changes import is_ajax
from scenarist.forms.basic import *
from scenarist.models.cards import Card
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone


class CardDetailView(DetailView):
    model = Card
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cardlinks'] = CardLinkFormSet(instance=self.object)
        context['data'] = self.object.to_json
        messages.success(self.request, 'Displaying card [%s].' % (context['object'].name))
        return context


class CardLinkInline(InlineFormSetFactory):
    model = CardLink
    form_class = CardLinkForm
    factory_kwargs = {'fk_name': 'cardin', 'extra': 2}


class CardUpdateView(AjaxFromResponseMixin, UpdateWithInlinesView):
    model = Card
    form_class = CardForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'
    inlines = [CardLinkInline]


    # def forms_invalid(self, form, inlines):
    #     for formset in inlines:
    #         for errors in formset.errors:
    #             for _, error in errors.items():
    #                 print(error[0])
    #     return self.render_to_response(
    #         self.get_context_data(request=self.request, form=form, inlines=inlines))

    # success_url = 'view_card'
    #
    # def form_valid(self, form):
    #     context = self.get_context_data(form=form)
    #     cardlinks_formset = context['cardlinks']
    #     print(context)
    #     if cardlinks_formset.is_valid():
    #         response = super().form_valid(form)
    #         cardlinks_formset.instance = self.object
    #         cardlinks_formset.save()
    #         return response
    #     else:
    #         messages.error(self.request, 'Card [%s] has errors. Unable to save.' % (context['object'].name))
    #         return super().form_invalid(form)
    #
    # def get_context_data(self, **kwargs):
    #     context = super(CardUpdateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['form'] = CardForm(self.request.POST, instance=self.object)
    #         context['cardlinks'] = CardLinkFormSet(self.request.POST, instance=self.object)
    #         context['cardlinks'].full_clean()
    #         messages.success(self.request, 'Card updated (gcd): %s' % (context['form']['name'].value()))
    #     else:
    #         context['form'] = CardForm(instance=self.object)
    #         context['cardlinks'] = CardLinkFormSet(instance=self.object)
    #         messages.info(self.request, 'Card edited: %s' % (context['form']['name'].value()))
    #     return context


class CardDeleteView(DeleteView):
    model = Card


@csrf_exempt
def add_card(request):
    if is_ajax(request):
        if request.method == 'POST':
            id_ = request.POST.get('id')
            id = id_.split('_')[2]
            item = Card()
            item.parent = Card.objects.get(pk=id)
            item.card_type = "SH"
            item.name = str(timezone.now())
            item.save()
    return HttpResponse(status=204)
