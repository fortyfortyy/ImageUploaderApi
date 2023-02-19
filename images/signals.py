import os
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image as PIL_Image

from images.models import Image


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance, **kwargs):
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

        # Save the resized image to the storage
        # thumbnail_storage = instance.image.storage
        # thumbnail_path = thumbnail_storage.save(thumb_file.name, thumb_file)
        # thumbnail_storage.save(thumb_file.name, thumb_file)
