from dataclasses import field
from rest_framework import serializers
from books.models import Book, Genre
from core.models import AppUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["name"]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["genre"]