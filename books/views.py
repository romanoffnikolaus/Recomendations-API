from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

import django_filters
from drf_yasg.utils import swagger_auto_schema


from .serializers import BookSerialiser, GenreSerializer
from .models import Genre, Book
from favorites import models, serializers
from favorites.models import History


class PermissioinMixin():
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy','create']:
            permissions = [IsAdminUser,]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class GenreViewset(PermissioinMixin, ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @swagger_auto_schema(tags=['Genres'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Genres'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Genres'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Genres'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Genres'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Genres'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BookViewset(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerialiser
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    filterset_fields = ['genre', 'author', 'title']
    search_fields = ['title', 'genre__title', 'author']
    ordering_fields = ['added', 'views']
    ordering = ['added']

    @swagger_auto_schema(tags=['Books'])
    def create(self, request, *args, **kwargs):
        try:
            genre_slugs = [i.strip() for i in request.data.get('genre').split(',')]
        except BaseException:
            return Response('Tag requires')
        genre = list(Genre.objects.filter(slug__in=genre_slugs))
        if len(genre) != len(genre_slugs):
            raise ValidationError(f"Invalid genre")
        data = request.data.copy()
        data.setlist('genre', genre)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Books'])
    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        book.views += 1
        book.save()
        serializer = self.get_serializer(book)
        history = History.objects.create(user=request.user, book=book)
        history.save()
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Books'])
    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        book = self.get_object()
        user = request.user
        serializer = serializers.FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            favorites_exists = models.Favorites.objects.filter(book=book, user=user).exists()
            if favorites_exists:
                models.Favorites.objects.filter(book=book, user=user).delete()
                message = 'Removed from favorites'
            else:
                models.Favorites.objects.create(book=book, in_favorites=True, user=user)
                message = 'Added to favorites'
            return Response(message, status=200)
    
    @swagger_auto_schema(tags=['Books'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Books'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Books'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Books'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    