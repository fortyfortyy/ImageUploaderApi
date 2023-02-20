from __future__ import absolute_import, unicode_literals

import logging
import os
from io import BytesIO

from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from PIL import Image as PIL_Image

from images.models import Image

logger = logging.getLogger(__name__)


@shared_task
def generate_thumbnail_task(pk: str):
    logger.info("generate thumbnails for %s" % pk)

    instance = Image.objects.get(id=pk)
    filename, ext = os.path.splitext(os.path.basename(instance.image.name))
    image_name = filename.split("/")[-1]

    account_tier = instance.user.account_tier
    thumbnail_sizes = account_tier.get_thumbnail_sizes

    # Convert the image for each thumbnail size and save to disk
    for size in thumbnail_sizes:
        img_file = BytesIO(instance.image.read())
        original_image = PIL_Image.open(img_file)

        # Resize the image, ANTIALIAS ensure that the resized image has the best possible resolution
        thumbnail = original_image.resize((size.width, size.height), PIL_Image.ANTIALIAS)

        # Save the resized image to the path
        thumb_io = BytesIO()

        thumbnail.save(thumb_io, format="JPEG" if ext.lower() == ".jpg" else "PNG")
        thumbnail_path = f"{image_name}_{size.height}{ext.lower()}"

        thumbail_file = SimpleUploadedFile(
            thumbnail_path, thumb_io.getvalue(), content_type="image/jpeg" if ext.lower() == ".jpg" else "image/png"
        )
        instance.image.save(thumbnail_path, thumbail_file, save=False)

        # Upload thumbnails to Google Cloud Storage
        # client = storage.Client()
        # bucket = client.bucket('my-bucket')
        # for size, thumbnail_file in thumbnails.items():
        #     blob = bucket.blob(f'thumbnails/{os.path.basename(thumbnail_file)}')
        #     blob.upload_from_filename(thumbnail_file)
        #     blob.make_public()


@shared_task
def cleanup_image_folder_task(path: str):
    logger.info("delete folder thumbnails from %s" % path)

    thumbnails_folder = os.path.dirname(path)
    if not os.path.isdir(thumbnails_folder):
        logger.warning("Folder %s does not exist" % thumbnails_folder)
        return

    for filename in os.listdir(thumbnails_folder):
        file_path = os.path.join(thumbnails_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            logger.warning("Failed to delete %s. Reason: %s" % (file_path, e))

    os.rmdir(thumbnails_folder)
