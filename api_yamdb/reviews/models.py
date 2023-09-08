from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class CategoryGenreModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(CategoryGenreModel):

    class Meta(CategoryGenreModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(CategoryGenreModel):

    class Meta(CategoryGenreModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            MaxValueValidator(
                limit_value=datetime.now().year,
                message='Год выпуска не может быть больше текущего!'
            )
        ],
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-year']

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
