from django.db import models

class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
    )
        
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг',
    )
        
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска'
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
