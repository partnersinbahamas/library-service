from django.urls import path
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CreateUserView, ManageUserView

BASE_API_URL = settings.BASE_API_URL

urlpatterns = [
    path(f"{BASE_API_URL}/register/", CreateUserView.as_view(), name="register"),
    path(f"{BASE_API_URL}/login/", TokenObtainPairView.as_view(), name="login"),
    path(f"{BASE_API_URL}/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{BASE_API_URL}/me/", ManageUserView.as_view(), name="me"),
]
