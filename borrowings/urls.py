from django.urls import include, path
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingViewSet

app_name = "borrowings"

router = DefaultRouter()
router.register("borrowings", BorrowingViewSet, basename="borrowings")

urlpatterns = [
    path("", include(router.urls)),
]
