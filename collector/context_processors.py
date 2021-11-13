"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from collector.utils import fics_references, fs_fics7
from collector.models.profile import Profile
from django.conf import settings
from collector.utils.basic import get_current_config
import sys
import socket


def users(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
    else:
        user_profile = None
    return dict(current_user=request.user, user_profile=user_profile)


def commons(request):
    try:
        from collector.models.campaign import Campaign
        configs = Campaign.objects.all()
    except:
        configs = []
    campaign = get_current_config(request)
    return dict(dp_version=fics_references.RELEASE, instance_name=settings.INSTANCE_NAME,
            python_version=sys.version, hostname=socket.gethostname().upper(), campaign=campaign, configs=configs, ghostmark='ghostmark')
