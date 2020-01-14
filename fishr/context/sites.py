from django.contrib.sites.models import Site
from django.conf import settings

def current_site(request):
    current_site = Site.objects.get_current()
    return { 'site': current_site }

def is_debug(request):
    return { 'is_debug': settings.DEBUG }
