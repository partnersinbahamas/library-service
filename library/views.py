from rest_framework import viewsets

from library.models import Book
from library.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

    def get_serializer_class(self):
        match self.action:
            case "list":
                return BookListSerializer
            case _:
                # BookListSerializer as a default serializer
                return BookSerializer
