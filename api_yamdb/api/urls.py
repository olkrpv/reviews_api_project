from django.urls import include, path
from rest_framework import routers

from users.views import get_token, register_user, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', register_user, name='register_user'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/', include(router.urls)),
]
