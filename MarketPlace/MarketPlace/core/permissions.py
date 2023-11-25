from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super().has_permission(request, view)
