from django.contrib import admin

from images.models import ExpiringLink, Image, ThumbnailSize

admin.site.register(Image)
admin.site.register(ThumbnailSize)
admin.site.register(ExpiringLink)
