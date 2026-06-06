from rest_framework import viewsets

from library.models import Book
from library.pagination import BookListPagination
from library.serializers import BookListSerializer, BookSerializer
from management.permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    pagination_class = BookListPagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        match self.action:
            case "list":
                return BookListSerializer
            case _:
                # BookListSerializer as a default serializer
                return BookSerializer
