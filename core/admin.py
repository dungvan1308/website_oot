from django.contrib import admin
from core.models import (
    Article,
    CaseStudy,
    CaseStudyTranslation,
    CompanyProfile,
    CompanyProfileTranslation,
    ContactRequest,
    Industry,
    IndustryTranslation,
    Partner,
    Product,
    ProductTranslation,
    SEOSetting,
    Service,
    ServiceTranslation,
    SiteSettings,
    SiteSettingsTranslation,
    Solution,
    SolutionTranslation,
    Statistic,
    Technology,
    ArticleTranslation,
)

admin.site.site_header = "Ocean One Technology CMS Administration"
admin.site.site_title = "Ocean One Technology CMS"
admin.site.index_title = "Manage website content"


class LanguageTranslationInline(admin.StackedInline):
    extra = 0
    max_num = 2
    ordering = ("language",)
    fieldsets = (
        ("Language and status", {"fields": ("language", "status")}),
        ("Translated content", {"fields": ("title", "summary", "description")} ),
        ("Language-specific SEO", {"fields": ("seo_title", "seo_description"), "classes": ("collapse",)}),
    )


class ServiceTranslationInline(LanguageTranslationInline):
    model = ServiceTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Service details", {"fields": ("category", "capabilities", "business_value")} ),)


class SolutionTranslationInline(LanguageTranslationInline):
    model = SolutionTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Solution details", {"fields": ("capabilities", "business_value")} ),)


class ProductTranslationInline(LanguageTranslationInline):
    model = ProductTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Product details", {"fields": ("features", "business_value")} ),)


class IndustryTranslationInline(LanguageTranslationInline):
    model = IndustryTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Industry details", {"fields": ("focus_areas",)}),)


class CaseStudyTranslationInline(LanguageTranslationInline):
    model = CaseStudyTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Case study details", {"fields": ("category", "challenge", "solution", "architecture", "implementation", "business_impact")} ),)


class ArticleTranslationInline(LanguageTranslationInline):
    model = ArticleTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Article details", {"fields": ("category", "content", "reading_time")} ),)


class CompanyProfileTranslationInline(LanguageTranslationInline):
    model = CompanyProfileTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (("Company details", {"fields": ("name", "tagline", "homepage_intro_heading", "mission", "vision")} ),)


class SiteSettingsTranslationInline(LanguageTranslationInline):
    model = SiteSettingsTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (
        (
            "Homepage settings",
            {
                "fields": (
                    "site_name",
                    "tagline",
                    "default_meta_description",
                    "hero_eyebrow",
                    "hero_title",
                    "hero_description",
                    ("hero_primary_label", "hero_primary_url"),
                    ("hero_secondary_label", "hero_secondary_url"),
                )
            },
        ),
    )


class TranslationLanguageFilter(admin.SimpleListFilter):
    title = "translation language"
    parameter_name = "translation_language"

    def lookups(self, request, model_admin):
        return (("vi", "Vietnamese"), ("en", "English"), ("missing", "Missing translation"))

    def queryset(self, request, queryset):
        if self.value() in ("vi", "en"):
            return queryset.filter(translations__language=self.value()).distinct()
        if self.value() == "missing":
            return queryset.exclude(translations__language__in=("vi", "en")).distinct()
        return queryset


class TranslationPublicationFilter(admin.SimpleListFilter):
    title = "translation status"
    parameter_name = "translation_status"

    def lookups(self, request, model_admin):
        return (("published", "Published"), ("draft", "Draft"))

    def queryset(self, request, queryset):
        return queryset.filter(translations__status=self.value()).distinct() if self.value() else queryset


class PublishableContentAdmin(admin.ModelAdmin):
    has_translations = True
    list_display = ("title", "vi_translation_status", "en_translation_status", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = ("is_published", "is_featured", TranslationLanguageFilter, TranslationPublicationFilter, "updated_at")
    list_editable = ("is_published", "is_featured", "display_order")
    search_fields = ("title", "slug", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("display_order", "title")
    date_hierarchy = "created_at"
    list_per_page = 30
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "description")}),
        ("Publishing", {"fields": ("is_published", "is_featured", "display_order")}),
        ("Image", {"fields": ("image", "image_alt"), "classes": ("collapse",)}),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("translations") if self.has_translations else queryset

    @admin.display(description="VI")
    def vi_translation_status(self, obj):
        return self._translation_status(obj, "vi")

    @admin.display(description="EN")
    def en_translation_status(self, obj):
        return self._translation_status(obj, "en")

    @staticmethod
    def _translation_status(obj, language):
        if not hasattr(obj, "translations"):
            return "—"
        translation = next((item for item in obj.translations.all() if item.language == language), None)
        if translation is None:
            return "⚠ Missing"
        return "✓ Published" if translation.status == "published" else "Draft"


