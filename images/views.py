from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

from images.models import Image
from images.serializers import ImageListSerializer, ImageUploadSerializer


class ImageListView(generics.ListAPIView):
    serializer_class = ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ImageUploadViewSet(generics.CreateAPIView):
    queryset = Image
    serializer_class = ImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser)


# TODO zaimplementować wygasające linki
# TODO przy inicjacji apki od nowa zaimplemenotwać testowego usera
# TODO zrobić config.py z domyślnymi globalnymi wartościami
# TODO testy
# TODO google storage, redis, celery
# TODO docker compose, zmienne środowiskowe
# TODO caching
# TODO hosting na cloud providerze
