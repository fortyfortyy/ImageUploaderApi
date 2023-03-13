import mimetypes

from django.http import FileResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied

from images.mixins import ExpiringLinkMixin
from images.models import ExpiringLink, Image
from images.serializers import (
    ExpiringLinkCreateSerializer,
    ExpiringLinkListSerializer,
    ImageCreateSerializer,
    ImageListSerializer,
)


class ImageListView(generics.ListAPIView):
    serializer_class = ImageListSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageCreateSerializer


class ExpiringLinkListCreateView(generics.ListCreateAPIView, ExpiringLinkMixin):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpiringLinkCreateSerializer
        return ExpiringLinkListSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = self.link
        return response

    def perform_create(self, serializer) -> None:
        expires_in = self.request.data.get('expires_in')
        self.link: dict = self.generate_expiring_link(serializer.validated_data['image'], expires_in)

    def get_queryset(self):
        """List expiring links."""
        return ExpiringLink.objects.filter(image__user=self.request.user)

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ExpiringLinkDetailView(generics.RetrieveAPIView, ExpiringLinkMixin):
    queryset = ExpiringLink.objects.all()

    def get_object(self):
        signed_link = self.kwargs.get('signed_link')

        expiring_link_id = self.decode_signed_value(signed_link)
        expiring_link = generics.get_object_or_404(self.queryset, pk=expiring_link_id)
        if expiring_link.is_expired():
            expiring_link.delete()
            raise NotFound("Link has expired")

        if expiring_link.image.user != self.request.user:
            raise PermissionDenied("User not authorized to view expiring link")

        return expiring_link.image

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object().image
        content_type, encoding = mimetypes.guess_type(image.name)
        response = FileResponse(image, content_type=content_type, as_attachment=True, filename=image.name.split('/')[-1])
        return response
