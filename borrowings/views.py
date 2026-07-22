from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.pagination import BorrowingsListPagination
from borrowings.serializers import (
    BorrowingDetailSerializer,
    BorrowingRepaySerializer,
    BorrowingSerializer,
)
from borrowings.services import BorrowingService


class BorrowingViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BorrowingsListPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.validated_data.pop("book")

        borrowing = BorrowingService.book_borrow(
            book, request.user, **serializer.validated_data
        )

        response_serializer = self.get_serializer(borrowing)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    # Using get temporary to test the action in DRF Browser API
    @action(detail=True, methods=["get", "post"])
    def repay(self, request, *args, **kwargs):
        borrowing = self.get_object()

        serializer = self.get_serializer(borrowing, data={}, partial=True)
        serializer.is_valid(raise_exception=True)

        BorrowingService.book_repay(borrowing)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return BorrowingDetailSerializer
            case "repay":
                return BorrowingRepaySerializer
            case _:
                return BorrowingSerializer
