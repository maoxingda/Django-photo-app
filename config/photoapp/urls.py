"""Photoapp URL patterns"""

from django.urls import path

from .views import (
    PhotoTagListView,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView,
    TagListView,
    PhotoListView,
    yes_no_tag,
    TaggedTagListView
)

app_name = 'photo'

urlpatterns = [
    path('', TagListView.as_view(), name='tags'),

    path('tagged/tags/<str:flag>/', TaggedTagListView.as_view(), name='tagged_tags'),

    path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),

    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),

    path('photo/create/', PhotoCreateView.as_view(), name='create'),

    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('photo/yes_no_tag/update/', yes_no_tag, name='yes-no-tag'),

    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

    path('photos/', PhotoListView.as_view(), name='photos'),
]
