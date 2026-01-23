from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse_lazy, reverse

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Post.objects.filter(is_private=False, is_banned=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse_lazy("posts:post_detail", kwargs={"slug": obj.slug})
