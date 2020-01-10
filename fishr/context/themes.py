from fishr.models import Theme

def all(request):
    return { 'themes': Theme.objects.all() }
