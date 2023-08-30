import uuid

from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import User
from users.serializers import (UserSerializer, UserMeSerializer,
                               SignUpSerializer, TokenSerializer)
from users.permissions import IsAdmin


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
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        confirmation_code = str(uuid.uuid4())

        User.objects.get_or_create(email=email, username=username,
                                   confirmation_code=confirmation_code,)
        data = serializer.data
    send_mail(
        subject='Регистрация в проекте YaMDb и код подтверждения.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[email]
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
    if confirmation_code != user.confirmation_code:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    return Response({'token': str(refresh.access_token)},
                    status=status.HTTP_200_OK)


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
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)
