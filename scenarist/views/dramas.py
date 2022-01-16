"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from scenarist.forms.basic import *
from scenarist.models.dramas import Drama
from django.shortcuts import get_object_or_404
from scenarist.mixins.ajaxfromresponse import AjaxFromResponseMixin
from django.http import HttpResponse, JsonResponse
from django.contrib import messages


class DramaDetailView(DetailView):
    model = Drama

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f'Showing {context["drama"]}')
        return context


class DramaUpdateView(AjaxFromResponseMixin,UpdateView):
    model = Drama
    form_class = DramaForm
    context_object_name = 'object'
    template_name_suffix = '_update_form'


def add_drama(request):
    import datetime
    if request.is_ajax():
        if request.method == 'POST':
            full_id = request.POST.get('id')
            # print(full_id)
            id = int(full_id.split("_")[1])
            item = Drama()
            item.title = datetime.datetime.now()
            item.epic = Epic.objects.get(pk=id)
            item.save()
            c = {}
            c[item] = item
            return JsonResponse(c)
    return HttpResponse(status=204)


class DramaDeleteView(DeleteView):
  model = Drama
