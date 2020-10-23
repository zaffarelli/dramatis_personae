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


def commons(request):
    return dict(dp_version=fics_references.RELEASE, instance_name=settings.INSTANCE_NAME,
            python_version=sys.version, hostname=socket.gethostname().upper())
