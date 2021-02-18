from django.contrib.gis.geoip2 import GeoIP2

class IPLocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        g = GeoIP2()
        try:
            # city = g.city('178.128.180.19') # US IP
            city = g.city(request.META['REMOTE_ADDR'])
            request.location = city['country_code']
        except Exception as e:
            request.location = 'US'
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
