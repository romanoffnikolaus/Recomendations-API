from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from functools import reduce
import operator

from drf_yasg.utils import swagger_auto_schema

from books.models import Book
from books.serializers import BookSerialiser
from favorites.models import History
from .utils import get_similar_words


class NewBooksList(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-added')[:20]
    serializer_class = BookSerialiser
    @swagger_auto_schema(tags=['Default recommendations'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PopularBooksList(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-views')[:20]
    serializer_class = BookSerialiser
    @swagger_auto_schema(tags=['Default recommendations'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RandomBookRecomendation(generics.ListAPIView):
    serializer_class = BookSerialiser
    def get_queryset(self):
        return Book.objects.all().order_by('?')[:1]
    
    @swagger_auto_schema(tags=['Default recommendations'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class HistoryBookRecommendation(APIView):
    @swagger_auto_schema(tags=['Algorithmic recommendations'])
    def get(self, request, *args, **kwargs):
        user = request.user
        history = History.objects.filter(user=user)
        genres = {}
        for h in history:
            for g in h.book.genre.all():
                print(g)
                if g.genre not in genres:
                    genres[g.genre] = 1
                else:
                    genres[g.genre] += 1
        sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
        books = Book.objects.filter(genre__genre__in=[x[0] for x in sorted_genres[:3]])
        books = books.exclude(history__user=user).distinct()
        serializer = BookSerialiser(books, many=True)
        return Response(serializer.data)


class LiveSearchView(APIView): 
    @swagger_auto_schema(tags=['Live-search'])
    def post(self, request):
        search_param = request.data.get('search')
        if search_param:
            similar_words = get_similar_words(search_param)
            try:
                books = Book.objects.filter(
                    reduce(operator.or_, 
                        [Q(title__icontains=i) | 
                            Q(author__icontains=i) for i in similar_words]))
            except Exception: return Response('Нет результатов по вашему запросу. Повезет в другой раз')
            serializer = BookSerialiser(books, many=True)
            return Response({f'Результат запроса по поиску {search_param} ':serializer.data})
        else:
            return Response('Передайте папраметр для поиска')
