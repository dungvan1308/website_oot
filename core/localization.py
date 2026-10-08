from types import SimpleNamespace

from django.urls import translate_url


def localized_content(instance, language):
    """Return published CMS translation fields, falling back to a published locale and base data."""
    if instance is None:
        return None

    translations = list(instance.translations.all())
    published = {item.language: item for item in translations if item.status == "published"}
    translation = published.get(language) or published.get("vi") or published.get("en")

    values = {}
    field_names = set()
    for item in translations:
        field_names.update(field.name for field in item._meta.fields)
    for field_name in field_names:
        if field_name in {"id", "pk", "language", "status", "updated_at"}:
            continue
        translated_value = getattr(translation, field_name, "") if translation else ""
        base_value = getattr(instance, field_name, "")
        values[field_name] = translated_value or base_value

    for field in instance._meta.fields:
        if field.name not in values:
            values[field.name] = getattr(instance, field.name)

    values["translation_language"] = translation.language if translation else None
    values["translation_status"] = translation.status if translation else "missing"
    return SimpleNamespace(**values)


def switch_language_url(request, language):
    return translate_url(request.get_full_path(), language)
