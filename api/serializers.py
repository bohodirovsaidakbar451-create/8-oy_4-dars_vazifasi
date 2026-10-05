from rest_framework import serializers
from .models import Genre, Book, Comment

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ["updated"]
        read_only_fields = ["id", "created"]
        extra_kwargs = {
            "name": {"min_length": 2, "trim_whitespace": True}
        }


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["updated"]
        read_only_fields = ["id", "created"]
        extra_kwargs = {
            "price": {"min_value": 0},
            "published_year": {"min_value": 0, "max_value": 2100},
            "description": {"required": False},
            "genre": {"required": True, "allow_null": False}
        }


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ["updated"]
        depth = 1


class GenreDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(source="book_set", many=True, read_only=True)

    class Meta:
        model = Genre
        exclude = ["updated"]
        read_only_fields = ["id", "created"]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        exclude = ["updated"]
        read_only_fields = ["id", "user", "created"]
        extra_kwargs = {
            "text": {"min_length": 2, "max_length": 1000}
        }
