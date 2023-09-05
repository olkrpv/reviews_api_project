from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import get_token, register_user, UserViewSet
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles/(?P<title_pk>\d+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/auth/signup/', register_user, name='register_user'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/', include(router.urls)),
]
