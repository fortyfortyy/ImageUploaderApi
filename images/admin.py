from django.contrib import admin
from images.models import Image, ThumbnailSize, ExpiringLink

admin.site.register(Image)
admin.site.register(ThumbnailSize)
admin.site.register(ExpiringLink)
