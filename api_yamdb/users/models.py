from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_username


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'


class User(AbstractUser):
    """Класс пользователей."""

    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимые символы для имени пользователя'),
            validate_username
        ]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='пару слов о себе',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль пользователя',
        choices=ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff
