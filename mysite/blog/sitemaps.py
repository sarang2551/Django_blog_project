from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSiteMap(Sitemap):
    # the frequency of changing the post pages
    changefreq = 'weekly'
    # the relevance of the page to the site (maximum is 1)
    priority = 0.9
    # returns the QuerySet of objects included in this sitemap
    def items(self):
        return Post.published.all()
    # returns the last time the object was modified (object being the post)
    def lastmod(self, obj):
        return obj.updated