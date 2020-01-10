from django.contrib.sites.models import Site

def current_site(request):
    current_site = Site.objects.get_current()
    return { 'site': current_site }
