from django.core.management.base import BaseCommand

from website_oot.core.models import (
    Article,
    ArticleTranslation,
    CaseStudy,
    CaseStudyTranslation,
    CompanyProfile,
    CompanyProfileTranslation,
    Industry,
    IndustryTranslation,
    Product,
    ProductTranslation,
    Service,
    ServiceTranslation,
    SiteSettings,
    SiteSettingsTranslation,
    Solution,
    SolutionTranslation,
)
from website_oot.core.vietnamese_content import VI_CONTENT, VI_EXTRA


class Command(BaseCommand):
    help = "Add reviewed Vietnamese translations to seeded CMS content without replacing editor changes."

    def handle(self, *args, **options):
        self._seed_publishable(Service, ServiceTranslation, "services", ("category", "capabilities", "business_value"))
        self._seed_publishable(Solution, SolutionTranslation, "solutions", ("capabilities", "business_value"))
        self._seed_publishable(Product, ProductTranslation, "products", ("features", "business_value"))
        self._seed_publishable(Industry, IndustryTranslation, "industries", ("focus_areas",))
        self._seed_publishable(CaseStudy, CaseStudyTranslation, "case-studies", ("category", "challenge", "solution", "architecture", "implementation", "business_impact"))
        self._seed_publishable(Article, ArticleTranslation, "articles", ("category", "content", "reading_time"))
        self._seed_company_profile()
        self._seed_site_settings()
        self.stdout.write(self.style.SUCCESS("Vietnamese translation seed is ready for review in Django Admin."))

    @staticmethod
    def _seed_publishable(parent_model, translation_model, key, extra_fields):
        entries = VI_CONTENT[key]
        extra_entries = VI_EXTRA.get(key, {})
        relation_name = {
            "CaseStudy": "case_study",
        }.get(parent_model.__name__, parent_model._meta.model_name)
        for parent in parent_model.objects.all():
            english = {field: getattr(parent, field, "") for field in ("title", "summary", "description", *extra_fields)}
            translation_model.objects.get_or_create(
                **{relation_name: parent, "language": "en"},
                defaults={**english, "status": "published" if parent.is_published else "draft"},
            )
            translated = entries.get(parent.slug)
            if not translated:
                continue
            title, summary, *description = translated
            extras = extra_entries.get(parent.slug, {})
            values = {
                "title": title,
                "summary": summary,
                "description": description[0] if description else summary,
                "status": "published" if parent.is_published else "draft",
                **extras,
            }
            translation, created = translation_model.objects.get_or_create(
                **{relation_name: parent, "language": "vi"}, defaults=values
            )
            if not created:
                changed = False
                for field, value in values.items():
                    if field == "status":
                        continue
                    current = getattr(translation, field, "")
                    base_value = getattr(parent, field, None)
                    if value and (not current or current == base_value):
                        setattr(translation, field, value)
                        changed = True
                if changed:
                    translation.save()

    @staticmethod
    def _seed_company_profile():
        profile = CompanyProfile.objects.first()
        if not profile:
            return
        english = {
            "title": profile.name,
            "name": profile.name,
            "summary": profile.tagline,
            "tagline": profile.tagline,
            "description": profile.introduction,
            "homepage_intro_heading": profile.homepage_intro_heading,
            "mission": profile.mission,
            "vision": profile.vision,
            "status": "published",
        }
        CompanyProfileTranslation.objects.get_or_create(company_profile=profile, language="en", defaults=english)
        CompanyProfileTranslation.objects.get_or_create(
            company_profile=profile,
            language="vi",
            defaults={
                "title": profile.name,
                "name": profile.name,
                "summary": "Giải pháp Công nghệ & Chuyển đổi Số",
                "tagline": "Giải pháp Công nghệ & Chuyển đổi Số",
                "description": "Kết nối dữ liệu, hệ thống và đội ngũ quanh những kết quả doanh nghiệp cần đạt được.",
                "homepage_intro_heading": "Đưa dữ liệu phát huy giá trị trên toàn doanh nghiệp.",
                "mission": "Kết nối dữ liệu, hệ thống và đội ngũ để thúc đẩy chuyển đổi doanh nghiệp bền vững.",
                "vision": "Trở thành đối tác công nghệ tin cậy cho các tổ chức đang xây dựng tương lai số.",
                "status": "published",
            },
        )

    @staticmethod
    def _seed_site_settings():
        site = SiteSettings.objects.filter(pk=1).first()
        if not site:
            return
        english = {
            "title": site.site_name,
            "site_name": site.site_name,
            "summary": site.tagline,
            "tagline": site.tagline,
            "description": site.hero_description,
            "default_meta_description": site.default_meta_description,
            "hero_eyebrow": site.hero_eyebrow,
            "hero_title": site.hero_title,
            "hero_description": site.hero_description,
            "hero_primary_label": site.hero_primary_label,
            "hero_primary_url": site.hero_primary_url,
            "hero_secondary_label": site.hero_secondary_label,
            "hero_secondary_url": site.hero_secondary_url,
            "status": "published",
        }
        SiteSettingsTranslation.objects.get_or_create(site_settings=site, language="en", defaults=english)
        SiteSettingsTranslation.objects.get_or_create(
            site_settings=site,
            language="vi",
            defaults={
                "title": site.site_name,
                "site_name": site.site_name,
                "summary": "Giải pháp Công nghệ & Chuyển đổi Số",
                "tagline": "Giải pháp Công nghệ & Chuyển đổi Số",
                "description": "Chúng tôi hiện đại hóa dữ liệu, ứng dụng và hạ tầng để hỗ trợ quyết định tốt hơn.",
                "default_meta_description": "Ocean One Technology cung cấp nền tảng dữ liệu, công nghệ doanh nghiệp và giải pháp chuyển đổi số.",
                "hero_eyebrow": "Giải pháp Công nghệ & Chuyển đổi Số",
                "hero_title": "Kiến tạo dữ liệu. Thúc đẩy chuyển đổi doanh nghiệp.",
                "hero_description": "Chúng tôi hiện đại hóa dữ liệu, ứng dụng và hạ tầng, xây dựng nền tảng kết nối cho quyết định tốt hơn.",
                "hero_primary_label": "Khám phá giải pháp",
                "hero_primary_url": "/vi/solutions/",
                "hero_secondary_label": "Trao đổi với chuyên gia",
                "hero_secondary_url": "/vi/contact/",
                "status": "published",
            },
        )
