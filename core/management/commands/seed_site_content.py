from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.urls import reverse
from django.utils.translation import override
from django.utils.text import slugify

from website_oot.core.editorial import CASE_STUDIES, INSIGHTS
from website_oot.core.homepage import INDUSTRIES, PRODUCTS, SERVICE_GROUPS, SOLUTIONS, TECHNOLOGIES
from website_oot.core.models import (
    Article,
    CaseStudy,
    CompanyProfile,
    Industry,
    Product,
    SEOSetting,
    Service,
    SiteSettings,
    Solution,
    Statistic,
    Technology,
)


SERVICE_CATEGORIES = [
    Service.Category.DATA_PLATFORM,
    Service.Category.BUSINESS_INTELLIGENCE,
    Service.Category.ENTERPRISE_SOFTWARE,
    Service.Category.BANKING_TECHNOLOGY,
    Service.Category.CLOUD_TRANSFORMATION,
]


class Command(BaseCommand):
    help = "Create the initial editable Ocean One Technology CMS content without overwriting existing records."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "Ocean One Technology",
                "tagline": "Enterprise Technology & Data Transformation",
                "default_meta_description": "Enterprise technology, data platforms and digital transformation.",
                "hero_eyebrow": "Enterprise technology & data transformation",
                "hero_title": "Engineering data. Powering enterprise transformation.",
                "hero_description": "We help organizations modernize data, applications and infrastructure—building connected foundations for better decisions and lasting change.",
                "hero_primary_label": "Explore our solutions",
                "hero_primary_url": "/solutions/",
                "hero_secondary_label": "Talk to our experts",
                "hero_secondary_url": "/contact/",
            },
        )
        CompanyProfile.objects.get_or_create(
            pk=1,
            defaults={
                "name": "Ocean One Technology",
                "tagline": "Enterprise Technology & Data Transformation",
                "homepage_intro_heading": "Make your data work across the enterprise.",
                "introduction": "We help organizations connect data, systems and teams around the outcomes that matter.",
            },
        )

        services = {}
        for order, item in enumerate(SERVICE_GROUPS, start=1):
            service, _ = Service.objects.get_or_create(
                slug=item["id"],
                defaults={
                    "title": item["title"],
                    "category": SERVICE_CATEGORIES[order - 1],
                    "summary": item["description"],
                    "description": item["description"],
                    "capabilities": "\n".join(item["features"]),
                    "business_value": item["outcome"],
                    "is_published": True,
                    "is_featured": True,
                    "display_order": order,
                },
            )
            services[service.title] = service

        technologies = {}
        for order, name in enumerate(TECHNOLOGIES, start=1):
            technology, _ = Technology.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    "title": name,
                    "summary": f"Technology ecosystem: {name}",
                    "category": "Technology ecosystem",
                    "is_published": True,
                    "display_order": order,
                },
            )
            technologies[name] = technology

        for item in SOLUTIONS:
            solution, created = Solution.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "summary": item["description"],
                    "description": item["description"],
                    "capabilities": "\n".join(item["capabilities"]),
                    "business_value": item["value"],
                    "is_published": True,
                    "is_featured": True,
                    "display_order": SOLUTIONS.index(item) + 1,
                },
            )
            categories = {
                "enterprise-data-platform": ["data_platform", "business_intelligence"],
                "lakehouse-platform": ["data_platform", "cloud_transformation"],
                "management-bi-platform": ["business_intelligence", "data_platform"],
                "enterprise-management-platform": ["enterprise_software"],
                "banking-data-reporting": ["banking_technology", "data_platform", "business_intelligence"],
                "core-banking-migration": ["banking_technology"],
                "sbv-regulatory-reporting": ["banking_technology", "business_intelligence"],
                "cloud-data-transformation": ["cloud_transformation", "data_platform"],
            }
            if created:
                solution.services.set([service for service in services.values() if service.category in categories[item["slug"]]])

        solution_by_title = {item.title: item for item in Solution.objects.all()}
        for order, item in enumerate(PRODUCTS, start=1):
            product, created = Product.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "summary": item["description"],
                    "description": item["description"],
                    "features": "\n".join(item["features"]),
                    "business_value": item["value"],
                    "is_published": True,
                    "is_featured": True,
                    "display_order": order,
                },
            )
            if created:
                product.technologies.set(
                    [
                        technology
                        for label, technology in technologies.items()
                        if label.casefold() in item["technology"].casefold()
                    ]
                )

        for order, item in enumerate(INDUSTRIES, start=1):
            industry, created = Industry.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "summary": item["description"],
                    "description": item["description"],
                    "focus_areas": "\n".join(item["focus"]),
                    "is_published": True,
                    "is_featured": True,
                    "display_order": order,
                },
            )
            if created:
                industry.solutions.set([solution_by_title[name] for name in item["solutions"] if name in solution_by_title])

        for order, item in enumerate(CASE_STUDIES, start=1):
            case_study, created = CaseStudy.objects.get_or_create(
                slug=item["id"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "summary": item["summary"],
                    "challenge": item["challenge"],
                    "solution": item["solution"],
                    "architecture": "\n".join(item["architecture"]),
                    "implementation": "\n".join(item["implementation"]),
                    "business_impact": "\n".join(item["impact"]),
                    "is_illustrative": True,
                    "is_published": True,
                    "is_featured": True,
                    "display_order": order,
                },
            )
            if created:
                case_study.technologies.set(
                    [technology for name, technology in technologies.items() if name.casefold() in " ".join(item["technology"]).casefold()]
                )

        for order, item in enumerate(INSIGHTS, start=1):
            content = "\n\n".join(f"{heading}\n{paragraph}" for heading, paragraph in item["sections"])
            Article.objects.get_or_create(
                slug=item["id"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "summary": item["summary"],
                    "content": content,
                    "reading_time": item["reading_time"],
                    "is_published": True,
                    "is_featured": True,
                    "display_order": order,
                },
            )

        for order, (value, label) in enumerate(
            [("05", "Connected capability domains"), ("08", "Enterprise solution areas"), ("08", "Product platforms and solutions")],
            start=1,
        ):
            Statistic.objects.get_or_create(
                label=label,
                defaults={"value": value, "is_published": True, "display_order": order},
            )

        seo_pages = {
            "home": ("Enterprise Technology & Data Transformation", "Enterprise technology, data platforms and digital transformation.", "Giải pháp Công nghệ & Chuyển đổi Số", "Nền tảng dữ liệu, công nghệ doanh nghiệp và giải pháp chuyển đổi số."),
            "about": ("About", "Learn about our enterprise technology and data transformation focus.", "Giới thiệu", "Tìm hiểu về Ocean One Technology và năng lực công nghệ doanh nghiệp, chuyển đổi dữ liệu."),
            "services": ("Enterprise Technology Services", "Data platform, BI, enterprise software, banking and cloud services.", "Dịch vụ công nghệ doanh nghiệp", "Dịch vụ nền tảng dữ liệu, BI, phần mềm doanh nghiệp, ngân hàng và điện toán đám mây."),
            "solutions": ("Enterprise Solutions", "Data, management, banking and cloud transformation solutions.", "Giải pháp doanh nghiệp", "Giải pháp dữ liệu, quản trị, ngân hàng và chuyển đổi điện toán đám mây."),
            "products": ("Enterprise Products & Platforms", "Products for enterprise data, reporting, applications and banking technology.", "Sản phẩm và nền tảng doanh nghiệp", "Sản phẩm dữ liệu, báo cáo, ứng dụng và công nghệ ngân hàng."),
            "industries": ("Industries", "Technology and data capabilities shaped for industry needs.", "Ngành", "Năng lực công nghệ và dữ liệu phù hợp với đặc thù từng ngành."),
            "case-studies": ("Case Studies", "Illustrative enterprise architecture and delivery scenarios.", "Nghiên cứu tình huống", "Các kịch bản kiến trúc và triển khai doanh nghiệp mang tính minh họa."),
            "insights": ("Insights", "Perspectives on enterprise data, banking technology and BI.", "Góc nhìn", "Góc nhìn về dữ liệu doanh nghiệp, công nghệ ngân hàng và BI."),
            "contact": ("Contact", "Start a conversation about your enterprise technology priorities.", "Liên hệ", "Trao đổi về các ưu tiên công nghệ doanh nghiệp của bạn."),
        }
        for route_name, (title_en, description_en, title_vi, description_vi) in seo_pages.items():
            for language, title, description in (
                ("en", title_en, description_en),
                ("vi", title_vi, description_vi),
            ):
                with override(language):
                    path = reverse(route_name)
                SEOSetting.objects.get_or_create(
                    path=path,
                    language=language,
                    defaults={"title": title, "meta_description": description},
                )

        call_command("seed_vietnamese_translations", verbosity=0)

        self.stdout.write(self.style.SUCCESS("Initial site content is ready for editing in Django Admin."))
