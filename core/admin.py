from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import Case, IntegerField, Q, Value, When
from django.utils.translation import get_language, gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget
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

admin.site.site_header = _("Ocean One Technology CMS Administration")
admin.site.site_title = _("Ocean One Technology CMS")
admin.site.index_title = _("Manage website content")


def get_translation_for_language(obj):
    """Return this record's translation for the language selected in admin."""
    translations = getattr(obj, "translations", None)
    if translations is None:
        return None
    language = get_language() or "en"
    return next((item for item in translations.all() if item.language == language), None)


def localized_value(obj, field_name):
    translation = get_translation_for_language(obj)
    translated_value = getattr(translation, field_name, "") if translation else ""
    return translated_value or getattr(obj, field_name, "")


RICH_TEXT_EXCLUDED_FIELDS = {
    # These fields are rendered as individual list items by the public site.
    "capabilities",
    "features",
    "focus_areas",
    "architecture",
    "implementation",
    "business_impact",
    # This is customer-submitted plain text, not CMS-authored content.
    "message",
}


class RichTextAdminMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if (
            isinstance(db_field, models.TextField)
            and db_field.name not in RICH_TEXT_EXCLUDED_FIELDS
        ):
            kwargs["widget"] = CKEditor5Widget(config_name="default")
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class LanguageTranslationInline(RichTextAdminMixin, admin.StackedInline):
    extra = 0
    max_num = 2
    ordering = ("language",)
    fieldsets = (
        (_("Language and status"), {"fields": ("language", "status")}),
        (_("Translated content"), {"fields": ("title", "summary", "description")} ),
        (_("Language-specific SEO"), {"fields": ("seo_title", "seo_description"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        language = get_language() or "en"
        return super().get_queryset(request).order_by(
            Case(
                When(language=language, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
            "language",
        )


class ServiceTranslationInline(LanguageTranslationInline):
    model = ServiceTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Service details"), {"fields": ("category", "capabilities", "business_value")} ),)


class SolutionTranslationInline(LanguageTranslationInline):
    model = SolutionTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Solution details"), {"fields": ("capabilities", "business_value")} ),)


class ProductTranslationInline(LanguageTranslationInline):
    model = ProductTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Product details"), {"fields": ("features", "business_value")} ),)


class IndustryTranslationInline(LanguageTranslationInline):
    model = IndustryTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Industry details"), {"fields": ("focus_areas",)}),)


class CaseStudyTranslationInline(LanguageTranslationInline):
    model = CaseStudyTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Case study details"), {"fields": ("category", "challenge", "solution", "architecture", "implementation", "business_impact")} ),)


class ArticleTranslationInline(LanguageTranslationInline):
    model = ArticleTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Article details"), {"fields": ("category", "content", "reading_time")} ),)


class CompanyProfileTranslationInline(LanguageTranslationInline):
    model = CompanyProfileTranslation
    fieldsets = LanguageTranslationInline.fieldsets + ((_("Company details"), {"fields": ("name", "tagline", "homepage_intro_heading", "mission", "vision")} ),)


class SiteSettingsTranslationInline(LanguageTranslationInline):
    model = SiteSettingsTranslation
    fieldsets = LanguageTranslationInline.fieldsets + (
        (
            _("Homepage settings"),
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
    title = _("Translation language")
    parameter_name = "translation_language"

    def lookups(self, request, model_admin):
        return (("vi", _("Vietnamese")), ("en", _("English")), ("missing", _("Missing translation")))

    def queryset(self, request, queryset):
        if self.value() in ("vi", "en"):
            return queryset.filter(translations__language=self.value()).distinct()
        if self.value() == "missing":
            return queryset.exclude(translations__language__in=("vi", "en")).distinct()
        return queryset


class TranslationPublicationFilter(admin.SimpleListFilter):
    title = _("Translation status")
    parameter_name = "translation_status"

    def lookups(self, request, model_admin):
        return (("published", _("Published")), ("draft", _("Draft")))

    def queryset(self, request, queryset):
        return queryset.filter(translations__status=self.value()).distinct() if self.value() else queryset


class LocalizedCategoryFilter(admin.SimpleListFilter):
    title = _("Category")
    parameter_name = "category"

    def lookups(self, request, model_admin):
        values = {
            model_admin.get_localized_category(obj)
            for obj in model_admin.get_queryset(request)
        }
        return tuple((value, value) for value in sorted(values, key=str.casefold) if value)

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        language = get_language() or "en"
        model = queryset.model
        localized_ids = model._default_manager.filter(
            translations__language=language,
            translations__category=self.value(),
        ).values("pk")
        translated_ids = model._default_manager.filter(
            translations__language=language,
        ).exclude(translations__category="").values("pk")
        fallback_ids = model._default_manager.filter(category=self.value()).exclude(
            pk__in=translated_ids
        ).values("pk")
        return queryset.filter(Q(pk__in=localized_ids) | Q(pk__in=fallback_ids)).distinct()


class PublishableContentAdmin(RichTextAdminMixin, admin.ModelAdmin):
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
        (_("Publishing"), {"fields": ("is_published", "is_featured", "display_order")}),
        (_("Image"), {"fields": ("image", "image_alt"), "classes": ("collapse",)}),
        (_("Dates"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("translations") if self.has_translations else queryset

    def get_list_display(self, request):
        display = super().get_list_display(request)
        return tuple(
            "localized_title" if name == "title" else
            "localized_category" if name == "category" else name
            for name in display
        )

    @admin.display(description=_("Title"), ordering="title")
    def localized_title(self, obj):
        return localized_value(obj, "title")

    def get_localized_category(self, obj):
        translation = get_translation_for_language(obj)
        translated = getattr(translation, "category", "") if translation else ""
        if translated:
            return translated
        get_display = getattr(obj, "get_category_display", None)
        return get_display() if get_display else getattr(obj, "category", "")

    @admin.display(description=_("Category"), ordering="category")
    def localized_category(self, obj):
        return self.get_localized_category(obj)

    @admin.display(description=_("VI"))
    def vi_translation_status(self, obj):
        return PublishableContentAdmin._translation_status(obj, "vi")

    @admin.display(description=_("EN"))
    def en_translation_status(self, obj):
        return PublishableContentAdmin._translation_status(obj, "en")

    @staticmethod
    def _translation_status(obj, language):
        if not hasattr(obj, "translations"):
            return "—"
        translation = next((item for item in obj.translations.all() if item.language == language), None)
        if translation is None:
            return _("Missing")
        return f"✓ {_('Published')}" if translation.status == "published" else _("Draft")


@admin.register(Service)
class ServiceAdmin(PublishableContentAdmin):
    inlines = (ServiceTranslationInline,)
    list_display = ("title", "category", "vi_translation_status", "en_translation_status", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = (*PublishableContentAdmin.list_filter, "category")
    search_fields = (*PublishableContentAdmin.search_fields, "capabilities", "business_value")
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Service details"), {"fields": ("category", "capabilities", "business_value")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Solution)
class SolutionAdmin(PublishableContentAdmin):
    inlines = (SolutionTranslationInline,)
    search_fields = (*PublishableContentAdmin.search_fields, "capabilities", "business_value")
    filter_horizontal = ("services",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Solution details"), {"fields": ("capabilities", "business_value", "services")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Product)
class ProductAdmin(PublishableContentAdmin):
    inlines = (ProductTranslationInline,)
    search_fields = (*PublishableContentAdmin.search_fields, "features", "business_value", "technologies__title")
    filter_horizontal = ("technologies",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Product details"), {"fields": ("features", "business_value", "technologies")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Industry)
class IndustryAdmin(PublishableContentAdmin):
    inlines = (IndustryTranslationInline,)
    search_fields = (*PublishableContentAdmin.search_fields, "focus_areas", "solutions__title")
    filter_horizontal = ("solutions",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Industry details"), {"fields": ("focus_areas", "solutions")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Technology)
class TechnologyAdmin(PublishableContentAdmin):
    has_translations = False
    list_display = ("title", "category", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = ("is_published", "is_featured", "updated_at", "category")
    search_fields = PublishableContentAdmin.search_fields + ("category",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Technology details"), {"fields": ("category", "website")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(CaseStudy)
class CaseStudyAdmin(PublishableContentAdmin):
    inlines = (CaseStudyTranslationInline,)
    list_display = ("title", "category", "vi_translation_status", "en_translation_status", "is_illustrative", "is_published", "is_featured", "display_order")
    list_filter = (*PublishableContentAdmin.list_filter, LocalizedCategoryFilter, "is_illustrative")
    search_fields = PublishableContentAdmin.search_fields + ("challenge", "solution", "business_impact")
    filter_horizontal = ("technologies",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Case study flow"), {"fields": ("category", "is_illustrative", "challenge", "solution", "architecture", "technologies", "implementation", "business_impact")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Article)
class ArticleAdmin(PublishableContentAdmin):
    inlines = (ArticleTranslationInline,)
    list_display = ("title", "category", "vi_translation_status", "en_translation_status", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = (*PublishableContentAdmin.list_filter, LocalizedCategoryFilter)
    search_fields = PublishableContentAdmin.search_fields + ("content", "category")
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Article details"), {"fields": ("category", "reading_time", "content")}),
    ) + PublishableContentAdmin.fieldsets[2:]


@admin.register(Partner)
class PartnerAdmin(PublishableContentAdmin):
    has_translations = False
    list_display = ("title", "is_published", "is_featured", "display_order", "updated_at")
    list_filter = ("is_published", "is_featured", "updated_at")
    search_fields = PublishableContentAdmin.search_fields + ("relationship_type",)
    fieldsets = PublishableContentAdmin.fieldsets[:2] + (
        (_("Relationship details"), {"fields": ("website", "relationship_type")}),
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
class CompanyProfileAdmin(RichTextAdminMixin, admin.ModelAdmin):
    inlines = (CompanyProfileTranslationInline,)
    list_display = ("localized_name", "vi_translation_status", "en_translation_status", "localized_tagline", "updated_at")
    list_filter = (TranslationLanguageFilter, TranslationPublicationFilter, "updated_at")
    search_fields = ("name", "tagline", "introduction")
    readonly_fields = ("updated_at",)
    fieldsets = (
        (_("Company"), {"fields": ("name", "tagline", "logo")}),
        (_("Homepage introduction"), {"fields": ("homepage_intro_heading", "introduction")}),
        (_("About"), {"fields": ("mission", "vision")}),
        (_("Dates"), {"fields": ("updated_at",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("translations")

    @admin.display(description=_("Company name"), ordering="name")
    def localized_name(self, obj):
        return localized_value(obj, "name")

    @admin.display(description=_("Tagline"), ordering="tagline")
    def localized_tagline(self, obj):
        return localized_value(obj, "tagline")

    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists() and super().has_add_permission(request)

    vi_translation_status = PublishableContentAdmin.vi_translation_status
    en_translation_status = PublishableContentAdmin.en_translation_status


@admin.register(SiteSettings)
class SiteSettingsAdmin(RichTextAdminMixin, admin.ModelAdmin):
    inlines = (SiteSettingsTranslationInline,)
    list_display = ("localized_site_name", "vi_translation_status", "en_translation_status", "contact_email", "updated_at")
    list_filter = (TranslationLanguageFilter, TranslationPublicationFilter, "updated_at")
    readonly_fields = ("updated_at",)
    fieldsets = (
        (_("Site identity"), {"fields": ("site_name", "tagline", "logo")}),
        (_("Homepage hero"), {"fields": ("hero_eyebrow", "hero_title", "hero_description", ("hero_primary_label", "hero_primary_url"), ("hero_secondary_label", "hero_secondary_url"))}),
        (_("Default SEO"), {"fields": ("default_meta_description",)}),
        (_("Contact details"), {"fields": ("contact_email", "contact_phone", "contact_address")}),
        (_("Dates"), {"fields": ("updated_at",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("translations")

    @admin.display(description=_("Site name"), ordering="site_name")
    def localized_site_name(self, obj):
        return localized_value(obj, "site_name")

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


@admin.action(description=_("Mark selected enquiries as in progress"))
def mark_contact_requests_in_progress(modeladmin, request, queryset):
    queryset.update(status=ContactRequest.Status.IN_PROGRESS)


@admin.action(description=_("Close selected enquiries"))
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


# Django derives admin column and form labels from each model field's
# ``verbose_name``. Localize those labels consistently, including fields whose
# models predate the Vietnamese admin catalog.
ADMIN_FIELD_LABELS = {
    "id": _("ID"),
    "title": _("Title"),
    "slug": _("Slug"),
    "summary": _("Summary"),
    "description": _("Description"),
    "image": _("Image"),
    "image_alt": _("Image alt text"),
    "is_published": _("Is published"),
    "is_featured": _("Is featured"),
    "display_order": _("Display order"),
    "created_at": _("Created at"),
    "updated_at": _("Updated at"),
    "site_name": _("Site name"),
    "tagline": _("Tagline"),
    "default_meta_description": _("Default meta description"),
    "contact_email": _("Contact email"),
    "contact_phone": _("Contact phone"),
    "contact_address": _("Contact address"),
    "hero_eyebrow": _("Hero eyebrow"),
    "hero_title": _("Hero title"),
    "hero_description": _("Hero description"),
    "hero_primary_label": _("Primary button label"),
    "hero_primary_url": _("Primary button URL"),
    "hero_secondary_label": _("Secondary button label"),
    "hero_secondary_url": _("Secondary button URL"),
    "logo": _("Logo"),
    "name": _("Name"),
    "homepage_intro_heading": _("Homepage introduction heading"),
    "introduction": _("Introduction"),
    "mission": _("Mission"),
    "vision": _("Vision"),
    "category": _("Category"),
    "capabilities": _("Capabilities"),
    "business_value": _("Business value"),
    "services": _("Services"),
    "features": _("Features"),
    "technologies": _("Technologies"),
    "focus_areas": _("Focus areas"),
    "solutions": _("Solutions"),
    "website": _("Website"),
    "challenge": _("Challenge"),
    "solution": _("Solution"),
    "architecture": _("Architecture"),
    "implementation": _("Implementation"),
    "business_impact": _("Business impact"),
    "is_illustrative": _("Illustrative example"),
    "content": _("Content"),
    "reading_time": _("Reading time"),
    "relationship_type": _("Relationship type"),
    "value": _("Value"),
    "label": _("Label"),
    "path": _("Path"),
    "language": _("Language"),
    "meta_description": _("Meta description"),
    "canonical_url": _("Canonical URL"),
    "og_image": _("Social sharing image"),
    "allow_indexing": _("Allow search indexing"),
    "status": _("Status"),
    "seo_title": _("SEO title"),
    "seo_description": _("SEO description"),
    "service": _("Service"),
    "product": _("Product"),
    "industry": _("Industry"),
    "case_study": _("Case study"),
    "article": _("Article"),
    "company_profile": _("Company profile"),
    "site_settings": _("Site settings"),
    "email": _("Email address"),
    "company": _("Company"),
    "phone": _("Phone"),
    "interest": _("Area of interest"),
    "message": _("Message"),
    "consent_to_contact": _("Consent to be contacted"),
}

inline_models = (
    ArticleTranslation,
    CaseStudyTranslation,
    CompanyProfileTranslation,
    IndustryTranslation,
    ProductTranslation,
    ServiceTranslation,
    SiteSettingsTranslation,
    SolutionTranslation,
)
inline_model_names = {
    ArticleTranslation: _("Article translation"),
    CaseStudyTranslation: _("Case study translation"),
    CompanyProfileTranslation: _("Company profile translation"),
    IndustryTranslation: _("Industry translation"),
    ProductTranslation: _("Product translation"),
    ServiceTranslation: _("Service translation"),
    SiteSettingsTranslation: _("Site settings translation"),
    SolutionTranslation: _("Solution translation"),
}
for translation_model, label in inline_model_names.items():
    translation_model._meta.verbose_name = label
    translation_model._meta.verbose_name_plural = label

for registered_model in (*admin.site._registry, *inline_models):
    if registered_model._meta.app_label != "core":
        continue
    for field_name, label in ADMIN_FIELD_LABELS.items():
        try:
            registered_model._meta.get_field(field_name).verbose_name = label
        except FieldDoesNotExist:
            # A field label applies only to models that define that field.
            continue

for model, overrides in {
    CompanyProfile: {"name": _("Company name")},
    CompanyProfileTranslation: {"name": _("Company name")},
}.items():
    for field_name, label in overrides.items():
        model._meta.get_field(field_name).verbose_name = label
