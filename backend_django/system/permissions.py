from rest_framework import permissions
from system.models import *


def check_user_role(user, role_key):
    roles = Role.objects.filter(id__in=user.user_role.values_list('role_id'))
    if role_key in roles.values_list('name', flat=True):
        return True
    else:
        return False

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and check_user_role(request.user, 'admin')

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser or check_user_role(request.user, 'admin'):
            return True
        # 请求用户是否是创建者
        return obj.creator == request.user

class HasRolePermission(permissions.BasePermission):
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        roles = Role.objects.filter(id__in=request.user.user_role.values_list('role_id'))
        for role in roles:
            if role.role_name in self.allowed_roles:
                return True
        return False
