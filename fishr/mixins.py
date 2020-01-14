from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from .models import Blog
from django.core.exceptions import PermissionDenied

class SuperUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        else:
            return super().dispatch(request, *args, **kwargs)

class BlogPublicMixin:
    def dispatch(self, request, *args, **kwargs):
        blog = Blog.objects.get(pk=kwargs['pk'])
        if blog.is_public == False:
            raise PermissionDenied
        else:
            return super().dispatch(request, *args, **kwargs)
