
from rest_framework import permissions
from reviews.models import MyUser


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role == MyUser.ROLE_MODERATOR
                or request.user.role == MyUser.ROLE_ADMIN
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin or request.user.is_superuser
            )
        )
