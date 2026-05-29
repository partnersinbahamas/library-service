from rest_framework import viewsets

from library.models import Book
from library.serializers import BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
