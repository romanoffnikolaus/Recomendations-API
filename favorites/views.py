from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .models import Favorites, History
from .serializers import FavoriteListSerializer, HistorySerializer


class FavoritesView(APIView):
    @swagger_auto_schema(tags=['Favorites'])
    def get(self, request):
        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoriteListSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(tags=['Favorites'])
    def delete(self, request, pk):
        try:
            favorite = Favorites.objects.filter(id=pk).first()
            copy = favorite
            favorite.delete()
            return Response(f'Книга {copy} удалена из избранного')

        except Favorites.DoesNotExist:
            return Response("Ошибка, книга не найдена")
        

class HistoryList(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        user = self.request.user
        sorted_list = History.objects.filter(user=user).order_by('-viewed_on')
        return sorted_list
