import os
import re


def image_upload_path(instance, filename):
    # 'instance' is the instance of the Image model, and 'filename' is the original name of the uploaded file.
    return f"{instance.user.id}/images/{instance.id}/{filename}"


def sanitize_filename(filename):
    """
    Sanitizes a filename by removing any characters that are not alphanumeric, underscores, or periods.
    """
    basename, ext = os.path.splitext(filename)

    # Replace any characters that are not alphanumeric, underscores, or periods
    basename = re.sub(r'[^\w\.]', '_', basename)
    filename = f"{basename}{ext}"
    return filename
