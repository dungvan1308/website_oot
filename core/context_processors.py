from django.conf import settings
from django.urls import reverse, translate_url

from website_oot.core.localization import localized_content
from website_oot.core.models import CompanyProfile, SEOSetting, SiteSettings


def site_metadata(request):
    """Shared site identity and primary navigation for global templates."""
    language = getattr(request, "LANGUAGE_CODE", settings.LANGUAGE_CODE)
    site_settings = localized_content(
        SiteSettings.objects.filter(pk=1).prefetch_related("translations").first(), language
    )
    company_profile = localized_content(
        CompanyProfile.objects.prefetch_related("translations").first(), language
    )
    seo_setting = SEOSetting.objects.filter(path=request.path, language=language).first()
    language_switcher = [
        {
            "code": code,
            "label": label,
            "url": translate_url(request.get_full_path(), code),
            "active": code == language,
        }
        for code, label in settings.LANGUAGES
    ]
    language_alternates = [
        {
            "code": code,
            "url": request.build_absolute_uri(translate_url(request.path, code)),
        }
        for code, _label in settings.LANGUAGES
    ]
    return {
        "site_name": site_settings.site_name if site_settings else "Ocean One Technology",
        "site_tagline": site_settings.tagline if site_settings else "Enterprise Technology",
        "site_settings": site_settings,
        "company_profile": company_profile,
        "seo_setting": seo_setting,
        "language_switcher": language_switcher,
        "language_alternates": language_alternates,
        "current_language": language,
        "site_urls": {
            "home": reverse("home"),
            "about": reverse("about"),
            "services": reverse("services"),
            "solutions": reverse("solutions"),
            "products": reverse("products"),
            "industries": reverse("industries"),
            "case_studies": reverse("case-studies"),
            "insights": reverse("insights"),
            "contact": reverse("contact"),
        },
        "nav_items": [
            {"label": label, "href": reverse(route)}
            for label, route in (
                ("About", "about"),
                ("Services", "services"),
                ("Solutions", "solutions"),
                ("Products", "products"),
                ("Industries", "industries"),
                ("Case studies", "case-studies"),
                ("Insights", "insights"),
            )
        ],
    }
