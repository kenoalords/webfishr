from fishr.models import Package

def web_design(request):
    return { 'packages': Package.objects.filter(category__title='Web Design') }
