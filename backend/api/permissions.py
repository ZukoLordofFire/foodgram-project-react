from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS)


class AdminOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user and request.user.is_staff
        )


class AuthorOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or obj.author == request.user:
            return True
        return False


CombinedPermission = (AuthorOnly or AdminOnly or ReadOnly)
