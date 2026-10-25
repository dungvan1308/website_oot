from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from website_oot.core.forms import ContactRequestForm
from website_oot.core.localization import localized_content
from website_oot.core.models import Article, CaseStudy, Industry, Product, Service, Solution, Statistic, Technology


def _lines(value):
    return [line.strip() for line in value.splitlines() if line.strip()]


def _localized_items(queryset, language):
    return [(item, localized_content(item, language)) for item in queryset]


def _catalog_context(language):
    services = _localized_items(
        Service.objects.filter(is_published=True).prefetch_related("translations").order_by("display_order", "title"), language
    )
    solutions = _localized_items(
        Solution.objects.filter(is_published=True).prefetch_related("translations").order_by("display_order", "title"), language
    )
    products = Product.objects.filter(is_published=True).prefetch_related("technologies", "translations").order_by("display_order", "title")
    industries = Industry.objects.filter(is_published=True).prefetch_related("solutions__translations", "translations").order_by("display_order", "title")
    return {
        "services": [
            {
                "title": text.title,
                "description": text.summary or text.description,
                "mark": "◈",
                "href": f"{reverse('services')}#{item.slug}",
                "image": item.image.url if item.image else "",
                "image_alt": item.image_alt,
            }
            for item, text in services
        ],
        "service_groups": [
            {
                "id": item.slug,
                "title": text.title,
                "description": text.summary or text.description,
                "mark": "◈",
                "features": _lines(text.capabilities),
                "outcome": text.business_value,
                "image": item.image.url if item.image else "",
                "image_alt": item.image_alt,
            }
            for item, text in services
        ],
        "solutions": [
            {
                "slug": item.slug,
                "title": text.title,
                "description": text.summary or text.description,
                "capabilities": _lines(text.capabilities),
                "value": text.business_value,
                "index": f"{index:02d}",
                "href": f"{reverse('solutions')}#{item.slug}",
                "image": item.image.url if item.image else "",
                "image_alt": item.image_alt,
            }
            for index, (item, text) in enumerate(solutions, start=1)
        ],
        "products": [
            {
                "slug": item.slug,
                "title": text.title,
                "description": text.summary or text.description,
                "technology": " · ".join(technology.title for technology in item.technologies.all()),
                "features": _lines(text.features),
                "value": text.business_value,
                "mark": "◈",
                "href": f"{reverse('products')}#{item.slug}",
                "image": item.image.url if item.image else "",
                "image_alt": item.image_alt,
            }
            for item, text in _localized_items(products, language)
        ],
        "industries": [
            {
                "slug": item.slug,
                "title": text.title,
                "description": text.summary or text.description,
                "index": f"{index:02d}",
                "focus": _lines(text.focus_areas),
                "solutions": [localized_content(solution, language).title for solution in item.solutions.all()],
                "image": item.image.url if item.image else "",
                "image_alt": item.image_alt,
            }
            for index, (item, text) in enumerate(_localized_items(industries, language), start=1)
        ],
        "technologies": list(
            Technology.objects.filter(is_published=True).order_by("display_order", "title").values_list("title", flat=True)
        ),
    }


def _case_study_data(queryset, language):
    results = []
    for item in queryset.prefetch_related("technologies", "translations"):
        text = localized_content(item, language)
        results.append(
            {
                "id": item.slug,
                "category": text.category,
                "title": text.title,
                "summary": text.summary,
                "challenge": text.challenge,
                "solution": text.solution,
                "architecture": _lines(text.architecture),
                "technology": [technology.title for technology in item.technologies.all()],
                "implementation": _lines(text.implementation),
                "impact": _lines(text.business_impact),
                "is_illustrative": item.is_illustrative,
                "href": f"{reverse('case-studies')}#{item.slug}",
                "image": item.image.url if item.image else "",
                "image_alt": item.image_alt,
            }
        )
    return results


def _article_data(queryset, language):
    return [
        {
            "id": item.slug,
            "category": text.category,
            "title": text.title,
            "summary": text.summary,
            "reading_time": text.reading_time,
            "content": text.content,
            "href": f"{reverse('insights')}#{item.slug}",
            "image": item.image.url if item.image else "",
            "image_alt": item.image_alt,
        }
        for item, text in _localized_items(queryset.prefetch_related("translations"), language)
    ]


def home(request):
    language = request.LANGUAGE_CODE
    context = {
        **_catalog_context(language),
        "delivery_patterns": _case_study_data(
            CaseStudy.objects.filter(is_published=True, is_featured=True).order_by("display_order", "title"), language
        ),
        "insights": _article_data(
            Article.objects.filter(is_published=True, is_featured=True).order_by("display_order", "title"), language
        ),
        "capability_stats": list(
            Statistic.objects.filter(is_published=True).order_by("display_order").values("value", "label")
        ),
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html", _catalog_context(request.LANGUAGE_CODE))


def services(request):
    return render(request, "pages/services.html", _catalog_context(request.LANGUAGE_CODE))


def solutions(request):
    return render(request, "pages/solutions.html", _catalog_context(request.LANGUAGE_CODE))


def products(request):
    return render(request, "pages/products.html", _catalog_context(request.LANGUAGE_CODE))


def industries(request):
    return render(request, "pages/industries.html", _catalog_context(request.LANGUAGE_CODE))


def case_studies(request):
    queryset = CaseStudy.objects.filter(is_published=True).prefetch_related("translations").order_by("display_order", "title")
    return render(request, "pages/case_studies.html", {"case_studies": _case_study_data(queryset, request.LANGUAGE_CODE)})


def insights(request):
    queryset = Article.objects.filter(is_published=True).prefetch_related("translations").order_by("display_order", "title")
    return render(request, "pages/insights.html", {"insights": _article_data(queryset, request.LANGUAGE_CODE)})


def contact(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thanks for getting in touch. Your enquiry has been received."))
            return redirect("contact")
    else:
        form = ContactRequestForm()
    return render(request, "pages/contact.html", {"form": form})


def robots(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    content = f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {sitemap_url}\n"
    return HttpResponse(content, content_type="text/plain; charset=utf-8")
