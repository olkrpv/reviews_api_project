from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Avg

from rest_framework import viewsets, filters, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Genre, Category, Title, Review
from users.permissions import IsAdmin, IsModerator, IsAdminOrReadOnly
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer, TitleGETSerializer, ReviewSerializer, CommentSerializer
from .filters import TitleFilter
from .exceptions import ReviewAlreadyExists
from .mixins import CreateDestroyListViewSet


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    

class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
        

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModerator,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_pk')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_pk')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            raise ReviewAlreadyExists()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModerator,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_pk')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_pk')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)