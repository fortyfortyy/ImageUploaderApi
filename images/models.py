import uuid

from django.db import models
from django.conf import settings

from images.utils import image_upload_path

User = settings.AUTH_USER_MODEL  # auth.User


class ThumbnailSize(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.width}x{self.height}"

    def __repr__(self):
        return """ThumbnailSize(width='%s', height='%s')""" % (self.width, self.height)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.image.name}"

    def __repr__(self):
        return """Image(id='%s', user='%s', image='%s', uploaded_at='%s')""" % (
            self.id,
            self.user,
            self.image.name,
            self.uploaded_at,
        )


class ExpiringLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="expiring_links")
    link = models.CharField(max_length=100)
    expiry_time = models.DateTimeField()

    def __str__(self):
        return f"{self.link} - {self.image.name}"

    def __repr__(self):
        return """ExpiringLink(image='%s', link='%s', expiry_time='%s')""" % (
            self.image.name,
            self.link,
            self.expiry_time
        )
