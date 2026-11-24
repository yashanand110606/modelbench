from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read for any authenticated user, write only for staff admins."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff
