from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

router = DefaultRouter()
router.register('v1/categories', CategoryViewSet)
router.register('v1/genres', GenreViewSet)
router.register('v1/titles', TitleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]