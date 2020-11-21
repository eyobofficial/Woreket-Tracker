from rest_framework import permissions

from shared.constants import ROLE_ADMIN


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """Ensure non-admin users have read-only access"""
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            return request.user.role == ROLE_ADMIN
        except AttributeError:
            return False
