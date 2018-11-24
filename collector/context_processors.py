from collector.utils import fs_fics7

def commons(request):
    return { 'dp_version': fs_fics7.RELEASE }
