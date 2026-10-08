from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from core.validators import validate_image_upload


class PublishableContent(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=190, unique=True)
    summary = models.CharField(max_length=320, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="cms/content/", blank=True, validators=[validate_image_upload])
    image_alt = models.CharField(max_length=180, blank=True)
    is_published = models.BooleanField(default=False, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=120, default="Ocean One Technology")
    tagline = models.CharField(max_length=200, blank=True)
    default_meta_description = models.CharField(max_length=320, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    contact_address = models.CharField(max_length=240, blank=True)
    hero_eyebrow = models.CharField(max_length=160, blank=True)
    hero_title = models.CharField(max_length=240, blank=True)
    hero_description = models.CharField(max_length=500, blank=True)
    hero_primary_label = models.CharField(max_length=80, blank=True)
    hero_primary_url = models.CharField(max_length=240, blank=True)
    hero_secondary_label = models.CharField(max_length=80, blank=True)
    hero_secondary_url = models.CharField(max_length=240, blank=True)
    logo = models.ImageField(upload_to="cms/site/", blank=True, validators=[validate_image_upload])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


class CompanyProfile(models.Model):
    name = models.CharField(max_length=180, default="Ocean One Technology")
    tagline = models.CharField(max_length=240, blank=True)
    homepage_intro_heading = models.CharField(max_length=240, blank=True)
    introduction = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    logo = models.ImageField(upload_to="cms/company/", blank=True, validators=[validate_image_upload])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class Service(PublishableContent):
    class Category(models.TextChoices):
        DATA_PLATFORM = "data_platform", _("Data platform")
        BUSINESS_INTELLIGENCE = "business_intelligence", _("Business intelligence")
        ENTERPRISE_SOFTWARE = "enterprise_software", _("Enterprise software")
        BANKING_TECHNOLOGY = "banking_technology", _("Banking technology")
        CLOUD_TRANSFORMATION = "cloud_transformation", _("Cloud & digital transformation")

    category = models.CharField(max_length=32, choices=Category.choices, db_index=True)
    capabilities = models.TextField(blank=True, help_text="Enter one capability per line.")
    business_value = models.TextField(blank=True)

    class Meta(PublishableContent.Meta):
        verbose_name_plural = "services"


class Solution(PublishableContent):
    capabilities = models.TextField(blank=True, help_text="Enter one capability per line.")
    business_value = models.TextField(blank=True)
    services = models.ManyToManyField(Service, blank=True, related_name="solutions")


class Technology(PublishableContent):
    category = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True, validators=[URLValidator(schemes=["https"])])


class Product(PublishableContent):
    features = models.TextField(blank=True, help_text="Enter one feature per line.")
    business_value = models.TextField(blank=True)
    technologies = models.ManyToManyField(Technology, blank=True, related_name="products")


class Industry(PublishableContent):
    focus_areas = models.TextField(blank=True, help_text="Enter one focus area per line.")
    solutions = models.ManyToManyField(Solution, blank=True, related_name="industries")


class CaseStudy(PublishableContent):
    category = models.CharField(max_length=120, blank=True)
    challenge = models.TextField()
    solution = models.TextField()
    architecture = models.TextField(blank=True, help_text="Enter one architecture layer per line.")
    technologies = models.ManyToManyField(Technology, blank=True, related_name="case_studies")
    implementation = models.TextField(blank=True, help_text="Enter one implementation step per line.")
    business_impact = models.TextField(blank=True, help_text="Enter one outcome per line.")
    is_illustrative = models.BooleanField(default=True, help_text="Keep enabled for illustrative scenarios. Disable only for a confirmed, approved client engagement.")


class Article(PublishableContent):
    category = models.CharField(max_length=120, blank=True)
    content = models.TextField(blank=True)
    reading_time = models.CharField(max_length=32, blank=True)


class Partner(PublishableContent):
    website = models.URLField(blank=True, validators=[URLValidator(schemes=["https"])])
    relationship_type = models.CharField(max_length=120, blank=True, help_text="Use precise, verified wording for any relationship claim.")


class Statistic(models.Model):
    value = models.CharField(max_length=40)
    label = models.CharField(max_length=180)
    is_published = models.BooleanField(default=False, db_index=True)
    display_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.value} — {self.label}"