@admin.register(Service)
class ServiceAdmin(PublishableContentAdmin):
    inlines = (ServiceTranslationInline,)
    list_display = ("title", "category", "vi_translation_status", "en_translation_status", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = (*PublishableContentAdmin.list_filter, "category")
    search_fields = (*PublishableContentAdmin.search_fields, "capabilities", "business_value")
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Service details", {"fields": ("category", "capabilities", "business_value")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Solution)
class SolutionAdmin(PublishableContentAdmin):
    inlines = (SolutionTranslationInline,)
    search_fields = (*PublishableContentAdmin.search_fields, "capabilities", "business_value")
    filter_horizontal = ("services",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Solution details", {"fields": ("capabilities", "business_value", "services")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Product)
class ProductAdmin(PublishableContentAdmin):
    inlines = (ProductTranslationInline,)
    search_fields = (*PublishableContentAdmin.search_fields, "features", "business_value", "technologies__title")
    filter_horizontal = ("technologies",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Product details", {"fields": ("features", "business_value", "technologies")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Industry)
class IndustryAdmin(PublishableContentAdmin):
    inlines = (IndustryTranslationInline,)
    search_fields = (*PublishableContentAdmin.search_fields, "focus_areas", "solutions__title")
    filter_horizontal = ("solutions",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Industry details", {"fields": ("focus_areas", "solutions")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Technology)
class TechnologyAdmin(PublishableContentAdmin):
    has_translations = False
    list_display = ("title", "category", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = ("is_published", "is_featured", "updated_at", "category")
    search_fields = PublishableContentAdmin.search_fields + ("category",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Technology details", {"fields": ("category", "website")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(CaseStudy)
class CaseStudyAdmin(PublishableContentAdmin):
    inlines = (CaseStudyTranslationInline,)
    list_display = ("title", "category", "vi_translation_status", "en_translation_status", "is_illustrative", "is_published", "is_featured", "display_order")
    list_filter = (*PublishableContentAdmin.list_filter, "category", "is_illustrative")
    search_fields = PublishableContentAdmin.search_fields + ("challenge", "solution", "business_impact")
    filter_horizontal = ("technologies",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Case study flow", {"fields": ("category", "is_illustrative", "challenge", "solution", "architecture", "technologies", "implementation", "business_impact")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Article)
class ArticleAdmin(PublishableContentAdmin):
    inlines = (ArticleTranslationInline,)
    list_display = ("title", "category", "vi_translation_status", "en_translation_status", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = (*PublishableContentAdmin.list_filter, "category")
    search_fields = PublishableContentAdmin.search_fields + ("content", "category")
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Article details", {"fields": ("category", "reading_time", "content")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Partner)
class PartnerAdmin(PublishableContentAdmin):
    has_translations = False
    list_display = ("title", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = ("is_published", "is_featured", "updated_at")
    search_fields = PublishableContentAdmin.search_fields + ("relationship_type",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        ("Relationship details", {"fields": ("website", "relationship_type")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "is_published", "display_order", "updated_at")
    list_filter = ("is_published", "updated_at")
    list_editable = ("is_published", "display_order")
    search_fields = ("value", "label")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("display_order", "id")


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    inlines = (CompanyProfileTranslationInline,)
    list_display = ("name", "vi_translation_status", "en_translation_status", "tagline", "updated_at")
    list_filter = (TranslationLanguageFilter, TranslationPublicationFilter, "updated_at")
    search_fields = ("name", "tagline", "introduction")
    readonly_fields = ("updated_at",)
    fieldsets = (
        ("Company", {"fields": ("name", "tagline", "logo")}),
        ("Homepage introduction", {"fields": ("homepage_intro_heading", "introduction")}),
        ("About", {"fields": ("mission", "vision")}),
        ("Dates", {"fields": ("updated_at",)}),
    )

    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists() and super().has_add_permission(request)

    vi_translation_status = PublishableContentAdmin.vi_translation_status
    en_translation_status = PublishableContentAdmin.en_translation_status


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = (SiteSettingsTranslationInline,)
    list_display = ("site_name", "vi_translation_status", "en_translation_status", "contact_email", "updated_at")
    list_filter = (TranslationLanguageFilter, TranslationPublicationFilter, "updated_at")
    readonly_fields = ("updated_at",)
    fieldsets = (
        ("Site identity", {"fields": ("site_name", "tagline", "logo")}),
        ("Homepage hero", {"fields": ("hero_eyebrow", "hero_title", "hero_description", ("hero_primary_label", "hero_primary_url"), ("hero_secondary_label", "hero_secondary_url"))}),
        ("Default SEO", {"fields": ("default_meta_description",)}),
        ("Contact details", {"fields": ("contact_email", "contact_phone", "contact_address")}),
        ("Dates", {"fields": ("updated_at",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists() and super().has_add_permission(request)

    vi_translation_status = PublishableContentAdmin.vi_translation_status
    en_translation_status = PublishableContentAdmin.en_translation_status


@admin.register(SEOSetting)
class SEOSettingAdmin(admin.ModelAdmin):
    list_display = ("path", "language", "title", "allow_indexing", "updated_at")
    list_filter = ("language", "allow_indexing", "updated_at")
    list_editable = ("allow_indexing",)
    search_fields = ("path", "title", "meta_description")
    readonly_fields = ("updated_at",)
    ordering = ("path",)


@admin.action(description="Mark selected enquiries as in progress")
def mark_contact_requests_in_progress(modeladmin, request, queryset):
    queryset.update(status=ContactRequest.Status.IN_PROGRESS)


@admin.action(description="Close selected enquiries")
def close_contact_requests(modeladmin, request, queryset):
    queryset.update(status=ContactRequest.Status.CLOSED)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "interest", "status", "created_at")
    list_filter = ("status", "interest", "created_at")
    search_fields = ("name", "email", "company", "phone", "message")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    actions = (mark_contact_requests_in_progress, close_contact_requests)
    list_per_page = 30
