from rest_framework import serializers

from .models import Favorites, History
from books.models import Book



class BookSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    book = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Favorites
        fields = '__all__'
    

class FavoriteListSerializer(serializers.ModelSerializer):
    book = BookSerialiser()
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Favorites
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'