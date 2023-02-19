import os

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".png"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload a JPG or PNG image.")

    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('File size exceeds the limit')
