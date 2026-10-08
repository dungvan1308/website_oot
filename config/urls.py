from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

from core.sitemaps import PublicPagesSitemap
from core.views import robots

sitemaps = {"pages": PublicPagesSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots, name="robots"),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(path("", include("core.urls")), prefix_default_language=True)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
