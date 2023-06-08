from rest_framework import permissions

from reviews.models import MyUser


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_authenticated
            or request.user.role == MyUser.ROLE_MODERATOR
            or request.user.role == MyUser.ROLE_ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        # Разрешить доступ, если пользователь является автором
        # или модератором или администратором
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                obj.author == request.user
                or request.user.role == MyUser.ROLE_MODERATOR
                or request.user.role == MyUser.ROLE_ADMIN
            )
        ):
            return True

        return False
