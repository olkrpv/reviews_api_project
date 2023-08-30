from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer
from .filters import TitleFilter

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)
