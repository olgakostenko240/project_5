from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(permissions.BasePermission):
    """Проверяет является ли пользователь модератором."""

    def has_permission(self, request, view):
        if request.user.groups.filter(name="moders").exists():
            return True
        return False


class IsOwner(permissions.BasePermission):
    """Проверяет является ли пользователь владельцем для Well и Lesson."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsStaff(BasePermission):
    """Проверяет является ли пользователь владельцем для User."""

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False
