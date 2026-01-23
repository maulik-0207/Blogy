"""
URL configuration for Blogy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2.4/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.posts.sitemaps import PostSitemap
from django.views.generic import TemplateView

sitemaps = {
    "posts": PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('',include('apps.main.urls')),
    path('accounts/',include('apps.accounts.urls')),
    path('',include('apps.accounts.public_urls')),
    path('posts/',include('apps.posts.urls')),
    path('comments/',include('apps.comments.urls')),
    path('post-lists/',include('apps.post_lists.urls')),
    path('notifications/',include('apps.notifications.urls')),
    path('reports/',include('apps.reports.urls')),
    
    
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]

handler400 = "apps.main.views.error_400"
handler403 = "apps.main.views.error_403"
handler404 = "apps.main.views.error_404"
handler500 = "apps.main.views.error_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
