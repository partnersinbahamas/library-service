from rest_framework import serializers

from library.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "api_id",
            "title",
            "summaries",
            "author",
            "cover",
            "inventory",
            "daily_fee",
            "year_of_publication",
        )
        read_only_fields = ("id", "api_id")


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
            "year_of_publication",
        )
