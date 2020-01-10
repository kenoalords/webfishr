from fishr.models import Testimonial

def all(request):
    t = Testimonial.objects.all()
    if t:
        return { 'testimonials': t }
    else:
        return {}
