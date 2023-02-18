from django.urls import path

from images import views

urlpatterns = [
    path("", views.ImageListView.as_view(), name="image-list"),
]
