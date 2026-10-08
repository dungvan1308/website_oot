from django.db import migrations


def seed_english_translations(apps, schema_editor):
    db = schema_editor.connection.alias
    text_fields = ("title", "summary", "description")
    content_models = (
        ("Service", "ServiceTranslation", "service", ("category", "capabilities", "business_value")),
        ("Solution", "SolutionTranslation", "solution", ("capabilities", "business_value")),
        ("Product", "ProductTranslation", "product", ("features", "business_value")),
        ("Industry", "IndustryTranslation", "industry", ("focus_areas",)),
        ("CaseStudy", "CaseStudyTranslation", "case_study", ("category", "challenge", "solution", "architecture", "implementation", "business_impact")),
        ("Article", "ArticleTranslation", "article", ("category", "content", "reading_time")),
    )
    for model_name, translation_name, relation_name, extra_fields in content_models:
        parent_model = apps.get_model("core", model_name)
        translation_model = apps.get_model("core", translation_name)
        for parent in parent_model.objects.using(db).all():
            values = {field: getattr(parent, field, "") for field in (*text_fields, *extra_fields)}
            values.update(language="en", status="published" if parent.is_published else "draft")
            translation_model.objects.using(db).get_or_create(
                **{relation_name: parent, "language": "en"}, defaults=values
            )

    for model_name, translation_name, relation_name, mapping in (
        ("CompanyProfile", "CompanyProfileTranslation", "company_profile", {
            "title": "name", "name": "name", "summary": "tagline", "tagline": "tagline",
            "description": "introduction", "homepage_intro_heading": "homepage_intro_heading",
            "mission": "mission", "vision": "vision",
        }),
        ("SiteSettings", "SiteSettingsTranslation", "site_settings", {
            "title": "site_name", "site_name": "site_name", "summary": "tagline", "tagline": "tagline",
            "description": "hero_description", "default_meta_description": "default_meta_description",
            "hero_eyebrow": "hero_eyebrow", "hero_title": "hero_title", "hero_description": "hero_description",
            "hero_primary_label": "hero_primary_label", "hero_secondary_label": "hero_secondary_label",
        }),
    ):
        parent_model = apps.get_model("core", model_name)
        translation_model = apps.get_model("core", translation_name)
        for parent in parent_model.objects.using(db).all():
            values = {target: getattr(parent, source, "") for target, source in mapping.items()}
            values.update(language="en", status="published")
            translation_model.objects.using(db).get_or_create(
                **{relation_name: parent, "language": "en"}, defaults=values
            )

    seo_model = apps.get_model("core", "SEOSetting")
    for setting in seo_model.objects.using(db).all():
        if not setting.path.startswith("/en/"):
            path = setting.path.lstrip("/")
            setting.path = f"/en/{path}" if path else "/en/"
        setting.language = "en"
        setting.save(using=db, update_fields=("path", "language"))


class Migration(migrations.Migration):
    dependencies = [("core", "0005_articletranslation_casestudytranslation_and_more")]
    operations = [migrations.RunPython(seed_english_translations, migrations.RunPython.noop)]
