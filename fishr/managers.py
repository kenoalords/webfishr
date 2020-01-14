from django.db import models

class BlogPublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_public=True)
