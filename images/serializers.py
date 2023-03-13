from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from images.models import ExpiringLink, Image
from images.utils import sanitize_filename
from images.validators import validate_image_extension


class ImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = [
            "image",
        ]

    def get_image(self, obj):
        thumbnails = obj.get_thumbnails()
        thumbnails_to_return = []
        for thumbnail in thumbnails:
            if thumbnail.startswith(('https', 'http')):
                # Already a full URL, no need to modify
                thumbnails_to_return.append(thumbnail)
                continue

            path = settings.MEDIA_URL + thumbnail
            thumbnails_to_return.append(path)

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

    def __init__(self, *args, **kwargs):
        super(ExpiringLinkCreateSerializer, self).__init__(*args, **kwargs)

        # Set the choices based on user's iamges
        user = self.context.get('request').user
        images = Image.objects.filter(user=user)
        self.fields['image'].queryset = images

    def validate_image(self, data):
        if self.context.get('request').user != data.user:
            raise ValidationError('You do not have access to this image')
        return data
