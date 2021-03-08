"""
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴
"""
from collector.utils.basic import get_current_config, export_epic
from django.http import HttpResponse


def build_config_pdf(request):
  campaign = get_current_config()
  _ = export_epic(request,campaign)
  return HttpResponse(status=204)
