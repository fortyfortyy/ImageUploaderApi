from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from images import views

urlpatterns = [
    path("", views.ImageListView.as_view(), name="image-list"),
    path("upload/", views.ImageCreateView.as_view(), name="image-create"),
    path("expiring-links/", views.ExpiringLinkListCreateView.as_view(), name='expiring-link-create-list'),
    path("expiring-links/<str:signed_link>/", views.ExpiringLinkDetailView.as_view(), name='expiring-link-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