class SEOSetting(models.Model):
    path = models.CharField(max_length=240, help_text="Localized page path, for example /vi/services/.")
    language = models.CharField(max_length=2, choices=(("vi", _("Vietnamese")), ("en", _("English"))), default="en")
    title = models.CharField(max_length=180, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    canonical_url = models.URLField(blank=True)
    og_image = models.ImageField(upload_to="cms/seo/", blank=True, validators=[validate_image_upload])
    allow_indexing = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["path"]
        constraints = [models.UniqueConstraint(fields=("path", "language"), name="unique_seo_path_language")]
        verbose_name = "SEO setting"
        verbose_name_plural = "SEO settings"

    def __str__(self):
        return f"{self.path} ({self.language})"


class TranslationFields(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")

    LANGUAGE_CHOICES = (("vi", _("Vietnamese")), ("en", _("English")))

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT, db_index=True)
    title = models.CharField(max_length=180)
    summary = models.CharField(max_length=320, blank=True)
    description = models.TextField(blank=True)
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.CharField(max_length=320, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceTranslation(TranslationFields):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="translations")
    category = models.CharField(max_length=120, blank=True)
    capabilities = models.TextField(blank=True)
    business_value = models.TextField(blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("service", "language"), name="unique_service_translation_language")]
        ordering = ("language",)


class SolutionTranslation(TranslationFields):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="translations")
    capabilities = models.TextField(blank=True)
    business_value = models.TextField(blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("solution", "language"), name="unique_solution_translation_language")]
        ordering = ("language",)


class ProductTranslation(TranslationFields):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="translations")
    features = models.TextField(blank=True)
    business_value = models.TextField(blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("product", "language"), name="unique_product_translation_language")]
        ordering = ("language",)


class IndustryTranslation(TranslationFields):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name="translations")
    focus_areas = models.TextField(blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("industry", "language"), name="unique_industry_translation_language")]
        ordering = ("language",)


class CaseStudyTranslation(TranslationFields):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name="translations")
    category = models.CharField(max_length=120, blank=True)
    challenge = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    architecture = models.TextField(blank=True)
    implementation = models.TextField(blank=True)
    business_impact = models.TextField(blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("case_study", "language"), name="unique_case_translation_language")]
        ordering = ("language",)


class ArticleTranslation(TranslationFields):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="translations")
    category = models.CharField(max_length=120, blank=True)
    content = models.TextField(blank=True)
    reading_time = models.CharField(max_length=32, blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("article", "language"), name="unique_article_translation_language")]
        ordering = ("language",)


class CompanyProfileTranslation(TranslationFields):
    company_profile = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name="translations")
    name = models.CharField(max_length=180, blank=True)
    tagline = models.CharField(max_length=240, blank=True)
    homepage_intro_heading = models.CharField(max_length=240, blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("company_profile", "language"), name="unique_company_translation_language")]
        ordering = ("language",)


class SiteSettingsTranslation(TranslationFields):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="translations")
    site_name = models.CharField(max_length=120, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    default_meta_description = models.CharField(max_length=320, blank=True)
    hero_eyebrow = models.CharField(max_length=160, blank=True)
    hero_title = models.CharField(max_length=240, blank=True)
    hero_description = models.CharField(max_length=500, blank=True)
    hero_primary_label = models.CharField(max_length=80, blank=True)
    hero_primary_url = models.CharField(max_length=240, blank=True)
    hero_secondary_label = models.CharField(max_length=80, blank=True)
    hero_secondary_url = models.CharField(max_length=240, blank=True)

    class Meta(TranslationFields.Meta):
        constraints = [models.UniqueConstraint(fields=("site_settings", "language"), name="unique_site_settings_translation_language")]
        ordering = ("language",)


class ContactRequest(models.Model):
    class Interest(models.TextChoices):
        DATA_PLATFORM = "data_platform", _("Data platform")
        BUSINESS_INTELLIGENCE = "business_intelligence", _("Business intelligence")
        ENTERPRISE_SOFTWARE = "enterprise_software", _("Enterprise software")
        BANKING_TECHNOLOGY = "banking_technology", _("Banking technology")
        CLOUD_TRANSFORMATION = "cloud_transformation", _("Cloud & digital transformation")
        OTHER = "other", _("Other")

    class Status(models.TextChoices):
        NEW = "new", _("New")
        IN_PROGRESS = "in_progress", _("In progress")
        CLOSED = "closed", _("Closed")

    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    company = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    interest = models.CharField(max_length=32, choices=Interest.choices, default=Interest.OTHER)
    message = models.TextField(max_length=4000)
    consent_to_contact = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contact request"
        verbose_name_plural = "contact requests"

    def __str__(self):
        return f"{self.name} — {self.get_interest_display()}"
