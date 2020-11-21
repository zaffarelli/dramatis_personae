'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from collector.utils import fics_references, fs_fics7
from collector.models.user import Profile
from django.conf import settings
import sys
import socket


def users(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
    else:
        user_profile = None
    return dict(current_user=request.user, user_profile=user_profile)


def commons(request):
    return dict(dp_version=fics_references.RELEASE, instance_name=settings.INSTANCE_NAME,
            python_version=sys.version, hostname=socket.gethostname().upper())
