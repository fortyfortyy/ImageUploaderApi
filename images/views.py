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


# TODO zaimplementować image upload, oraz jego walidacje
# TODO zaimplementować wygasające linki
# TODO przy inicjacji apki od nowa zaimplemenotwać testowego usera
# TODO zrobić config.py z domyślnymi globalnymi wartościami
# TODO testy
# TODO google storage, redis, celery
# TODO docker compose, zmienne środowiskowe
# TODO caching
# TODO hosting na cloud providerze
