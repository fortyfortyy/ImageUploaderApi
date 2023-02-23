import mimetypes

from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

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
    parser_classes = (MultiPartParser, FormParser)


class ExpiringLinkListCreateView(generics.ListCreateAPIView, ExpiringLinkMixin):
    queryset = Image.objects.all()
    # serializer_class = ExpiringLinkSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExpiringLinkCreateSerializer
        return ExpiringLinkListSerializer

    def list(self, request, *args, **kwargs):
        links = ExpiringLink.objects.filter(image__user=request.user)
        serializer = self.get_serializer_class()(links, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        expires_in = request.data.get('expires_in')
        link = self.generate_expiring_link(validated_data['image'], expires_in)
        return Response(link, status=status.HTTP_201_CREATED)


class ExpiringLinkDetailView(generics.RetrieveAPIView, ExpiringLinkMixin):
    queryset = ExpiringLink.objects.all()

    def get_object(self):
        signed_link = self.kwargs.get('signed_link')

        expiring_link_id = self.decode_signed_value(signed_link)
        expiring_link = get_object_or_404(self.queryset, pk=expiring_link_id)
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
