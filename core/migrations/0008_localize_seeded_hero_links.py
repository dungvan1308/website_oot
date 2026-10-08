from django.db import migrations


def localize_hero_links(apps, schema_editor):
    Translation = apps.get_model("core", "SiteSettingsTranslation")
    db = schema_editor.connection.alias
    for item in Translation.objects.using(db).all():
        prefix = f"/{item.language}"
        item.hero_primary_url = f"{prefix}/solutions/"
        item.hero_secondary_url = f"{prefix}/contact/"
        item.save(using=db, update_fields=("hero_primary_url", "hero_secondary_url"))


class Migration(migrations.Migration):
    dependencies = [("core", "0007_sitesettingstranslation_hero_primary_url_and_more")]
    operations = [migrations.RunPython(localize_hero_links, migrations.RunPython.noop)]
