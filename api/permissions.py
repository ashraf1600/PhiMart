from rest_framework.permissions import BasePermission , SAFE_METHODS
from rest_framework import permissions





class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access for all users
        return request.user and request.user.is_staff  # Only allow write access for admin users