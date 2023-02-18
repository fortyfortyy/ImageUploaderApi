from rest_framework import serializers

from images.models import Image


class ImageSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = [
            "images",
        ]

    def get_images(self, obj):
        if not hasattr(obj, "id"):
            return None

        if not isinstance(obj, Image):
            return None

        return obj.get_thumbnails()
