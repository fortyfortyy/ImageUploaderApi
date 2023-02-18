from rest_framework import generics

from images.models import Image
from images.serializers import ImageSerializer


class ImageListView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user

        return Image.objects.filter(user=user)
