from rest_framework.permissions import BasePermission , SAFE_METHODS
from rest_framework import permissions





class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access for all users
        return request.user and request.user.is_staff  # Only allow write access for admin users
    



class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        super().__init__()
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
