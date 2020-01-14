from django.shortcuts import reverse
from django.contrib.sitemaps import Sitemap

from fishr.models import Blog, Package, Theme

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return Blog.public.all()

    def lastmod(self, obj):
        return obj.updated_at

class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ['index', 'themes', 'about', 'career', 'contact', 'policy', 'how-it-works', 'faq', 'pricing', 'blogs']

    def location(self, item):
        return reverse(item)
