from django.http import JsonResponse

class AjaxFromResponseMixin:

  def form_valid(self, form):
    response = super().form_valid(form)
    if self.request.is_ajax():
      data = {
        'pk': self.object.pk,        
      }
      return JsonResponse(data)
    else:
      return response

  def form_invalid(self, form):
    response = super().form_invalid(form)
    if self.request.is_ajax():
      return JsonResponse(form.errors, status=400)
    else:
      return response
