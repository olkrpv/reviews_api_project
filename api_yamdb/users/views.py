import uuid
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.permissions import IsAdmin
from users.serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer
)


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_user(request):
    """Функция регистрации user, генерации и отправки кода на почту"""
    username = request.data.get('username')
    email = request.data.get('email')

    try:
        '''Если пользователь уже существует, посылаем ему код.'''
        user = User.objects.get(email=email, username=username)
        confirmation_code = str(uuid.uuid4())
        user.confirmation_code = confirmation_code
        user.save()
        data = request.data
    except ObjectDoesNotExist:
        '''Если пользователя не существует, то регистрируем.'''
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        confirmation_code = default_token_generator.make_token(
            User.objects.create(email=email, username=username)
        )
        data = serializer.data
    send_mail(
        subject='Регистрация в проекте YaMDb и код подтверждения.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[email],
    )
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    """Функция выдачи токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            data={'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        'Неверный код подтверждения или имя пользователя!',
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        '''Обработчик запросов к users/me.'''
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
