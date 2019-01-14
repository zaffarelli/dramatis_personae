from collector.utils import fics_references
from django.conf import settings

def commons(request):
    return { 'dp_version': fics_references.RELEASE, 'instance_name': settings.INSTANCE_NAME }
