import os

from django.core.exceptions import ValidationError

from default_configs import MAX_EXPIRY_LINK_TIME, MAX_UPLOAD_SIZE, MIN_EXPIRY_LINK_TIME


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".png"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Please upload a JPG or PNG image.")

    if value.size > MAX_UPLOAD_SIZE:
        raise ValidationError('File size exceeds the limit')


def validate_expiration_time(value):
    if not MIN_EXPIRY_LINK_TIME <= value <= MAX_EXPIRY_LINK_TIME:
        raise ValidationError(f'Expiration time must be between {MIN_EXPIRY_LINK_TIME} and {MAX_EXPIRY_LINK_TIME} seconds.')
