from rest_framework.permissions import BasePermission
from .models import User


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.MANAGER)


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.EMPLOYEE)
