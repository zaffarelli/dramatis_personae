'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
import json
from django.shortcuts import _get_queryset
from django.http import HttpResponse
from scenarist.exceptions.custom import JsonNotFound

# replacement for django.shortcuts.get_object_or_404()
# allows json to be returned with a 404 error
def get_object_or_json404(klass, *args, **kwargs):
  print("get_object_or_json404")
  queryset = _get_queryset(klass)
  print(queryset)
  try:
    return queryset.get(*args, **kwargs)
  except queryset.model.DoesNotExist:
    raise JsonNotFound()


def render_to_json_response(context, **response_kwargs):
  # returns a JSON response, transforming 'context' to make the payload
  print("render_to_json_response")
  print(context)
  new_context = context.copy()
  new_context['object'] = context['object'].to_json()
  response_kwargs['content_type'] = 'application/json'
  return HttpResponse(convert_context_to_json(new_context), **response_kwargs)


def convert_context_to_json(context):
  # convert the context dictionary into a JSON object
  # note: this is *EXTREMELY* naive; in reality, you'll need
  # to do much more complex handling to ensure that arbitrary
  # objects -- such as Django model instances or querysets
  # -- can be serialized as JSON.
  #print("convert_context_to_json")
  #new_context = {}
  #print(context)
  #for key,item in context:
  #  try:
  #    json_item = item.to_json()
  #    new_context[key] = json_item
  #  except:
  #    new_context[key] = item 
  #print(new_context)
  return context
  #return json.dumps(context)
  
