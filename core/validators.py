from pathlib import Path

from django.core.exceptions import ValidationError


MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image_upload(upload):
    extension = Path(upload.name).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError("Upload a JPG, PNG or WebP image.")
    if upload.size > MAX_IMAGE_SIZE:
        raise ValidationError("Image files must be 5 MB or smaller.")
