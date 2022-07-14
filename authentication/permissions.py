from rest_framework import permissions
from .models import CustomUser, User


def is_user_customer(request):
    if request.user.is_authenticated:
        return request.user.user_type == 1
    else:
        return False


class IsUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 1:
            return True
        return False


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 0:
            return True
        return False


class IsAdminOrUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.user_type == 0 or request.user.user_type == 1):
            if request.method == 'POST' and request.user.user_type != 0:
                return False
            else:
                return True
        return False



class AdminOrUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if (request.method in ['POST', 'PATCH', 'PUT', 'DELETE']) and request.user.user_type in [0, 1]:
                return True
            else:
                return False
        return False

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if (request.method in ['POST', 'PATCH', 'PUT', 'DELETE']) and request.user.user_type == 1:
                return True
            else:
                return False
        return False
