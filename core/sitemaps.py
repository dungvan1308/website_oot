from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PublicPagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    i18n = True
    alternates = True

    page_names = (
        "home",
        "about",
        "services",
        "solutions",
        "products",
        "industries",
        "case-studies",
        "insights",
        "contact",
    )

    def items(self):
        return self.page_names

    def location(self, item):
        return reverse(item)
