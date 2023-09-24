"""Custom permissions for API application."""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission to make only author change his value."""

    def has_object_permission(self, request, view, obj):
        """If object is author then you can change value."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
