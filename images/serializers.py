from rest_framework import serializers

from images.models import ExpiringLink, Image
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
        thumbnails = obj.get_thumbnails()
        request = self.context.get('request')
        thumbnails_to_return = []

        for thumbnail in thumbnails:
            if thumbnail.startswith('http' or 'https'):
                # Already a full URL, no need to modify
                thumbnails_to_return.append(thumbnail)
            elif request is not None:
                # Generate full URL for thumbnail using request's build_absolute_uri method
                thumbnail_url = request.build_absolute_uri(thumbnail)
                thumbnails_to_return.append(thumbnail_url)

        return thumbnails_to_return


class ImageCreateSerializer(serializers.ModelSerializer):
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


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('link',)


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('image', 'expires_in')
