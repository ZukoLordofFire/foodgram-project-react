from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from users.models import UserRole


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS)


class AdminOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == UserRole.ADMIN)
        )


class AuthorOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.author == request.user:
            return True


CombinedPermission = (AuthorOnly or AdminOnly or ReadOnly)
