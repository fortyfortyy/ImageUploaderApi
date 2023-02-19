from rest_framework import serializers

from images.models import Image
from images.utils import sanitize_filename
from images.validators import validate_image_extension


class ImageListSerializer(serializers.ModelSerializer):
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


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

    def validate_image(self, value):
        validate_image_extension(value)
        filename = sanitize_filename(value.name)
        value.name = filename
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Image.objects.create(**validated_data)
