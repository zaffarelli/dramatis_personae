from collector.utils import fics_references, fs_fics7
from django.conf import settings

def commons(request):
    return { 'dp_version': fics_references.RELEASE, 'instance_name': settings.INSTANCE_NAME, 'config_keywords': fs_fics7.get_keywords()}
