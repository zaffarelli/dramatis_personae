'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
'''
from django.http import JsonResponse

from collector.utils.d4_changes import is_ajax


class AjaxFromResponseMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        if is_ajax(self.request):
            data = dict(pk=self.object.pk)
            return JsonResponse(data)
        else:
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if is_ajax(self.request):
            return JsonResponse(form.errors, status=400)
        else:
           return response

