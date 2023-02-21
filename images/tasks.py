from __future__ import absolute_import, unicode_literals

import logging
import os
from io import BytesIO

from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from PIL import Image as PIL_Image

from images.models import Image
from ImageUploadApi.storage import GoogleCloudMediaFileStorage

logger = logging.getLogger(__name__)


@shared_task
def generate_thumbnail_task(pk: str):
    logger.info("generate thumbnails for %s" % pk)

    instance = Image.objects.get(id=pk)
    filename, ext = os.path.splitext(os.path.basename(instance.image.name))
    image_name = filename.split("/")[-1]

    account_tier = instance.user.account_tier
    thumbnail_sizes = account_tier.get_thumbnail_sizes

    # Convert the image into thumbnails based on user account tier and save to GCP bucket
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


@shared_task
def cleanup_image_folder_task(path: str):
    logger.info("delete thumbnails folder %s" % path)

    storage = GoogleCloudMediaFileStorage()
    for file in storage.listdir(os.path.dirname(path))[1]:
        logger.info("deleting file from the bucket: %s" % file)
        storage.delete(os.path.join(os.path.dirname(path), file))
