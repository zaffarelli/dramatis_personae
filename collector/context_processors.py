from collector.utils import fics_references

def commons(request):
    return { 'dp_version': fics_references.RELEASE }
