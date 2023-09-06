from django.core.validators import RegexValidator

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(
                'Username "me" невозможен для регистрации.'
                'Примените фантазию.'
            )
        elif name is None or name == "":
            raise serializers.ValidationError(
                'Поле  "Username" не может быть пустым'
            )
        return name

    def validate_email(self, email):
        if email is None or email == "":
            raise serializers.ValidationError(
                'Поле  "Email" не может быть пустым'
            )
        return email


class UserMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
    # class Meta:
    #     model = User
    #     fields = (
    #         'username',
    #         'email',
    #         'first_name',
    #         'last_name',
    #         'bio',
    #         'role')
    #     read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True, max_length=128,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимые символы для имени пользователя'
        ), ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Username "me" невозможен для регистрации'
            )
        return username

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            return User.objects.get(username=username, email=email)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует'
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такая почта уже зарегестрирована'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(
                'Требуется ввести имя пользователя'
            )
        if confirmation_code is None:
            raise serializers.ValidationError(
                'Требуется ввести код подтверждения'
            )
        return data
