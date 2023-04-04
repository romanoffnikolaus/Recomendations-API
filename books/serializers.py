from rest_framework.serializers import ModelSerializer

from .models import Genre, Book


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerialiser(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
