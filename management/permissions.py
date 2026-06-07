from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsAdminUser().has_permission(request, view)
